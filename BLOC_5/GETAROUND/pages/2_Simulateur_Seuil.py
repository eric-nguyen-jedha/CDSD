
import streamlit as st
import pandas as pd
import altair as alt

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Simulateur de Seuil Getaround", page_icon="🧮")

with st.sidebar:
    st.title("Dashboard Menu")
    
    st.page_link("app.py", label="Accueil", icon="🏠")
    st.page_link("pages/1_EDA_GetAround.py", label="EDA GetAround", icon="📈")
    st.page_link("pages/2_Simulateur_Seuil.py", label="Simulateur Seuil", icon="⏱️")
    st.page_link("pages/3_Prediction_Prix.py", label="Prediction Prix", icon="💰")

st.html(
    "<h1 style='color: #b725c8cc; font-size: 22px'>Simulateur de Seuil d'Annulation pour Getaround</span>!</h1>"
)


# --- 1. CHARGEMENT ET PRÉPARATION DES DONNÉES ---
# Optimisation des performances de Streamlit : 1 chargement.
@st.cache_data
def load_data(path):
    df = pd.read_excel(path)
    # On s'assure que la colonne est bien numérique pour les comparaisons
    df['time_delta_with_previous_rental_in_minutes'] = pd.to_numeric(df['time_delta_with_previous_rental_in_minutes'], errors='coerce')
    return df

df = load_data("get_around_delay_analysis.xlsx")

# DataFrames de base pour les calculs. On se focalise sur les locations consécutives.
base_df = df[df['time_delta_with_previous_rental_in_minutes'].notna() & (df['time_delta_with_previous_rental_in_minutes'] >= 0)].copy()

# Filtre > 30 min
# On ne garde que les locations où le temps de battement est de 30 minutes ou plus.
SEUIL_MINIMUM_ANALYSE = 30
base_df = df[df['time_delta_with_previous_rental_in_minutes'] >= SEUIL_MINIMUM_ANALYSE].copy()

all_consecutive_rentals_count = len(base_df)
canceled_df = base_df[base_df['state'] == 'canceled'].copy()
mobile_canceled_df = canceled_df[canceled_df['checkin_type'] == 'mobile'].copy()
connect_canceled_df = canceled_df[canceled_df['checkin_type'] == 'connect'].copy()

# --- 2. FONCTIONS DE CALCUL ---
def calculate_cancellation_rate(dataframe, threshold):
    count = dataframe[dataframe["time_delta_with_previous_rental_in_minutes"] <= threshold].shape[0]
    return (count / all_consecutive_rentals_count) * 100 if all_consecutive_rentals_count > 0 else 0

def calculate_impact(threshold):
    lost_clients = canceled_df[canceled_df["time_delta_with_previous_rental_in_minutes"] <= threshold].shape[0]
    lost_clients_pct_total = (lost_clients / len(df)) * 100 if len(df) > 0 else 0
    
    total_consecutive_cancellations = len(canceled_df)
    remaining_problems_pct = ((total_consecutive_cancellations - lost_clients) / total_consecutive_cancellations) * 100 if total_consecutive_cancellations > 0 else 0
    
    return lost_clients, lost_clients_pct_total, remaining_problems_pct

# --- 3. PRÉ-CALCUL POUR LA COURBE (méthode Pandas) ---

st.html(
    "<h2 style='color: #b725c8cc; font-size: 20px'>Visualisez l'accumulation des annulations en fonction du temps.</span>!</h2>"
)

cancellation_counts = canceled_df['time_delta_with_previous_rental_in_minutes'].value_counts()
full_range_counts = cancellation_counts.reindex(range(751), fill_value=0).sort_index()
cumulative_cancellations = full_range_counts.cumsum()

plot_data = cumulative_cancellations.reset_index()
plot_data.columns = ['seuil_minutes', 'clients_perdus_cumul']

total_cancellations = len(canceled_df)
plot_data['probleme_cible_pct'] = (plot_data['clients_perdus_cumul'] / total_cancellations) * 100 if total_cancellations > 0 else 0

# --- 4. INTERFACE UTILISATEUR (Slider et Graphique) ---
time_delta = st.slider("Choisissez une fenêtre de temps d'action (en minutes)", min_value=0, max_value=750, value=90)

# Création du graphique Altair
base = alt.Chart(plot_data).encode(
    x=alt.X('seuil_minutes', title='Fenêtre de temps (minutes)')
)

line = base.mark_line().encode(
    y=alt.Y('clients_perdus_cumul', title="Nombre cumulé d'annulations"),
    tooltip=[
        alt.Tooltip('seuil_minutes', title='Seuil (min)'),
        alt.Tooltip('clients_perdus_cumul', title='Clients perdus cumulés'),
        alt.Tooltip('probleme_cible_pct', title='Part du Problème Ciblée (%)', format='.1f')
    ]
).properties(
    title="Concentration des Annulations en Fonction du Temps"
)

vertical_line = alt.Chart(pd.DataFrame({'x': [time_delta]})).mark_rule(color='#b725c8cc', strokeDash=[3,3]).encode(x='x')

# Point sur la courbe avec les couleurs personnalisées
point_on_line = alt.Chart(plot_data[plot_data['seuil_minutes'] == time_delta]).mark_point(
    color='#b725c8cc',
    size=150,
    filled=True
).encode(
    x='seuil_minutes',
    y='clients_perdus_cumul'
)

# Texte sur le point (bulle) avec les couleurs personnalisées
text_on_point = point_on_line.mark_text(
    align='center',
    baseline='bottom',
    dy=-10,  # Décalage vertical pour positionner au-dessus du point
    color='#fed58cff',
    fontSize=14,
    fontWeight='bold'
).encode(
    text=alt.Text('clients_perdus_cumul:Q')
)

final_chart = (line + vertical_line + point_on_line + text_on_point).interactive()
st.altair_chart(final_chart, use_container_width=True)

# --- 5. AFFICHAGE DES KPIs ---
st.header(f"Analyse pour la fenêtre de temps de {time_delta} minutes")

# Calcul des KPIs pour le seuil choisi
total_annul_rate = calculate_cancellation_rate(canceled_df, time_delta)
mobile_annul_rate = calculate_cancellation_rate(mobile_canceled_df, time_delta)
desktop_annul_rate = calculate_cancellation_rate(connect_canceled_df, time_delta)
lost_clients, lost_clients_pct_total, remaining_problems_pct = calculate_impact(time_delta)
targeted_problem_pct = 100 - remaining_problems_pct

# Affichage avec st.metric pour un look propre
col1, col2, col3 = st.columns(3)
col1.metric("🚘 Taux d'Annulation Ciblé", f"{total_annul_rate:.2f}%", help="Pourcentage de toutes les locations consécutives qui sont annulées dans ce délai.")
col2.metric("📱 Annulations Mobiles Ciblées", f"{mobile_annul_rate:.2f}%")
col3.metric("💻 Annulations Desktop Ciblées", f"{desktop_annul_rate:.2f}%")

col1, col2, col3 = st.columns(3)
col1.metric("🤦‍♀️ Clients Perdus dans ce délai (nb)", f"{lost_clients:,.0f}")
col2.metric("🤷‍♂️ Impact sur le total des locations (%)", f"{lost_clients_pct_total:.2f}%")
col3.metric("🎯 Part du Problème Ciblée (%)", f"{100 - targeted_problem_pct:.2f}%", help="Pourcentage de TOUTES les annulations consécutives qui se produisent dans cette fenêtre de temps.")