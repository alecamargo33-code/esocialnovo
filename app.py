import pandas as pd
import plotly.express as px
import streamlit as st

df = pd.read_parquet("https://raw.githubusercontent.com/alecamargo33-code/esocialnovo/refs/heads/master/eventos_esocial.parquet")

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

# --- Filtragem do DataFrame ---
# O dataframe principal é filtrado com base nas seleções feitas na barra lateral.
df_filtrado = df[
    (df['Ano'].isin(anos_selecionados)) &
    (df['Código Evento'].isin(eventos_selecionados)) &
    (df['Status Evento'].isin(status_selecionados))
]

# --- Conteúdo Principal ---
st.title("🎲 Dashboard de Análise eSocial")
st.markdown("Explore os dados do eSocial, use filtros à esquerda para refinar sua análise.")

# --- Métricas Principais (KPIs) ---
st.subheader("Big Numbers")

if not df_filtrado.empty:
    total_eventos = len(df_filtrado)
    eventos_2240 = len(df_filtrado[df_filtrado['Código Evento'] == 2240])
else:
    total_eventos = 0; eventos_2240 = 0

col1, col2 = st.columns(2)
col1.metric("Total de eventos", f"{total_eventos:,.0f}")
col2.metric("Eventos 2240", f"{eventos_2240:,.0f}")

st.markdown("---")









