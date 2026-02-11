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
    eventos_concluidos = len(df_filtrado[df_filtrado['Status Evento'] == "Concluido"])
    eventos_erros = len(df_filtrado[df_filtrado['Status Evento'] == "Inconsistencias"])
else:
    total_eventos = 0; eventos_concluidos = 0; eventos_erros = 0

col1, col2, col3 = st.columns(3)
col1.metric("Total de eventos", f"{total_eventos}")
col2.metric("Eventos concluidos", f"{eventos_concluidos}")
col3.metric(
    label = "Eventos Inconsistentes", 
    value = f"{eventos_erros}",
    help = "xml com inconsistencias"
) 

st.markdown("---")

# --- Análise visuais ---
st.subheader("Gráfios")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        st.markdown("Evolução dos eventos")
        eventos_de_interesse = ['2220','2240','2221','2210']
        df_filtrado = df[df["Código Evento"].isin(eventos_de_interesse)]

        df_contagem = df_filtrado.groupby(['Ano', 'Código Evento']).size().reset_index(name='total')
        df_contagem['Ano'] = df_contagem['Ano'].astype(str)
        df_contagem = df_contagem.sort_values(by='Ano')

        grafico_eventos = px.line(
            df_contagem,
            x = 'Ano',
            y = 'total',
            color = 'Código Evento',
            markers = True,
            line_group = 'Código Evento',
            title = "Eventos por Ano",
            labels = {'total': 'Qtd de eventos','Ano':'ano'}
        )
        grafico_eventos.update_xaxes(type='category')
        st.plotly_chart(grafico_eventos,use_container_width=True)
    else:
        st.warning("Opa erro")










