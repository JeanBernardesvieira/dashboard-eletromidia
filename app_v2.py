import pandas as pd
import streamlit as st

st.set_page_config(page_title="Dashboard de Chamados", page_icon="📊", layout="wide")

CSV_URL = "https://docs.google.com/spreadsheets/d/1vkBUlqKyquL6auioTkW_kNMvLqpRohgyCfHvV0viR58/export?format=csv&gid=1963619439"

@st.cache_data(ttl=300)
def carregar_dados():
    try:
        return pd.read_csv(CSV_URL)
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

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

def card_html(titulo, valor, subtitulo="", cor="#475569", icone="📊"):
    # Lógica de variação (exemplo simples: se contiver '%' e for positivo, verde; se negativo, vermelho)
    sub_style = ""
    if "%" in str(valor) or "%" in str(subtitulo):
        if "+" in str(valor) or "+" in str(subtitulo):
            sub_style = "color: #10b981; font-weight: bold;"
        elif "-" in str(valor) or "-" in str(subtitulo):
            sub_style = "color: #ef4444; font-weight: bold;"

    return f"""
    <div class="jg-card">
        <div class="jg-card-header">
            <span class="jg-card-icon" style="background-color: {cor}20; color: {cor};">{icone}</span>
            <div class="jg-card-title">{titulo}</div>
        </div>
        <div class="jg-card-body">
            <div class="jg-card-value" style="color: {cor};">{valor}</div>
            <div class="jg-card-sub" style="{sub_style}">{subtitulo}</div>
        </div>
        <div class="jg-card-footer" style="background-color: {cor};"></div>
    </div>
    """

df = carregar_dados()

if df.empty:
    st.warning("A base de dados está vazia ou não pôde ser carregada.")
    st.stop()

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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #f8fafc;
    }

    .main > div {padding-top: 1rem;}
    .block-container {padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1600px;}
    
    /* Grid System */
    .jg-grid {
        display: grid;
        gap: 20px;
        margin-bottom: 25px;
        width: 100%;
    }
    .jg-grid-4 { grid-template-columns: repeat(4, 1fr); }
    .jg-grid-3 { grid-template-columns: repeat(3, 1fr); }

    /* Card Design */
    .jg-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 20px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border: 1px solid #f1f5f9;
        position: relative;
        overflow: hidden;
        min-height: 160px;
    }
    
    .jg-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }

    .jg-card-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 15px;
    }

    .jg-card-icon {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }

    .jg-card-title {
        font-size: 13px;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .jg-card-value {
        font-size: 32px;
        color: #1e293b;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 6px;
    }

    .jg-card-sub {
        font-size: 13px;
        color: #94a3b8;
        font-weight: 500;
    }

    .jg-card-footer {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 4px;
        opacity: 0.6;
    }

    /* Section Titles */
    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1e293b;
        margin: 2rem 0 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .note { color: #64748b; font-size: 0.9rem; margin-bottom: 1.5rem; }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #f1f5f9; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

    /* Responsive */
    @media (max-width: 1200px) {
        .jg-grid-4 { grid-template-columns: repeat(2, 1fr); }
        .jg-grid-3 { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 768px) {
        .jg-grid-4, .jg-grid-3 { grid-template-columns: 1fr; }
    }
</style>
""", unsafe_allow_html=True)

df_filtrado = df.copy()

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1055/1055644.png", width=80)
    st.title("Filtros")
    
    if st.button("🔄 Atualizar Dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.divider()

    if col_tecnico:
        tecnicos = sorted([x for x in limpar_texto(df[col_tecnico].dropna()).unique() if x and x.lower() != "nan"])
        tecnico_sel = st.multiselect("👤 Técnico", tecnicos)
        if tecnico_sel:
            df_filtrado = df_filtrado[limpar_texto(df_filtrado[col_tecnico]).isin(tecnico_sel)]

    if col_cidade:
        cidades = sorted([x for x in limpar_texto(df[col_cidade].dropna()).unique() if x and x.lower() != "nan"])
        cidade_sel = st.multiselect("🏙️ Cidade", cidades)
        if cidade_sel:
            df_filtrado = df_filtrado[limpar_texto(df_filtrado[col_cidade]).isin(cidade_sel)]

    if col_status:
        status_opcoes = sorted([x for x in limpar_texto(df[col_status].dropna()).unique() if x and x.lower() != "nan"])
        status_sel = st.multiselect("📌 Status", status_opcoes)
        if status_sel:
            df_filtrado = df_filtrado[limpar_texto(df_filtrado[col_status]).isin(status_sel)]

    if "MesRef" in df_filtrado.columns:
        meses_validos = sorted([x for x in df_filtrado["MesRef"].dropna().unique() if x not in ("NaT", "Sem data")])
        mes_sel = st.multiselect("📅 Mês", meses_validos)
        if mes_sel:
            df_filtrado = df_filtrado[df_filtrado["MesRef"].isin(mes_sel)]

    st.divider()
    st.markdown("### 📊 Resumo do Filtro")
    c1, c2 = st.columns(2)
    c1.metric("Registros", len(df_filtrado))
    c2.metric("Colunas", len(df_filtrado.columns))

# Header principal
st.markdown(
    """
    <div style="
        padding: 30px;
        border-radius: 20px;
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin-bottom: 30px;
        border: 1px solid rgba(255,255,255,0.1);">
        <div style="font-size: 12px; letter-spacing: 2px; text-transform: uppercase; color: #94a3b8; font-weight: 700; margin-bottom: 8px;">
            Operações em Tempo Real
        </div>
        <h1 style="font-size: 36px; font-weight: 800; margin: 0; color: white; border: none;">
            📊 Dashboard de Chamados
        </h1>
        <p style="font-size: 16px; color: #cbd5e1; margin-top: 12px; opacity: 0.9;">
            Análise detalhada de performance, status e volumetria da base operacional.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Cálculos
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

abertos = 0
fechados = 0
if col_status:
    status_norm = normalizar_texto(df_filtrado[col_status]).fillna("")
    palavras_fechado = ["fechado", "finalizado", "finalizada", "concluido", "concluída", "encerrado", "encerrada", "resolvido", "resolvida", "ok"]
    palavras_aberto = ["aberto", "aberta", "pendente", "em andamento", "andamento", "novo", "nova", "aguardando", "atrasado", "atrasada", "na fila"]
    fechados = int(status_norm.apply(lambda x: any(p in x for p in palavras_fechado)).sum())
    abertos = int(status_norm.apply(lambda x: any(p in x for p in palavras_aberto)).sum())

mes_atual = "-"
chamados_mes_atual = 0
variacao_mensal = "0%"
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
                variacao_mensal = f"{sinal}{variacao:.1f}%"
            else:
                variacao_mensal = "Novo"

# Renderização dos Cards
st.markdown('<div class="section-title">📌 Indicadores Principais</div>', unsafe_allow_html=True)

c1_html = card_html("Chamados Abertos", abertos, "Pendentes de ação", "#ef4444", "🔴")
c2_html = card_html("Chamados Fechados", fechados, "Concluídos com sucesso", "#10b981", "🟢")
c3_html = card_html("Tempo Médio", f"{str(tempo_medio).replace('.', ',')}m" if tempo_medio else "-", "Minutos por chamado", "#3b82f6", "⚡")
c4_html = card_html("Variação Mensal", variacao_mensal, f"Vs. mês anterior", "#8b5cf6", "📈")

st.markdown(f'<div class="jg-grid jg-grid-4">{c1_html}{c2_html}{c3_html}{c4_html}</div>', unsafe_allow_html=True)

c5_html = card_html("Top Técnico", top_tecnico, f"{top_qtd} atendimentos", "#f59e0b", "👑")
c6_html = card_html("Cidade Líder", cidade_top, f"{cidade_top_qtd} chamados", "#64748b", "🏙️")
c7_html = card_html("Pontos Únicos", pontos_unicos, "Locais atendidos", "#06b6d4", "🏢")
c8_html = card_html("Total Geral", total_registros, "Volume total da base", "#1e293b", "📦")

st.markdown(f'<div class="jg-grid jg-grid-4">{c5_html}{c6_html}{c7_html}{c8_html}</div>', unsafe_allow_html=True)

# Gráficos
st.markdown('<div class="section-title">📈 Análise de Tendências e Distribuição</div>', unsafe_allow_html=True)

g1, g2 = st.columns([1.5, 1], gap="large")

with g1:
    st.markdown('<div class="note">Evolução temporal de chamados</div>', unsafe_allow_html=True)
    if not evolucao.empty:
        st.line_chart(evolucao.set_index("Mês"), color="#3b82f6")
    else:
        st.info("Dados insuficientes para evolução mensal.")

with g2:
    st.markdown('<div class="note">Top 10 Ambientes/Áreas</div>', unsafe_allow_html=True)
    if col_ambiente:
        ranking_amb = limpar_texto(df_filtrado[col_ambiente]).value_counts().head(10)
        st.bar_chart(ranking_amb, color="#64748b")
    else:
        st.info("Coluna de ambiente não encontrada.")

# Tabelas e Rankings
st.markdown('<div class="section-title">📋 Detalhamento Operacional</div>', unsafe_allow_html=True)

t1, t2 = st.columns(2, gap="large")

with t1:
    st.subheader("🧑‍🔧 Top 10 Técnicos")
    if col_tecnico:
        rt = limpar_texto(df_filtrado[col_tecnico]).value_counts().head(10).rename_axis("Técnico").reset_index(name="Qtd")
        st.dataframe(rt, use_container_width=True, hide_index=True)

with t2:
    st.subheader("📍 Top 10 Pontos")
    if col_ponto:
        rp = limpar_texto(df_filtrado[col_ponto]).value_counts().head(10).rename_axis("Ponto").reset_index(name="Qtd")
        st.dataframe(rp, use_container_width=True, hide_index=True)

st.divider()
with st.expander("🔍 Visualizar Base de Dados Completa"):
    st.dataframe(df_filtrado, use_container_width=True)
