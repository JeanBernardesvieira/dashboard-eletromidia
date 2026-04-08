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

def render_card(titulo, valor, subtitulo="", borda="#64748b"):
    st.markdown(
        f"""
        <div style="
            background:white;
            border:1px solid #e5e7eb;
            border-left:6px solid {borda};
            border-radius:18px;
            padding:18px;
            box-shadow:0 8px 24px rgba(15,23,42,0.06);
            min-height:132px;">
            <div style="font-size:14px;color:#6b7280;font-weight:700;margin-bottom:8px;">{titulo}</div>
            <div style="font-size:34px;color:#0f172a;font-weight:900;line-height:1.05;">{valor}</div>
            <div style="font-size:12px;color:#64748b;margin-top:8px;">{subtitulo}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

df = carregar_dados()

# Descoberta de colunas
col_status = pegar_coluna(df, ["Status"])
col_tecnico = pegar_coluna(df, ["Técnico", "Tecnico"])
col_cidade = pegar_coluna(df, ["Cidade"])
col_ambiente = pegar_coluna(df, ["Ambiente", "Área de Trabalho", "Area de Trabalho", "Área", "Area"])
col_ponto = pegar_coluna(df, ["Ponto"])
col_duracao = pegar_coluna(df, ["Duração Exec. em minutos", "Duracao Exec. em minutos"])
col_data = pegar_coluna(df, [
    "Data de Criação", "Data de Criacao",
    "Data Criação", "Data Criacao",
    "Início do Serviço", "Inicio do Servico",
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
.block-container {padding-top: 1rem; padding-bottom: 2rem;}
div[data-testid="stDataFrame"] {border-radius: 16px; overflow: hidden; border: 1px solid #e5e7eb;}
div[data-testid="stMetric"] {background: white; border: 1px solid #e5e7eb; padding: 10px; border-radius: 16px;}
.section-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 22px;
    padding: 18px 18px 10px 18px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
    margin-bottom: 16px;
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
</style>
""", unsafe_allow_html=True)

# Filtros
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
        meses = sorted([x for x in df_filtrado["MesRef"].dropna().unique() if x != "NaT"])
        mes_sel = st.multiselect("Mês", meses)
        if mes_sel:
            df_filtrado = df_filtrado[df_filtrado["MesRef"].isin(mes_sel)]

    st.markdown("### Resumo da base")
    st.write(f"**Registros:** {len(df_filtrado)}")
    st.write(f"**Colunas:** {len(df_filtrado.columns)}")

# Métricas
total_registros = len(df_filtrado)
pontos_unicos = df_filtrado[col_ponto].nunique() if col_ponto else 0
tecnicos_unicos = df_filtrado[col_tecnico].nunique() if col_tecnico else 0
cidades_unicas = df_filtrado[col_cidade].nunique() if col_cidade else 0
tempo_medio = round(df_filtrado[col_duracao].dropna().mean(), 1) if col_duracao and df_filtrado[col_duracao].notna().any() else None

top_tecnico = "-"
top_qtd = 0
if col_tecnico:
    ranking = limpar_texto(df_filtrado[col_tecnico]).value_counts()
    if not ranking.empty:
        top_tecnico = ranking.index[0]
        top_qtd = int(ranking.iloc[0])

cidade_top = "-"
cidade_top_qtd = 0
if col_cidade:
    ranking_cidade = limpar_texto(df_filtrado[col_cidade]).value_counts()
    if not ranking_cidade.empty:
        cidade_top = ranking_cidade.index[0]
        cidade_top_qtd = int(ranking_cidade.iloc[0])

# Status robusto
abertos = None
fechados = None
status_info = "Sem coluna de status"

if col_status:
    status_norm = normalizar_texto(df_filtrado[col_status]).fillna("")
    palavras_fechado = [
        "fechado", "finalizado", "finalizada", "concluido", "concluída", "concluido",
        "encerrado", "encerrada", "resolvido", "resolvida", "ok"
    ]
    palavras_aberto = [
        "aberto", "aberta", "pendente", "em andamento", "andamento", "novo", "nova",
        "aguardando", "atrasado", "atrasada", "na fila"
    ]

    mask_fechado = status_norm.apply(lambda x: any(p in x for p in palavras_fechado))
    mask_aberto = status_norm.apply(lambda x: any(p in x for p in palavras_aberto))

    if mask_fechado.any() or mask_aberto.any():
        fechados = int(mask_fechado.sum())
        abertos = int(mask_aberto.sum())
        status_info = "Classificação automática por palavras-chave"
    else:
        contagem_status = limpar_texto(df_filtrado[col_status]).value_counts()
        status_info = "Status não bateu com aberto/fechado. Mostrando top status real da base."
else:
    contagem_status = pd.Series(dtype="int64")

# Comparativo mensal
mes_atual = "-"
variacao_mensal_txt = "-"
atual = None
anterior = None
evolucao = pd.DataFrame()

if "MesRef" in df_filtrado.columns and (df_filtrado["MesRef"] != "Sem data").any():
    evolucao = (
        df_filtrado[df_filtrado["MesRef"] != "Sem data"]["MesRef"]
        .value_counts()
        .sort_index()
        .rename_axis("Mês")
        .reset_index(name="Chamados")
    )
    if not evolucao.empty:
        mes_atual = evolucao.iloc[-1]["Mês"]
        atual = int(evolucao.iloc[-1]["Chamados"])
        if len(evolucao) >= 2:
            anterior = int(evolucao.iloc[-2]["Chamados"])
            if anterior != 0:
                variacao = ((atual - anterior) / anterior) * 100
                sinal = "+" if variacao >= 0 else ""
                variacao_mensal_txt = f"{sinal}{variacao:.1f}% vs mês anterior".replace(".", ",")
            else:
                variacao_mensal_txt = "Sem base de comparação"
        else:
            variacao_mensal_txt = "Primeiro mês da base"

st.markdown("""
<div class="hero">
    <div class="hero-top">Painel operacional restaurado</div>
    <div class="hero-title">📊 Dashboard de Chamados</div>
    <div class="hero-sub">Versão corrigida com layout completo, filtros, rankings e leitura mais robusta dos status.</div>
</div>
""", unsafe_allow_html=True)

# Linha 1
c1, c2, c3, c4 = st.columns(4)
with c1:
    if abertos is not None:
        render_card("🔴 Chamados abertos", abertos, status_info, "#dc2626")
    else:
        render_card("📦 Total de chamados", total_registros, "Base filtrada", "#475569")
with c2:
    if fechados is not None:
        render_card("🟢 Chamados fechados", fechados, status_info, "#16a34a")
    elif col_status and not contagem_status.empty:
        render_card("📌 Status principal", contagem_status.index[0], f"{int(contagem_status.iloc[0])} chamados", "#0ea5e9")
    else:
        render_card("🧰 Técnicos ativos", tecnicos_unicos, "Na base filtrada", "#475569")
with c3:
    render_card("⚡ Tempo médio", f"{str(tempo_medio).replace('.', ',')} min" if tempo_medio is not None else "-", "Performance geral", "#2563eb")
with c4:
    render_card("👑 Top técnico", top_tecnico, f"{top_qtd} chamados", "#d97706")

# Linha 2
c5, c6, c7, c8 = st.columns(4)
with c5:
    render_card("🏙️ Cidade líder", cidade_top, f"{cidade_top_qtd} chamados", "#64748b")
with c6:
    render_card("🏢 Pontos únicos", pontos_unicos, "Locais atendidos", "#64748b")
with c7:
    render_card("🧰 Técnicos únicos", tecnicos_unicos, "Profissionais na base", "#64748b")
with c8:
    render_card("🌎 Cidades", cidades_unicas, "Cobertura da base", "#64748b")

# Faixa executiva
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Último mês da base", mes_atual)
with m2:
    st.metric("Chamados no mês atual", atual if atual is not None else "-")
with m3:
    st.metric("Variação mensal", variacao_mensal_txt)

# Blocos
b1, b2 = st.columns([1.2, 1])

with b1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("📈 Evolução mensal")
    if not evolucao.empty:
        st.line_chart(evolucao.set_index("Mês"))
        st.dataframe(evolucao, use_container_width=True, hide_index=True)
    else:
        st.info("Não encontrei coluna de data válida para montar a evolução mensal.")
    st.markdown('</div>', unsafe_allow_html=True)

with b2:
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

b3, b4 = st.columns(2)

with b3:
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

with b4:
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
