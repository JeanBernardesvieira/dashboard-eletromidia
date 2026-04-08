import pandas as pd
import streamlit as st

st.set_page_config(page_title="Dashboard de Chamados", layout="wide")

CSV_URL = "https://docs.google.com/spreadsheets/d/1vkBUlqKyquL6auioTkW_kNMvLqpRohgyCfHvV0viR58/export?format=csv&gid=1963619439"

@st.cache_data(ttl=300)
def carregar_dados():
    df = pd.read_csv(CSV_URL)
    return df

df = carregar_dados()

st.title("📊 Dashboard de Chamados")
st.caption("Dados carregados diretamente da sua planilha Google Sheets")

with st.sidebar:
    st.header("Controles")
    if st.button("Atualizar dados"):
        st.cache_data.clear()
        st.rerun()
    st.info("Este painel lê os dados direto da planilha online.")

st.subheader("Resumo rápido")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total de registros", len(df))

with col2:
    st.metric("Total de colunas", len(df.columns))

with col3:
    st.metric("Fonte", "Google Sheets")

st.subheader("Colunas encontradas")
st.write(list(df.columns))

st.subheader("Visualização dos dados")
st.dataframe(df, use_container_width=True)
