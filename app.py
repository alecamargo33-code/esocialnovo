import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Indicadores eSocial",
    layout="wide"
)
st.title("Gestão eSocial")
st.write("Dashboard local")

df = pd.DataFrame(
    {"Categoria":["A","B","C","D"],
     "Valor":[10,25,40,55]
     }
)

st.bar_chart(df.set_index("Categoria"))