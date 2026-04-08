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

def card(titulo, valor, subtitulo=""):
    st.markdown(
        f"""
        <div style="
            background:white;
            padding:18px;
            border-radius:18px;
            border:1px solid #e5e7eb;
            box-shadow:0 8px 24px rgba(15,23,42,0.06);
            min-height:124px;">
            <div style="font-size:14px;color:#6b7280;font-weight:600;margin-bottom:6px;">{titulo}</div>
            <div style="font-size:34px;font-weight:800;color:#111827;line-height:1.1;">{valor}</div>
            <div style="font-size:12px;color:#6b7280;margin-top:8px;">{subtitulo}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

df = carregar_dados()

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
div[data-testid="stDataFrame"] {border-radius: 14px; overflow: hidden;}
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

    st.markdown("### Base filtrada")
    st.write(f"**Registros:** {len(df_filtrado)}")
    st.write(f"**Colunas:** {len(df_filtrado.columns)}")

st.markdown(
    """
    <div style="
        padding:20px 22px;
        border-radius:22px;
        background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);
        color:white;
        box-shadow:0 10px 30px rgba(0,0,0,.14);
        margin-bottom:18px;">
        <div style="font-size:18px;font-weight:700;opacity:.9;">Painel operacional</div>
        <div style="font-size:42px;font-weight:800;line-height:1.05;margin-top:4px;">📊 Dashboard de Chamados</div>
        <div style="font-size:15px;color:#cbd5e1;margin-top:8px;">Atualizou a planilha, atualizou o painel. Sem gambiarra, sem retrabalho.</div>
    </div>
    """,
    unsafe_allow_html=True
)

status_aberto = ["aberto", "pendente", "em andamento", "novo"]
status_fechado = ["finalizado", "concluido", "concluído", "fechado", "encerrado"]

abertos = 0
fechados = 0
top_tecnico = "-"
top_qtd = 0
tempo_medio = None

if col_status:
    status_series = normalizar_texto(df_filtrado[col_status])
    abertos = status_series.isin(status_aberto).sum()
    fechados = status_series.isin(status_fechado).sum()

if col_tecnico:
    ranking = limpar_texto(df_filtrado[col_tecnico]).value_counts()
    if not ranking.empty:
        top_tecnico = ranking.index[0]
        top_qtd = int(ranking.iloc[0])

if col_duracao and df_filtrado[col_duracao].notna().any():
    tempo_medio = round(df_filtrado[col_duracao].dropna().mean(), 1)

cidade_top = "-"
cidade_top_qtd = 0
if col_cidade:
    ranking_cidade = limpar_texto(df_filtrado[col_cidade]).value_counts()
    if not ranking_cidade.empty:
        cidade_top = ranking_cidade.index[0]
        cidade_top_qtd = int(ranking_cidade.iloc[0])

c1, c2, c3, c4 = st.columns(4)
with c1:
    card("🔴 Chamados abertos", abertos, "Precisam de atenção")
with c2:
    card("🟢 Chamados fechados", fechados, "Resolvidos")
with c3:
    card("⚡ Tempo médio", f"{str(tempo_medio).replace('.', ',')} min" if tempo_medio is not None else "-", "Performance geral")
with c4:
    card("👑 Top técnico", top_tecnico, f"{top_qtd} chamados")

c5, c6, c7, c8 = st.columns(4)
with c5:
    card("🏙️ Cidade líder", cidade_top, f"{cidade_top_qtd} chamados")
with c6:
    pontos_unicos = df_filtrado[col_ponto].nunique() if col_ponto else 0
    card("🏢 Pontos únicos", pontos_unicos, "Locais atendidos")
with c7:
    tecnicos_unicos = df_filtrado[col_tecnico].nunique() if col_tecnico else 0
    card("🧰 Técnicos ativos", tecnicos_unicos, "Na base filtrada")
with c8:
    total_registros = len(df_filtrado)
    card("📦 Total filtrado", total_registros, "Chamados no recorte")

mes_atual = "-"
variacao_mensal_txt = "-"
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

st.markdown("---")
cc1, cc2 = st.columns([1.2, 1])

with cc1:
    st.subheader("📈 Evolução mensal")
    if "MesRef" in df_filtrado.columns and (df_filtrado["MesRef"] != "Sem data").any():
        evolucao = (
            df_filtrado[df_filtrado["MesRef"] != "Sem data"]["MesRef"]
            .value_counts()
            .sort_index()
            .rename_axis("Mês")
            .reset_index(name="Chamados")
        )
        st.caption(f"Último mês da base: {mes_atual} | {variacao_mensal_txt}")
        st.line_chart(evolucao.set_index("Mês"))
        st.dataframe(evolucao, use_container_width=True, hide_index=True)
    else:
        st.info("Não encontrei coluna de data válida para montar a evolução mensal.")

with cc2:
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

a1, a2 = st.columns(2)
with a1:
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

with a2:
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

st.subheader("📋 Base detalhada")
st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
