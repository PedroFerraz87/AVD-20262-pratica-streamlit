import altair as alt
import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_loader import load_data


st.set_page_config(
    page_title="Futebol Brasileiro | Análise de partidas",
    page_icon="⚽",
    layout="wide",
)

VARS_QUANT = [
    "home_goal",
    "away_goal",
    "home_corner",
    "away_corner",
    "home_attack",
    "away_attack",
    "home_shots",
    "away_shots",
    "ht_diff",
    "at_diff",
    "total_corners",
]
COLUNAS_OBRIGATORIAS = {
    "tournament",
    "home",
    "away",
    "home_goal",
    "away_goal",
    "date",
    "at_result",
    *VARS_QUANT,
}

st.title("Análise de partidas do futebol brasileiro")
st.caption(
    "Explore os resultados, as estatísticas das partidas e as relações entre "
    "as variáveis quantitativas."
)

df = load_data()
colunas_faltantes = COLUNAS_OBRIGATORIAS.difference(df.columns)
if colunas_faltantes:
    st.error(
        "O dataset não contém todas as colunas esperadas pela EDA: "
        + ", ".join(sorted(colunas_faltantes))
    )
    st.stop()

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["resultado_partida"] = "Indeterminado"
df.loc[df["home_goal"] > df["away_goal"], "resultado_partida"] = (
    "Vitória mandante"
)
df.loc[df["home_goal"] == df["away_goal"], "resultado_partida"] = "Empate"
df.loc[df["home_goal"] < df["away_goal"], "resultado_partida"] = (
    "Vitória visitante"
)

with st.sidebar:
    st.header("Filtros")

    torneios = sorted(df["tournament"].dropna().unique().tolist())
    torneios_selecionados = st.multiselect(
        "Torneios",
        options=torneios,
        default=torneios,
    )

    equipes = sorted(set(df["home"].dropna()) | set(df["away"].dropna()))
    equipe_selecionada = st.selectbox(
        "Equipe",
        options=["Todas as equipes", *equipes],
    )

    resultados = [
        "Todos",
        "Vitória mandante",
        "Empate",
        "Vitória visitante",
        "Indeterminado",
    ]
    resultado_selecionado = st.selectbox("Resultado", options=resultados)

    datas_validas = df["date"].dropna()
    if not datas_validas.empty:
        intervalo_datas = st.date_input(
            "Período",
            value=(datas_validas.min().date(), datas_validas.max().date()),
            min_value=datas_validas.min().date(),
            max_value=datas_validas.max().date(),
        )
    else:
        intervalo_datas = None

df_filtrado = df[df["tournament"].isin(torneios_selecionados)]
if equipe_selecionada != "Todas as equipes":
    df_filtrado = df_filtrado[
        (df_filtrado["home"] == equipe_selecionada)
        | (df_filtrado["away"] == equipe_selecionada)
    ]
if resultado_selecionado != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["resultado_partida"] == resultado_selecionado
    ]
if intervalo_datas:
    if isinstance(intervalo_datas, (tuple, list)) and len(intervalo_datas) == 2:
        data_inicio, data_fim = intervalo_datas
    else:
        data_inicio = data_fim = intervalo_datas
    df_filtrado = df_filtrado[
        df_filtrado["date"].dt.date.between(data_inicio, data_fim)
    ]

st.caption(
    f"{len(df_filtrado):,} de {len(df):,} partidas correspondem aos filtros."
)

aba_analise, aba_kpis = st.tabs(["Dashboard 1 · Análise", "Dashboard 2 · KPIs"])

with aba_analise:
    col_correlacao, col_distribuicao = st.columns([1, 1.2])

    with col_correlacao:
        st.subheader("Correlação entre variáveis quantitativas")
        variaveis = st.multiselect(
            "Variáveis para a matriz de correlação",
            options=VARS_QUANT,
            default=VARS_QUANT,
            key="variaveis_correlacao",
        )
        if len(variaveis) < 2:
            st.info("Selecione pelo menos duas variáveis para calcular correlações.")
        elif df_filtrado.empty:
            st.info("Não há partidas para os filtros selecionados.")
        else:
            matriz = df_filtrado[variaveis].corr(method="spearman")
            fig_correlacao = px.imshow(
                matriz,
                text_auto=".2f",
                aspect="auto",
                color_continuous_scale="RdBu_r",
                zmin=-1,
                zmax=1,
                labels={"color": "Correlação"},
            )
            fig_correlacao.update_layout(
                height=580,
                margin=dict(l=10, r=10, t=30, b=10),
            )
            st.plotly_chart(fig_correlacao, width="stretch")
            st.caption(
                "Correlação de Spearman; pares com valores ausentes são "
                "desconsiderados no cálculo."
            )

    with col_distribuicao:
        st.subheader("Distribuição das variáveis")
        variavel_distribuicao = st.selectbox(
            "Variável quantitativa",
            options=VARS_QUANT,
            key="variavel_distribuicao",
        )
        separar_resultado = st.checkbox(
            "Separar por resultado da partida",
            value=False,
        )
        if df_filtrado.empty:
            st.info("Não há partidas para os filtros selecionados.")
        else:
            fig_distribuicao = px.histogram(
                df_filtrado,
                x=variavel_distribuicao,
                color="resultado_partida" if separar_resultado else None,
                nbins=30,
                barmode="overlay" if separar_resultado else "relative",
                opacity=0.75 if separar_resultado else 1,
                labels={
                    variavel_distribuicao: variavel_distribuicao,
                    "count": "Partidas",
                    "resultado_partida": "Resultado",
                },
            )
            fig_distribuicao.update_layout(
                height=480,
                yaxis_title="Partidas",
                margin=dict(l=10, r=10, t=30, b=10),
            )
            st.plotly_chart(fig_distribuicao, width="stretch")

with aba_kpis:
    st.subheader("Indicadores das partidas filtradas")
    if df_filtrado.empty:
        st.info("Não há partidas para calcular indicadores com os filtros atuais.")
    else:
        total_partidas = len(df_filtrado)
        vitorias_mandante = (
            df_filtrado["resultado_partida"] == "Vitória mandante"
        ).mean()
        empates = (df_filtrado["resultado_partida"] == "Empate").mean()
        vitorias_visitante = (
            df_filtrado["resultado_partida"] == "Vitória visitante"
        ).mean()
        media_gols = (
            df_filtrado["home_goal"] + df_filtrado["away_goal"]
        ).mean()

        metrica_partidas, metrica_gols, metrica_mandante, metrica_empate, metrica_visitante = (
            st.columns(5)
        )
        metrica_partidas.metric("Partidas", f"{total_partidas:,}")
        metrica_gols.metric("Média de gols", f"{media_gols:.2f}")
        metrica_mandante.metric("Vitórias mandantes", f"{vitorias_mandante:.1%}")
        metrica_empate.metric("Empates", f"{empates:.1%}")
        metrica_visitante.metric(
            "Vitórias visitantes",
            f"{vitorias_visitante:.1%}",
        )

        col_resultados, col_torneios = st.columns(2)
        with col_resultados:
            st.subheader("Distribuição dos resultados")
            contagem_resultados = (
                df_filtrado["resultado_partida"]
                .value_counts()
                .rename_axis("Resultado")
                .reset_index(name="Partidas")
            )
            fig_resultados = px.pie(
                contagem_resultados,
                names="Resultado",
                values="Partidas",
                hole=0.4,
            )
            st.plotly_chart(fig_resultados, width="stretch")

        with col_torneios:
            st.subheader("Média de gols por torneio")
            gols_por_torneio = (
                df_filtrado.assign(
                    gols_partida=df_filtrado["home_goal"] + df_filtrado["away_goal"]
                )
                .groupby("tournament", as_index=False)
                .agg(
                    media_gols=("gols_partida", "mean"),
                    partidas=("gols_partida", "size"),
                )
                .sort_values("partidas", ascending=False)
                .head(10)
                .sort_values("media_gols")
            )
            fig_torneios = px.bar(
                gols_por_torneio,
                x="media_gols",
                y="tournament",
                orientation="h",
                text_auto=".2f",
                labels={
                    "media_gols": "Média de gols por partida",
                    "tournament": "Torneio",
                },
            )
            st.plotly_chart(fig_torneios, width="stretch")
