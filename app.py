import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
        df_contagem = df_contagem.sort_values(by='Ano')

        grafico_eventos = go.Figure()
        for evento in df_contagem['Código Evento'].unique():
            df_evento = df_contagem[df_contagem['Código Evento'] == evento]
            grafico_eventos.add_trace(
                go.Scatter(
                    x=df_evento['Ano'],
                    y=df_evento['total'],
                    mode='line+markers',
                    name=f"Evento {evento}",
                    hovertemplate="<b>Evento %{fullData.name}</b><br>Ano:{x}<br>Qtd: %{y}<extra></extra>",
                    line=dict(width=3),
                    marker=dict(size=8),
                    connectgaps=True
                )
            )
            grafico_eventos.update_layout(
                hovermode="x unified", # Mostra todos os eventos juntos ao passar o mouse
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    margin=dict(l=0, r=0, t=30, b=0),
                    xaxis=dict(type='category'), # Força o eixo X a ser categórico
                    yaxis=dict(rangemode="tozero") # Garante que o gráfico comece do zero
            )
            st.plotly_chart(grafico_eventos, use_container_width=True)
      
    else:
        st.warning("Opa erro")










