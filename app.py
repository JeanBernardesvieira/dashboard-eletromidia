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

def render_card(titulo, valor, subtitulo="", cor="#475569"):
    st.markdown(
        f"""
        <div style="
            background:#ffffff;
            border:1px solid #e5e7eb;
            border-left:6px solid {cor};
            border-radius:18px;
            padding:18px 18px 16px 18px;
            box-shadow:0 6px 18px rgba(15,23,42,0.06);
            min-height:126px;">
            <div style="font-size:14px;color:#64748b;font-weight:700;margin-bottom:8px;">{titulo}</div>
            <div style="font-size:30px;line-height:1.05;color:#0f172a;font-weight:900;word-break:break-word;">{valor}</div>
            <div style="font-size:12px;color:#64748b;margin-top:10px;">{subtitulo}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

df = carregar_dados()

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
.main > div {
    padding-top: 1rem;
}
.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}
div[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid #e5e7eb;
}
.section-title {
    font-size: 1.1rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 0.4rem;
}
.note {
    color: #64748b;
    font-size: 0.92rem;
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

    meses_validos = []
    if "MesRef" in df_filtrado.columns:
        meses_validos = sorted([x for x in df_filtrado["MesRef"].dropna().unique() if x not in ("NaT", "Sem data")])
        mes_sel = st.multiselect("Mês", meses_validos)
        if mes_sel:
            df_filtrado = df_filtrado[df_filtrado["MesRef"].isin(mes_sel)]

    st.markdown("### Base filtrada")
    st.write(f"**Registros:** {len(df_filtrado)}")
    st.write(f"**Colunas:** {len(df_filtrado.columns)}")

st.markdown(
    """
    <div style="
        padding:22px 24px;
        border-radius:24px;
        background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);
        color:white;
        box-shadow:0 12px 30px rgba(15,23,42,0.18);
        margin-bottom:18px;">
        <div style="font-size:13px;letter-spacing:.6px;text-transform:uppercase;color:#cbd5e1;font-weight:800;">
            Painel operacional
        </div>
        <div style="font-size:42px;line-height:1.05;font-weight:900;margin-top:6px;">
            📊 Dashboard de Chamados
        </div>
        <div style="font-size:15px;color:#e2e8f0;margin-top:10px;">
            Versão revisada com layout alinhado, cards equilibrados e leitura mais limpa.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Métricas principais
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

status_info = "Sem classificação de aberto/fechado"
abertos = None
fechados = None
contagem_status = pd.Series(dtype="int64")

if col_status:
    status_norm = normalizar_texto(df_filtrado[col_status]).fillna("")
    palavras_fechado = ["fechado", "finalizado", "finalizada", "concluido", "concluída", "encerrado", "encerrada", "resolvido", "resolvida", "ok"]
    palavras_aberto = ["aberto", "aberta", "pendente", "em andamento", "andamento", "novo", "nova", "aguardando", "atrasado", "atrasada", "na fila"]

    mask_fechado = status_norm.apply(lambda x: any(p in x for p in palavras_fechado))
    mask_aberto = status_norm.apply(lambda x: any(p in x for p in palavras_aberto))

    if mask_fechado.any() or mask_aberto.any():
        fechados = int(mask_fechado.sum())
        abertos = int(mask_aberto.sum())
        status_info = "Leitura automática por palavras-chave"
    contagem_status = limpar_texto(df_filtrado[col_status]).value_counts()

# Evolução mensal
mes_atual = "-"
chamados_mes_atual = "-"
variacao_mensal = "-"
evolucao = pd.DataFrame()

if "MesRef" in df_filtrado.columns:
    evolucao = (
        df_filtrado[df_filtrado["MesRef"].isin([x for x in df_filtrado["MesRef"].unique() if x not in ("NaT", "Sem data")])]["MesRef"]
        .value_counts()
        .sort_index()
        .rename_axis("Mês")
        .reset_index(name="Chamados")
    )
    if not evolucao.empty:
        mes_atual = str(evolucao.iloc[-1]["Mês"])
        chamados_mes_atual = int(evolucao.iloc[-1]["Chamados"])
        if len(evolucao) >= 2:
            anterior = int(evolucao.iloc[-2]["Chamados"])
            if anterior != 0:
                variacao = ((chamados_mes_atual - anterior) / anterior) * 100
                sinal = "+" if variacao >= 0 else ""
                variacao_mensal = f"{sinal}{variacao:.1f}%".replace(".", ",")
            else:
                variacao_mensal = "Sem base"
        else:
            variacao_mensal = "Primeiro mês"

# Cards linha 1
l1c1, l1c2, l1c3, l1c4 = st.columns(4)
with l1c1:
    if abertos is not None:
        render_card("🔴 Chamados abertos", abertos, status_info, "#dc2626")
    else:
        render_card("📦 Total de chamados", total_registros, "Base filtrada", "#475569")
with l1c2:
    if fechados is not None:
        render_card("🟢 Chamados fechados", fechados, status_info, "#16a34a")
    elif not contagem_status.empty:
        render_card("📌 Status principal", contagem_status.index[0], f"{int(contagem_status.iloc[0])} chamados", "#0ea5e9")
    else:
        render_card("📌 Status principal", "-", "Sem coluna útil", "#0ea5e9")
with l1c3:
    render_card("⚡ Tempo médio", f"{str(tempo_medio).replace('.', ',')} min" if tempo_medio is not None else "-", "Performance geral", "#2563eb")
with l1c4:
    render_card("👑 Top técnico", top_tecnico, f"{top_qtd} chamados", "#d97706")

# Cards linha 2
l2c1, l2c2, l2c3, l2c4 = st.columns(4)
with l2c1:
    render_card("🏙️ Cidade líder", cidade_top, f"{cidade_top_qtd} chamados", "#64748b")
with l2c2:
    render_card("🏢 Pontos únicos", pontos_unicos, "Locais atendidos", "#64748b")
with l2c3:
    render_card("🧰 Técnicos únicos", tecnicos_unicos, "Profissionais na base", "#64748b")
with l2c4:
    render_card("🌎 Cidades", cidades_unicas, "Cobertura da base", "#64748b")

# Cards executivos limpos
e1, e2, e3 = st.columns(3)
with e1:
    render_card("🗓️ Último mês da base", mes_atual, "Última competência encontrada", "#7c3aed")
with e2:
    render_card("📈 Chamados no mês atual", chamados_mes_atual, "Volume do último mês", "#7c3aed")
with e3:
    render_card("📊 Variação mensal", variacao_mensal, "Comparado ao mês anterior", "#7c3aed")

# Blocos analíticos
b1, b2 = st.columns([1.2, 1])
with b1:
    st.markdown('<div class="section-title">📈 Evolução mensal</div>', unsafe_allow_html=True)
    st.markdown('<div class="note">Volume de chamados por mês.</div>', unsafe_allow_html=True)
    if not evolucao.empty:
        st.line_chart(evolucao.set_index("Mês"))
        st.dataframe(evolucao, use_container_width=True, hide_index=True)
    else:
        st.info("Não encontrei coluna de data válida para montar a evolução mensal.")

with b2:
    st.markdown('<div class="section-title">🗺️ Ranking por ambiente / região</div>', unsafe_allow_html=True)
    st.markdown('<div class="note">Top 10 agrupamentos operacionais.</div>', unsafe_allow_html=True)
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

b3, b4 = st.columns(2)
with b3:
    st.markdown('<div class="section-title">🧑‍🔧 Ranking de técnicos</div>', unsafe_allow_html=True)
    st.markdown('<div class="note">Top 10 por quantidade de chamados.</div>', unsafe_allow_html=True)
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

with b4:
    st.markdown('<div class="section-title">📌 Status dos chamados</div>', unsafe_allow_html=True)
    st.markdown('<div class="note">Distribuição real de status da base.</div>', unsafe_allow_html=True)
    if col_status and not contagem_status.empty:
        ranking_status = contagem_status.rename_axis("Status").reset_index(name="Quantidade")
        st.bar_chart(ranking_status.set_index("Status"))
        st.dataframe(ranking_status, use_container_width=True, hide_index=True)
    else:
        st.info("Não encontrei a coluna de status.")

st.markdown('<div class="section-title">🚨 Pontos com mais chamados</div>', unsafe_allow_html=True)
st.markdown('<div class="note">Top 15 pontos com maior recorrência.</div>', unsafe_allow_html=True)
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

st.markdown('<div class="section-title">📋 Base detalhada</div>', unsafe_allow_html=True)
st.markdown('<div class="note">Tabela completa do recorte atual.</div>', unsafe_allow_html=True)
st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
