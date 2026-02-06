import pandas as pd
import plotly.express as px
import streamlit as st

df = pd.read_excel("https://raw.githubusercontent.com/alecamargo33-code/esocialnovo/refs/heads/master/eventos_esocial.xlsx")

st.set_page_config(
    page_title="Indicadores eSocial",
    layout="wide"
)
st.title("Gestão eSocial")
st.write("Dashboard local")

st.sidebar.header("Filtros")

#Filtro de ano
anos_disponiveis = sorted(df['Ano'].unique())
anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)

#Filtro de evento
eventos_disponiveis = sorted(df['Código Evento'].unique())
eventos_selecionados = st.sidebar.multiselect("Evento", eventos_disponiveis, default=eventos_disponiveis)

#Filtro de status do evento
status_disponiveis = sorted(df['Status Evento'].astype(str).unique())
status_selecionados = st.sidebar.multiselect("Status do Evento", status_disponiveis, default=status_disponiveis)





