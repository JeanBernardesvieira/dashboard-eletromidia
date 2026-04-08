
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Dashboard de Chamados", layout="wide")

CSV_URL = "https://docs.google.com/spreadsheets/d/1vkBUlqKyquL6auioTkW_kNMvLqpRohgyCfHvV0viR58/export?format=csv&gid=1963619439"

@st.cache_data(ttl=300)
def carregar_dados():
    return pd.read_csv(CSV_URL)

def pegar_coluna(df, nomes):
    mapa = {str(c).strip().lower(): c for c in df.columns}
    for nome in nomes:
        if nome.lower() in mapa:
            return mapa[nome.lower()]
    return None

def limpar_texto(s):
    return s.astype(str).str.strip()

def normalizar_texto(s):
    return limpar_texto(s).str.lower()

def card_html(titulo, valor, subtitulo="", classe=""):
    return f'<div class="kpi-card {classe}"><div class="kpi-title">{titulo}</div><div class="kpi-value">{valor}</div><div class="kpi-subtitle">{subtitulo}</div></div>'

df = carregar_dados()

col_status = pegar_coluna(df, ["Status"])
col_tecnico = pegar_coluna(df, ["Técnico","Tecnico"])
col_ponto = pegar_coluna(df, ["Ponto"])
col_duracao = pegar_coluna(df, ["Duração Exec. em minutos","Duracao Exec. em minutos"])

if col_duracao:
    df[col_duracao] = pd.to_numeric(df[col_duracao], errors="coerce")

st.markdown("""<style>
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.kpi-card{background:white;padding:18px;border-radius:16px;border:1px solid #eee}
.kpi-title{font-size:14px;color:#666}
.kpi-value{font-size:28px;font-weight:700}
.kpi-subtitle{font-size:12px;color:#888}
.open{border-left:5px solid red}
.closed{border-left:5px solid green}
.time{border-left:5px solid blue}
.top{border-left:5px solid orange}
</style>""", unsafe_allow_html=True)

status_aberto=["aberto","pendente","em andamento"]
status_fechado=["finalizado","concluido","fechado"]

abertos=0
fechados=0

if col_status:
    s=normalizar_texto(df[col_status])
    abertos=int(s.isin(status_aberto).sum())
    fechados=int(s.isin(status_fechado).sum())

top_tecnico="-"
top_qtd=0
if col_tecnico:
    r=df[col_tecnico].value_counts()
    if not r.empty:
        top_tecnico=r.index[0]
        top_qtd=int(r.iloc[0])

tempo_medio=None
if col_duracao:
    tempo_medio=round(df[col_duracao].mean(),1)

html_cards = (
    '<div class="kpi-grid">'
    + card_html("🔴 Abertos", abertos,"","open")
    + card_html("🟢 Fechados", fechados,"","closed")
    + card_html("⚡ Tempo", f"{tempo_medio} min" if tempo_medio else "-","","time")
    + card_html("👑 Top", top_tecnico,f"{top_qtd} chamados","top")
    + '</div>'
)

st.markdown(html_cards, unsafe_allow_html=True)

st.subheader("Dados")
st.dataframe(df)
