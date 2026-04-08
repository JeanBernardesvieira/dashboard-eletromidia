import pandas as pd
import streamlit as st

st.set_page_config(page_title="Dashboard de Chamados", page_icon="📊", layout="wide")

CSV_URL = "https://docs.google.com/spreadsheets/d/1vkBUlqKyquL6auioTkW_kNMvLqpRohgyCfHvV0viR58/export?format=csv&gid=1963619439"

@st.cache_data(ttl=300)
def carregar_dados():
    return pd.read_csv(CSV_URL)

def pegar_coluna(df, nomes):
    mapa = {str(c).strip().lower(): c for c in df.columns}
    for nome in nomes:
        chave = str(nome).strip().lower()
        if chave in mapa:
            return mapa[chave]
    return None

def limpar_texto(serie):
    return serie.astype(str).str.strip()

def normalizar_texto(serie):
    return limpar_texto(serie).str.lower()

def card_html(titulo, valor, subtitulo="", classe_extra=""):
    return f"""
    <div class="kpi-card {classe_extra}">
        <div class="kpi-title">{titulo}</div>
        <div class="kpi-value">{valor}</div>
        <div class="kpi-subtitle">{subtitulo}</div>
    </div>
    """

df = carregar_dados()

# Descoberta de colunas
col_status = pegar_coluna(df, ["Status"])
col_tecnico = pegar_coluna(df, ["Técnico", "Tecnico"])
col_cidade = pegar_coluna(df, ["Cidade"])
col_ambiente = pegar_coluna(df, ["Ambiente"])
col_ponto = pegar_coluna(df, ["Ponto"])
col_duracao = pegar_coluna(df, ["Duração Exec. em minutos", "Duracao Exec. em minutos"])
col_data = pegar_coluna(df, [
    "Data de Criação", "Data de Criacao",
    "Data Criação", "Data Criacao",
    "Data"
])

if col_duracao:
    df[col_duracao] = pd.to_numeric(df[col_duracao], errors="coerce")

if col_data:
    df[col_data] = pd.to_datetime(df[col_data], errors="coerce", dayfirst=True)
    df["MesRef"] = df[col_data].dt.to_period("M").astype(str)
else:
    df["MesRef"] = "Sem data"

st.markdown("""
<style>
    .main > div {padding-top: 1rem;}
    .block-container {padding-top: 1.2rem; padding-bottom: 2rem;}
    div[data-testid="stDataFrame"] {border-radius: 16px; overflow: hidden; border: 1px solid #e5e7eb;}
    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e5e7eb;
        padding: 12px;
        border-radius: 16px;
    }
    .hero {
        padding: 24px;
        border-radius: 24px;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 55%, #334155 100%);
        color: white;
        box-shadow: 0 16px 40px rgba(15, 23, 42, 0.20);
        margin-bottom: 20px;
    }
    .hero-top {
        font-size: 14px;
        color: #cbd5e1;
        font-weight: 700;
        letter-spacing: .4px;
        text-transform: uppercase;
    }
    .hero-title {
        font-size: 42px;
        line-height: 1.05;
        font-weight: 900;
        margin-top: 6px;
    }
    .hero-sub {
        font-size: 15px;
        color: #e2e8f0;
        margin-top: 10px;
    }
    .section-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 22px;
        padding: 18px 18px 10px 18px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
        margin-bottom: 16px;
    }
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 14px;
        margin-bottom: 14px;
    }
    .kpi-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 20px;
        padding: 18px;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
        min-height: 132px;
    }
    .kpi-card.open {border-left: 6px solid #dc2626;}
    .kpi-card.closed {border-left: 6px solid #16a34a;}
    .kpi-card.time {border-left: 6px solid #2563eb;}
    .kpi-card.top {border-left: 6px solid #d97706;}
    .kpi-card.neutral {border-left: 6px solid #64748b;}
    .kpi-title {
        font-size: 14px;
        color: #6b7280;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 34px;
        color: #0f172a;
        font-weight: 900;
        line-height: 1.05;
        word-break: break-word;
    }
    .kpi-subtitle {
        margin-top: 8px;
        color: #64748b;
        font-size: 12px;
    }
    .small-note {
        color: #64748b;
        font-size: 13px;
        margin-top: 6px;
    }
    @media (max-width: 1100px) {
        .kpi-grid {grid-template-columns: repeat(2, minmax(0, 1fr));}
    }
</style>
""", unsafe_allow_html=True)

df_filtrado = df.copy()

with st.sidebar:
    st.header("Filtros")
    if st.button("Atualizar dados"):
        st.cache_data.clear()
        st.rerun()

    if col_tecnico:
        tecnicos = sorted([x for x in limpar_texto(df[col_tecnico].dropna()).unique() if x and x.lower() != "nan"])
        tecnico_sel = st.multiselect("Técnico", tecnicos)
        if tecnico_sel:
            df_filtrado = df_filtrado[limpar_texto(df_filtrado[col_tecnico]).isin(tecnico_sel)]

    if col_cidade:
        cidades = sorted([x for x in limpar_texto(df[col_cidade].dropna()).unique() if x and x.lower() != "nan"])
        cidade_sel = st.multiselect("Cidade", cidades)
        if cidade_sel:
            df_filtrado = df_filtrado[limpar_texto(df_filtrado[col_cidade]).isin(cidade_sel)]

    if col_status:
        status_opcoes = sorted([x for x in limpar_texto(df[col_status].dropna()).unique() if x and x.lower() != "nan"])
        status_sel = st.multiselect("Status", status_opcoes)
        if status_sel:
            df_filtrado = df_filtrado[limpar_texto(df_filtrado[col_status]).isin(status_sel)]

    if "MesRef" in df_filtrado.columns:
        meses = sorted(df_filtrado["MesRef"].dropna().unique())
        mes_sel = st.multiselect("Mês", meses)
        if mes_sel:
            df_filtrado = df_filtrado[df_filtrado["MesRef"].isin(mes_sel)]

    st.markdown("### Resumo da base")
    st.write(f"**Registros:** {len(df_filtrado)}")
    st.write(f"**Colunas:** {len(df_filtrado.columns)}")

# métricas
status_aberto = ["aberto", "pendente", "em andamento", "novo"]
status_fechado = ["finalizado", "concluido", "concluído", "fechado", "encerrado"]

abertos = 0
fechados = 0
top_tecnico = "-"
top_qtd = 0
tempo_medio = None
cidade_top = "-"
cidade_top_qtd = 0
pontos_unicos = df_filtrado[col_ponto].nunique() if col_ponto else 0
tecnicos_unicos = df_filtrado[col_tecnico].nunique() if col_tecnico else 0
total_registros = len(df_filtrado)

if col_status:
    status_series = normalizar_texto(df_filtrado[col_status])
    abertos = int(status_series.isin(status_aberto).sum())
    fechados = int(status_series.isin(status_fechado).sum())

if col_tecnico:
    ranking = limpar_texto(df_filtrado[col_tecnico]).value_counts()
    if not ranking.empty:
        top_tecnico = ranking.index[0]
        top_qtd = int(ranking.iloc[0])

if col_duracao and df_filtrado[col_duracao].notna().any():
    tempo_medio = round(df_filtrado[col_duracao].dropna().mean(), 1)

if col_cidade:
    ranking_cidade = limpar_texto(df_filtrado[col_cidade]).value_counts()
    if not ranking_cidade.empty:
        cidade_top = ranking_cidade.index[0]
        cidade_top_qtd = int(ranking_cidade.iloc[0])

mes_atual = "-"
variacao_mensal_txt = "-"
atual = None
anterior = None
if "MesRef" in df_filtrado.columns and (df_filtrado["MesRef"] != "Sem data").any():
    serie_mes = df_filtrado[df_filtrado["MesRef"] != "Sem data"]["MesRef"].value_counts().sort_index()
    if not serie_mes.empty:
        mes_atual = serie_mes.index[-1]
        atual = int(serie_mes.iloc[-1])
        if len(serie_mes) >= 2:
            anterior = int(serie_mes.iloc[-2])
            if anterior != 0:
                variacao = ((atual - anterior) / anterior) * 100
                sinal = "+" if variacao >= 0 else ""
                variacao_mensal_txt = f"{sinal}{variacao:.1f}% vs mês anterior".replace(".", ",")
            else:
                variacao_mensal_txt = "Sem base de comparação"
        else:
            variacao_mensal_txt = "Primeiro mês da base"

st.markdown(f"""
<div class="hero">
    <div class="hero-top">Painel operacional</div>
    <div class="hero-title">📊 Dashboard de Chamados</div>
    <div class="hero-sub">Atualizou a planilha, atualizou o painel. Agora com visual mais limpo, leitura mais rápida e foco no que interessa.</div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="kpi-grid">'
    + card_html("🔴 Chamados abertos", abertos, "Precisam de atenção", "open")
    + card_html("🟢 Chamados fechados", fechados, "Resolvidos", "closed")
    + card_html("⚡ Tempo médio", f"{str(tempo_medio).replace('.', ',')} min" if tempo_medio is not None else "-", "Performance geral", "time")
    + card_html("👑 Top técnico", top_tecnico, f"{top_qtd} chamados", "top")
    + '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="kpi-grid">'
    + card_html("🏙️ Cidade líder", cidade_top, f"{cidade_top_qtd} chamados", "neutral")
    + card_html("🏢 Pontos únicos", pontos_unicos, "Locais atendidos", "neutral")
    + card_html("🧰 Técnicos ativos", tecnicos_unicos, "Na base filtrada", "neutral")
    + card_html("📦 Total filtrado", total_registros, "Chamados no recorte", "neutral")
    + '</div>',
    unsafe_allow_html=True
)

mc1, mc2, mc3 = st.columns(3)
with mc1:
    st.metric("Último mês da base", mes_atual)
with mc2:
    st.metric("Chamados no mês atual", atual if atual is not None else "-")
with mc3:
    st.metric("Variação mensal", variacao_mensal_txt)

row1_col1, row1_col2 = st.columns([1.25, 1])

with row1_col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("📈 Evolução mensal")
    if "MesRef" in df_filtrado.columns and (df_filtrado["MesRef"] != "Sem data").any():
        evolucao = (
            df_filtrado[df_filtrado["MesRef"] != "Sem data"]["MesRef"]
            .value_counts()
            .sort_index()
            .rename_axis("Mês")
            .reset_index(name="Chamados")
        )
        st.line_chart(evolucao.set_index("Mês"))
        st.dataframe(evolucao, use_container_width=True, hide_index=True)
    else:
        st.info("Não encontrei coluna de data válida para montar a evolução mensal.")
    st.markdown('</div>', unsafe_allow_html=True)

with row1_col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("🗺️ Ranking por ambiente / região")
    if col_ambiente:
        ranking_amb = (
            limpar_texto(df_filtrado[col_ambiente])
            .value_counts()
            .rename_axis("Ambiente")
            .reset_index(name="Chamados")
            .head(10)
        )
        st.bar_chart(ranking_amb.set_index("Ambiente"))
        st.dataframe(ranking_amb, use_container_width=True, hide_index=True)
    elif col_cidade:
        ranking_cid = (
            limpar_texto(df_filtrado[col_cidade])
            .value_counts()
            .rename_axis("Cidade")
            .reset_index(name="Chamados")
            .head(10)
        )
        st.bar_chart(ranking_cid.set_index("Cidade"))
        st.dataframe(ranking_cid, use_container_width=True, hide_index=True)
    else:
        st.info("Não encontrei coluna de ambiente ou cidade.")
    st.markdown('</div>', unsafe_allow_html=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("🧑‍🔧 Ranking de técnicos")
    if col_tecnico:
        ranking_tecnicos = (
            limpar_texto(df_filtrado[col_tecnico])
            .value_counts()
            .rename_axis("Técnico")
            .reset_index(name="Chamados")
            .head(10)
        )
        st.bar_chart(ranking_tecnicos.set_index("Técnico"))
        st.dataframe(ranking_tecnicos, use_container_width=True, hide_index=True)
    else:
        st.info("Não encontrei a coluna de técnico.")
    st.markdown('</div>', unsafe_allow_html=True)

with row2_col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("📌 Status dos chamados")
    if col_status:
        ranking_status = (
            limpar_texto(df_filtrado[col_status])
            .value_counts()
            .rename_axis("Status")
            .reset_index(name="Quantidade")
        )
        st.bar_chart(ranking_status.set_index("Status"))
        st.dataframe(ranking_status, use_container_width=True, hide_index=True)
    else:
        st.info("Não encontrei a coluna de status.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("🚨 Pontos com mais chamados")
if col_ponto:
    ranking_pontos = (
        limpar_texto(df_filtrado[col_ponto])
        .value_counts()
        .rename_axis("Ponto")
        .reset_index(name="Chamados")
        .head(15)
    )
    st.bar_chart(ranking_pontos.set_index("Ponto"))
    st.dataframe(ranking_pontos, use_container_width=True, hide_index=True)
else:
    st.info("Não encontrei a coluna de ponto.")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("📋 Base detalhada")
st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)
