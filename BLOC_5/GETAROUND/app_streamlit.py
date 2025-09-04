import streamlit as st
st.image("./img/getaround.jpg")

with st.sidebar:
    st.title("Dashboard Menu")
    
    st.page_link("app.py", label="Accueil", icon="🏠")
    st.page_link("pages/1_EDA_GetAround.py", label="EDA GetAround", icon="📈")
    st.page_link("pages/2_Simulateur_Seuil.py", label="Simulateur Seuil", icon="⏱️")
    st.page_link("pages/3_Prediction_Prix.py", label="Prediction Prix", icon="💰")