
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Dashboard de Chamados", page_icon="📊", layout="wide")

CSV_URL = "https://docs.google.com/spreadsheets/d/1vkBUlqKyquL6auioTkW_kNMvLqpRohgyCfHvV0viR58/export?format=csv&gid=1963619439"

@st.cache_data(ttl=300)
def carregar_dados():
    return pd.read_csv(CSV_URL)

df = carregar_dados()

def pegar_coluna(df, nomes):
    mapa = {str(c).strip().lower(): c for c in df.columns}
    for nome in nomes:
        if nome.lower() in mapa:
            return mapa[nome.lower()]
    return None

def card(titulo, valor, subtitulo=""):
    st.markdown(f'''
    <div style="background:white;padding:18px;border-radius:16px;border:1px solid #eee;box-shadow:0 4px 12px rgba(0,0,0,0.05)">
        <div style="font-size:14px;color:#6b7280">{titulo}</div>
        <div style="font-size:28px;font-weight:700;color:#111">{valor}</div>
        <div style="font-size:12px;color:#6b7280">{subtitulo}</div>
    </div>
    ''', unsafe_allow_html=True)

col_status = pegar_coluna(df, ["Status"])
col_tecnico = pegar_coluna(df, ["Técnico","Tecnico"])
col_duracao = pegar_coluna(df, ["Duração Exec. em minutos","Duracao Exec. em minutos"])

# ===== CARDS INTELIGENTES =====
status_aberto = ["aberto","pendente","em andamento"]
status_fechado = ["finalizado","concluido","fechado"]

abertos = 0
fechados = 0

if col_status:
    status_series = df[col_status].astype(str).str.lower()
    abertos = status_series.isin(status_aberto).sum()
    fechados = status_series.isin(status_fechado).sum()

top_tecnico = "-"
top_qtd = 0

if col_tecnico:
    ranking = df[col_tecnico].value_counts()
    if not ranking.empty:
        top_tecnico = ranking.index[0]
        top_qtd = ranking.iloc[0]

tempo_medio = None
if col_duracao:
    df[col_duracao] = pd.to_numeric(df[col_duracao], errors="coerce")
    tempo_medio = round(df[col_duracao].dropna().mean(),1)

st.title("📊 Dashboard de Chamados")

c1,c2,c3,c4 = st.columns(4)

with c1:
    card("🔴 Chamados abertos", abertos, "Precisam de atenção")

with c2:
    card("🟢 Chamados fechados", fechados, "Resolvidos")

with c3:
    card("⚡ Tempo médio", f"{tempo_medio} min" if tempo_medio else "-", "Performance")

with c4:
    card("👑 Top técnico", top_tecnico, f"{top_qtd} chamados")

st.subheader("📊 Top técnicos")
if col_tecnico:
    st.bar_chart(df[col_tecnico].value_counts())

st.subheader("📌 Status")
if col_status:
    st.bar_chart(df[col_status].value_counts())

st.subheader("📋 Dados")
st.dataframe(df, use_container_width=True)
