import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
WIDTH = 800
HEIGHT = 700

st.set_page_config(page_title="EDA GetAround", page_icon="📊")

with st.sidebar:
    st.title("Dashboard Menu")
    
    st.page_link("app.py", label="Accueil", icon="🏠")
    st.page_link("pages/1_EDA_GetAround.py", label="EDA GetAround", icon="📈")
    st.page_link("pages/2_Simulateur_Seuil.py", label="Simulateur Seuil", icon="⏱️")
    st.page_link("pages/3_Prediction_Prix.py", label="Prediction Prix", icon="💰")

st.html(
    "<h1 style='color: #b725c8cc; font-size: 22px'>EDA GETAROUND</span>!</h1>"
)

df = pd.read_excel("get_around_delay_analysis.xlsx")

# Calculer le nombre de valeurs manquantes par colonne
missing_values_count = df.isnull().sum()

# Calculer le pourcentage de valeurs manquantes par colonne
missing_values_percent = (missing_values_count / len(df)) * 100

# Créer un nouveau DataFrame pour afficher les résultats
missing_data = pd.DataFrame({
    'missing_values_count': missing_values_count,
    'missing_values_percent': missing_values_percent
})

missing_df = missing_data[missing_data['missing_values_count'] > 0]
missing_df_percent = missing_df['missing_values_percent'].reset_index()

missing = px.bar(missing_df_percent, x = "index", y = "missing_values_percent",
       hover_data=['index'], title="Données manquantes en pourcentage", color='index', text_auto='.2s')

fig = px.bar(
    missing_df_percent,
    x="index",
    y="missing_values_percent",
    hover_data=['index'],
    title="Données manquantes en pourcentage",
    color='index',
    text_auto='.2f',
    text="missing_values_percent"
)

# Personnalisation pour ajouter le % et mettre en gras
fig.update_traces(
    texttemplate='<b>%{text:.2f}%</b>',
    textposition='inside'
)

# Affichage dans Streamlit
st.plotly_chart(fig, use_container_width=True)

#% de Clients qui vont jusqu'au bout versus % de Clients qui abandonnent.

st.html(
    "<h2 style='color: #b725c8cc; font-size: 20px'>Clients qui louent versus Clients qui abandonnent</span>!</h1><span style='font-style: italic; text-align='right'>DataScience 33 - Eric Nguyen</span>"
)


state_car = df['state'].value_counts()
state_car = pd.DataFrame(state_car).reset_index()
state_car.columns = ['state', 'count']

min_count = state_car['count'].min()
min_state = state_car[state_car['count'] == min_count]['state'].values[0]
max_count = state_car['count'].max()
max_state = state_car[state_car['count'] == max_count]['state'].values[0]

state_car['state_with_emoji'] = state_car['state'].apply(
    lambda x: f'🚗 {x}' if x == min_state else (f'🚙 {x}' if x == max_state else x)
)

fig = px.pie(
    state_car,
    values='count',
    names='state_with_emoji',
    title='% de Clients qui concluent vs % de clients qui abandonnent',
    color='state',
    width=800,
    hole=0.3
)

fig.update_traces(
    textposition='inside',
    insidetextorientation='radial',
    marker=dict(
        colors=['yellow' if state == min_state else color
                for state, color in zip(state_car['state'], fig.data[0].marker.colors)],
        line=dict(
            color='white',
            width=[3 if state == min_state else 1
                   for state in state_car['state']]
        )
    ),
    textinfo='percent+label',
    textfont=dict(
        size=14,
        color='black'
    )
)

st.plotly_chart(fig)

#-------------------

# --- Titre et description ---
st.html(
    "<h2 style='color: #b725c8cc; font-size: 20px'>Répartition des clients par état et par Device</span>!</h1><span style='font-style: italic; text-align='right'>DataScience 33 - Eric Nguyen</span>"
)

fig = go.Figure()

checkin_df = df.groupby('checkin_type')['state'].value_counts()
checkin_df = pd.DataFrame(checkin_df).reset_index()
checkin_df_connect = checkin_df[checkin_df['checkin_type'] == 'connect']['count'].sum()
checkin_df_mobile = checkin_df[checkin_df['checkin_type'] == 'mobile']['count'].sum()
total_checkin = checkin_df['count'].sum()
checkin_df = checkin_df.assign(percent=lambda x: (x['count']/total_checkin)*100)

emoji_map = {
    'ended': '🚙',
    'canceled': '🚗'
}

color_map = {
    'ended': '#647CF6',
    'canceled': '#F06050'
}

for state in checkin_df['state'].unique():
    df_state = checkin_df[checkin_df['state'] == state]
    emoji = emoji_map[state]
    color = color_map[state]

    fig.add_trace(go.Bar(
        x=df_state['checkin_type'],
        y=df_state['percent'],
        name=state,
        text=df_state['percent'].apply(lambda x: f'{round(x, 1)}% {emoji}'),
        textfont=dict(size=16, weight='bold', color='black'),
        textposition="outside",
        marker_color=color,
        marker_line_width=0
    ))

fig.update_layout(
    yaxis_title='Percent',
    xaxis_title=None,
    barmode='group',
    plot_bgcolor='rgb(240, 242, 246)',
    paper_bgcolor='white',
    yaxis=dict(gridcolor='white', range=[0, max(checkin_df['percent']) * 1.15]),
    xaxis=dict(tickfont=dict(size=14)),
    legend_title_text='État du Check-in',
    font=dict(family="Arial, sans-serif"),
    width=800,
    height=600
)

st.plotly_chart(fig)

# Type de Check in

st.html(
    "<h2 style='color: #b725c8cc; font-size: 20px'>Analyse des annulations par type de check-in</span>!</h1><span style='font-style: italic; text-align='right'>DataScience 33 - Eric Nguyen</span>"
)

# Préparation des données
mask_canceled = df['state'] == 'canceled'
car_canceled_detail = df[mask_canceled]
car_canceled_detail = car_canceled_detail['checkin_type'].value_counts().reset_index()
car_canceled_detail.columns = ['checkin_type', 'count']

# Trouver les segments le plus petit et le plus gros
min_count = car_canceled_detail['count'].min()
min_type = car_canceled_detail[car_canceled_detail['count'] == min_count]['checkin_type'].values[0]
max_count = car_canceled_detail['count'].max()
max_type = car_canceled_detail[car_canceled_detail['count'] == max_count]['checkin_type'].values[0]

# Ajouter les emojis selon la taille du segment
car_canceled_detail['checkin_type_with_emoji'] = car_canceled_detail['checkin_type'].apply(
    lambda x: f'🚗 {x}' if x == min_type else (f'🚙 {x}' if x == max_type else x)
)

# Créer le camembert avec les couleurs personnalisées
fig = px.pie(
    car_canceled_detail,
    values='count',
    names='checkin_type_with_emoji',
    title='Groupe Cancel : Checkin Type',
    color='checkin_type',
    width=800,
    hole=0.3,
    color_discrete_map={min_type: 'yellow', max_type: '#6275F7'}
)

# Détacher le petit segment et ajuster la mise en forme
fig.update_traces(
    pull=[0.1 if checkin_type == min_type else 0 for checkin_type in car_canceled_detail['checkin_type']],
    textposition='inside',
    insidetextorientation='radial',
    marker=dict(line=dict(color='white', width=2)),
    textinfo='percent+label',
    textfont=dict(size=14, color='black')
)

st.plotly_chart(fig)

#------


#---

st.html(
    "<h2 style='color: #b725c8cc; font-size: 20px'>Canceled selon les intervalles de temps</span>!</h1><span style='font-style: italic; text-align='right'>DataScience 33 - Eric Nguyen</span>"
)

mask_delta = df['time_delta_with_previous_rental_in_minutes'] >=  0
delta = df[mask_delta]
delta_canceled = delta[delta['state'] == 'canceled']
mask_canceled = df['state'] == 'canceled'
df_canceled = df[mask_canceled].shape[0]

time_bins = [0, 15, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 400, 500, 600, 700, 750]
labels = [f"{time_bins[i]}-{time_bins[i+1]} min" for i in range(len(time_bins)-1)]
delta_canceled['time_interval'] = pd.cut(
    delta_canceled['time_delta_with_previous_rental_in_minutes'],
    bins=time_bins,
    labels=labels,
    right=True,
    include_lowest=True
)
cancellation_counts = delta_canceled['time_interval'].value_counts().sort_index()

df_plot = cancellation_counts.reset_index()
df_plot.columns = ['Intervalle', 'Nombre']

fig = px.bar(
    df_plot,
    x='Intervalle',
    y='Nombre',
    color='Nombre',
    color_continuous_scale='Plasma_r',
    title="Distribution des Annulations - Canceled - par Intervalle de Temps",
    labels={"Intervalle": "Intervalle de temps (minutes)", "Nombre": "Nombre d'annulations"}
)

fig.update_layout(
    xaxis_tickangle=-45,
    coloraxis_showscale=False,
    template="seaborn"
)

fig.update_traces(
    text=df_plot['Nombre'],
    textposition='outside',
    textfont_size=10
)

st.plotly_chart(fig)

#---

#Visualisation des Cancels et les outliers

delay_mask = df['delay_at_checkout_in_minutes'] > 0
delay_dataf = df[delay_mask]
fig = px.scatter(delay_dataf, x = "delay_at_checkout_in_minutes")
st.plotly_chart(fig)

#Transformation des status Early en On Time

def status_time(x):
    if x <0:
        return 'ONTIME'
    elif x > 0:
        return "DELAY"
    else:
        return "NOFINFO"


df['time'] = df['delay_at_checkout_in_minutes'].apply(status_time)
df['time'] = df.apply(lambda row: row['state'].upper() if row['time'] == 'NOFINFO' else row['time'], axis=1)
df_state = df['time'].value_counts()
df_state_detail = pd.DataFrame(df_state).reset_index()
status = px.pie(df_state_detail, values='count', names = 'time', width=WIDTH, title="State of the Car")
st.plotly_chart(status)