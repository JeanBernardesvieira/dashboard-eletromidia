import math
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Dashboard de Chamados", page_icon="📊", layout="wide")

CSV_URL = "https://docs.google.com/spreadsheets/d/1vkBUlqKyquL6auioTkW_kNMvLqpRohgyCfHvV0viR58/export?format=csv&gid=1963619439"

@st.cache_data(ttl=300)
def carregar_dados():
    df = pd.read_csv(CSV_URL)
    return df

def pegar_coluna(df, nomes):
    mapa = {str(c).strip().lower(): c for c in df.columns}
    for nome in nomes:
        achada = mapa.get(nome.strip().lower())
        if achada:
            return achada
    return None

def formatar_numero(valor):
    try:
        if pd.isna(valor):
            return "-"
        if isinstance(valor, (int, float)):
            if float(valor).is_integer():
                return f"{int(valor):,}".replace(",", ".")
            return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return str(valor)
    except Exception:
        return str(valor)

def card(titulo, valor, subtitulo=""):
    st.markdown(
        f'''
        <div class="kpi-card">
            <div class="kpi-title">{titulo}</div>
            <div class="kpi-value">{valor}</div>
            <div class="kpi-subtitle">{subtitulo}</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

df = carregar_dados()

# Descoberta de colunas principais
col_tecnico = pegar_coluna(df, ["Técnico", "Tecnico"])
col_status = pegar_coluna(df, ["Status"])
col_cidade = pegar_coluna(df, ["Cidade"])
col_ponto = pegar_coluna(df, ["Ponto"])
col_duracao = pegar_coluna(df, ["Duração Exec. em minutos", "Duracao Exec. em minutos", "Duração Exec em minutos"])

if col_duracao:
    df[col_duracao] = pd.to_numeric(df[col_duracao], errors="coerce")

st.markdown(
    '''
    <style>
        .main > div {
            padding-top: 1.2rem;
        }
        .topo {
            padding: 1.1rem 1.25rem;
            border-radius: 20px;
            background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
            color: white;
            margin-bottom: 1rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }
        .topo h1 {
            margin: 0;
            font-size: 2.2rem;
        }
        .topo p {
            margin: 0.35rem 0 0 0;
            color: #d1d5db;
            font-size: 1rem;
        }
        .kpi-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 18px;
            padding: 18px 18px 16px 18px;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.07);
            min-height: 125px;
        }
        .kpi-title {
            font-size: 0.95rem;
            color: #6b7280;
            margin-bottom: 0.4rem;
            font-weight: 600;
        }
        .kpi-value {
            font-size: 2rem;
            font-weight: 800;
            color: #111827;
            line-height: 1.1;
            margin-bottom: 0.45rem;
        }
        .kpi-subtitle {
            font-size: 0.88rem;
            color: #6b7280;
        }
        .bloco {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 18px;
            padding: 1rem 1rem 0.6rem 1rem;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
            margin-top: 1rem;
        }
        div[data-testid="stDataFrame"] {
            border-radius: 14px;
            overflow: hidden;
        }
    </style>
    ''',
    unsafe_allow_html=True
)

with st.sidebar:
    st.header("Controles")
    if st.button("Atualizar dados"):
        st.cache_data.clear()
        st.rerun()
    st.info("Este painel lê os dados direto da planilha online.")
    st.markdown("### Base")
    st.write(f"**Registros:** {len(df)}")
    st.write(f"**Colunas:** {len(df.columns)}")

st.markdown(
    '''
    <div class="topo">
        <h1>📊 Dashboard de Chamados</h1>
        <p>Painel conectado direto ao Google Sheets. Atualizou a planilha, atualizou o painel.</p>
    </div>
    ''',
    unsafe_allow_html=True
)

total_registros = len(df)
tecnicos_unicos = df[col_tecnico].dropna().nunique() if col_tecnico else 0
cidades_unicas = df[col_cidade].dropna().nunique() if col_cidade else 0
tempo_medio = round(df[col_duracao].dropna().mean(), 1) if col_duracao and df[col_duracao].notna().any() else None
pontos_unicos = df[col_ponto].dropna().nunique() if col_ponto else 0
status_unicos = df[col_status].dropna().nunique() if col_status else 0

c1, c2, c3, c4 = st.columns(4)

with c1:
    card("Total de chamados", formatar_numero(total_registros), f"{formatar_numero(pontos_unicos)} pontos diferentes")
with c2:
    card("Técnicos únicos", formatar_numero(tecnicos_unicos), "Profissionais identificados na base")
with c3:
    card("Cidades", formatar_numero(cidades_unicas), f"{formatar_numero(status_unicos)} status encontrados")
with c4:
    card("Tempo médio", f"{str(tempo_medio).replace('.', ',')} min" if tempo_medio is not None else "-", "Baseado na duração em minutos")

col_a, col_b = st.columns([1, 1])

with col_a:
    st.markdown('<div class="bloco">', unsafe_allow_html=True)
    st.subheader("Top técnicos")
    if col_tecnico:
        ranking_tecnicos = (
            df[col_tecnico]
            .fillna("Não informado")
            .value_counts()
            .reset_index()
        )
        ranking_tecnicos.columns = ["Técnico", "Chamados"]
        st.bar_chart(ranking_tecnicos.set_index("Técnico"))
        st.dataframe(ranking_tecnicos.head(10), use_container_width=True, hide_index=True)
    else:
        st.warning("Não encontrei a coluna de técnico.")
    st.markdown('</div>', unsafe_allow_html=True)

with col_b:
    st.markdown('<div class="bloco">', unsafe_allow_html=True)
    st.subheader("Status dos chamados")
    if col_status:
        ranking_status = (
            df[col_status]
            .fillna("Não informado")
            .value_counts()
            .reset_index()
        )
        ranking_status.columns = ["Status", "Quantidade"]
        st.bar_chart(ranking_status.set_index("Status"))
        st.dataframe(ranking_status.head(10), use_container_width=True, hide_index=True)
    else:
        st.warning("Não encontrei a coluna de status.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="bloco">', unsafe_allow_html=True)
st.subheader("Visualização dos dados")
st.dataframe(df, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)
