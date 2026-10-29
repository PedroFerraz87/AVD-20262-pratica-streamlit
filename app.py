import altair as alt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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


def atualizar_selecao_kpi():
    estado_graficos = st.session_state.get("kpi_crossfilter", {})
    selecao = getattr(estado_graficos, "selection", None)
    if selecao is None and isinstance(estado_graficos, dict):
        selecao = estado_graficos.get("selection", {})
    st.session_state["kpi_selecao"] = selecao or {}


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

    variavel_intervalo = st.selectbox(
        "Variável para limitar por intervalo",
        options=VARS_QUANT,
        key="variavel_intervalo",
    )
    valores_intervalo = df[variavel_intervalo].dropna()
    minimo = float(valores_intervalo.min())
    maximo = float(valores_intervalo.max())
    valores_inteiros = valores_intervalo.mod(1).eq(0).all()
    if valores_inteiros:
        minimo, maximo, passo = int(minimo), int(maximo), 1
    else:
        passo = max(round((maximo - minimo) / 100, 2), 0.01)
    intervalo_numerico = st.slider(
        f"Intervalo de {variavel_intervalo}",
        min_value=minimo,
        max_value=maximo,
        value=(minimo, maximo),
        step=passo,
        help=(
            "Partidas sem valor para essa variável não entram no resultado "
            "enquanto o intervalo estiver aplicado."
        ),
        key=f"intervalo_numerico_{variavel_intervalo}",
    )

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
df_filtrado = df_filtrado[
    df_filtrado[variavel_intervalo].between(*intervalo_numerico)
]
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
            valores = matriz.to_numpy()
            textos = [
                [
                    f"{valor:.2f}"
                    if linha > coluna and pd.notna(valor)
                    else ""
                    for coluna, valor in enumerate(valores_linha)
                ]
                for linha, valores_linha in enumerate(valores)
            ]
            fig_correlacao = go.Figure(
                data=go.Heatmap(
                    z=valores,
                    x=matriz.columns,
                    y=matriz.index,
                    text=textos,
                    texttemplate="%{text}",
                    colorscale="RdBu",
                    zmin=-1,
                    zmax=1,
                    colorbar={"title": "Correlação"},
                    hovertemplate=(
                        "%{y} × %{x}<br>Correlação: %{z:.2f}<extra></extra>"
                    ),
                )
            )
            fig_correlacao.update_layout(
                height=580,
                margin=dict(l=10, r=10, t=30, b=10),
            )
            fig_correlacao.update_yaxes(autorange="reversed")
            st.plotly_chart(fig_correlacao, width="stretch")
            st.caption(
                "Correlação de Spearman; pares com valores ausentes são "
                "desconsiderados no cálculo."
            )

    with col_distribuicao:
        st.subheader("Distribuição das variáveis")
        variaveis_distribuicao = st.multiselect(
            "Variáveis quantitativas",
            options=VARS_QUANT,
            default=["home_goal", "away_goal"],
            key="variaveis_distribuicao",
        )
        separar_resultado = st.checkbox(
            "Separar por resultado da partida",
            value=False,
        )
        if not variaveis_distribuicao:
            st.info("Selecione pelo menos uma variável para exibir os histogramas.")
        elif df_filtrado.empty:
            st.info("Não há partidas para os filtros selecionados.")
        else:
            for inicio in range(0, len(variaveis_distribuicao), 2):
                colunas_graficos = st.columns(2)
                for coluna, variavel in zip(
                    colunas_graficos,
                    variaveis_distribuicao[inicio : inicio + 2],
                ):
                    with coluna:
                        fig_distribuicao = px.histogram(
                            df_filtrado,
                            x=variavel,
                            color="resultado_partida" if separar_resultado else None,
                            nbins=30,
                            barmode="overlay" if separar_resultado else "relative",
                            opacity=0.75 if separar_resultado else 1,
                            labels={
                                variavel: variavel,
                                "count": "Partidas",
                                "resultado_partida": "Resultado",
                            },
                            title=variavel,
                        )
                        fig_distribuicao.update_layout(
                            height=340,
                            showlegend=separar_resultado,
                            yaxis_title="Partidas",
                            margin=dict(l=10, r=10, t=45, b=10),
                        )
                        st.plotly_chart(fig_distribuicao, width="stretch")

with aba_kpis:
    st.subheader("Indicadores das partidas filtradas")
    if df_filtrado.empty:
        st.info("Não há partidas para calcular indicadores com os filtros atuais.")
    else:
        selecao = st.session_state.get("kpi_selecao", {})
        resultados_selecionados = [
            item["resultado_partida"]
            for item in selecao.get("resultado", [])
            if "resultado_partida" in item
        ]
        torneios_selecionados_no_grafico = [
            item["tournament"]
            for item in selecao.get("torneio", [])
            if "tournament" in item
        ]

        df_kpis = df_filtrado
        if resultados_selecionados:
            df_kpis = df_kpis[
                df_kpis["resultado_partida"].isin(resultados_selecionados)
            ]
        if torneios_selecionados_no_grafico:
            df_kpis = df_kpis[
                df_kpis["tournament"].isin(torneios_selecionados_no_grafico)
            ]

        if df_kpis.empty:
            st.info(
                "A combinação das seleções dos gráficos não contém partidas. "
                "Limpe uma das seleções para ver os indicadores."
            )
        else:
            st.caption(
                "Clique nas barras para filtrar os indicadores e os outros "
                "gráficos. Use Shift+clique para selecionar mais de uma categoria; "
                "clique duas vezes para limpar a seleção."
            )
            total_partidas = len(df_kpis)
            partidas_com_resultado = df_kpis[
                df_kpis["resultado_partida"].isin(
                    [
                        "Vitória mandante",
                        "Empate",
                        "Vitória visitante",
                    ]
                )
            ]
            total_com_resultado = len(partidas_com_resultado)
            if total_com_resultado:
                vitorias_mandante = (
                    partidas_com_resultado["resultado_partida"]
                    == "Vitória mandante"
                ).mean()
                empates = (
                    partidas_com_resultado["resultado_partida"] == "Empate"
                ).mean()
                vitorias_visitante = (
                    partidas_com_resultado["resultado_partida"]
                    == "Vitória visitante"
                ).mean()
                taxa_mandante = f"{vitorias_mandante:.1%}"
                taxa_empate = f"{empates:.1%}"
                taxa_visitante = f"{vitorias_visitante:.1%}"
            else:
                taxa_mandante = taxa_empate = taxa_visitante = "—"
            media_gols = (
                df_kpis["home_goal"] + df_kpis["away_goal"]
            ).mean()

            (
                metrica_partidas,
                metrica_gols,
                metrica_mandante,
                metrica_empate,
                metrica_visitante,
            ) = st.columns(5)
            metrica_partidas.metric("Partidas", f"{total_partidas:,}")
            metrica_gols.metric("Média de gols", f"{media_gols:.2f}")
            metrica_mandante.metric(
                "Vitórias mandantes",
                taxa_mandante,
            )
            metrica_empate.metric("Empates", taxa_empate)
            metrica_visitante.metric(
                "Vitórias visitantes",
                taxa_visitante,
            )

            dados_graficos = df_filtrado.assign(
                gols_partida=df_filtrado["home_goal"] + df_filtrado["away_goal"],
                ano=df_filtrado["date"].dt.year,
            )
            selecao_resultado = alt.selection_point(
                name="resultado",
                fields=["resultado_partida"],
            )
            selecao_torneio = alt.selection_point(
                name="torneio",
                fields=["tournament"],
            )
            grafico_resultados = (
                alt.Chart(dados_graficos)
                .transform_filter(selecao_torneio)
                .mark_bar()
                .encode(
                    x=alt.X(
                        "resultado_partida:N",
                        title="Resultado",
                        sort=[
                            "Vitória mandante",
                            "Empate",
                            "Vitória visitante",
                            "Indeterminado",
                        ],
                    ),
                    y=alt.Y("count():Q", title="Partidas"),
                    color=alt.Color(
                        "resultado_partida:N",
                        title="Resultado",
                        scale=alt.Scale(scheme="tableau10"),
                    ),
                    opacity=alt.condition(
                        selecao_resultado,
                        alt.value(1),
                        alt.value(0.35),
                    ),
                    tooltip=[
                        alt.Tooltip("resultado_partida:N", title="Resultado"),
                        alt.Tooltip("count():Q", title="Partidas"),
                    ],
                )
                .add_params(selecao_resultado)
                .properties(
                    title="Partidas por resultado",
                    width=300,
                    height=320,
                )
            )
            grafico_torneios = (
                alt.Chart(dados_graficos)
                .transform_filter(selecao_resultado)
                .mark_bar()
                .encode(
                    y=alt.Y(
                        "tournament:N",
                        title="Torneio",
                        sort="-x",
                    ),
                    x=alt.X(
                        "mean(gols_partida):Q",
                        title="Média de gols por partida",
                    ),
                    color=alt.condition(
                        selecao_torneio,
                        alt.value("#c1121f"),
                        alt.value("#c9cdd4"),
                    ),
                    tooltip=[
                        alt.Tooltip("tournament:N", title="Torneio"),
                        alt.Tooltip(
                            "mean(gols_partida):Q",
                            title="Média de gols",
                            format=".2f",
                        ),
                        alt.Tooltip("count():Q", title="Partidas"),
                    ],
                )
                .add_params(selecao_torneio)
                .properties(
                    title="Média de gols por torneio",
                    width=420,
                    height=320,
                )
            )
            grafico_tendencia_gols = (
                alt.Chart(dados_graficos)
                .transform_filter(selecao_resultado)
                .transform_filter(selecao_torneio)
                .mark_line(point=True)
                .encode(
                    x=alt.X("ano:O", title="Ano", sort="ascending"),
                    y=alt.Y(
                        "mean(gols_partida):Q",
                        title="Média de gols por partida",
                    ),
                    tooltip=[
                        alt.Tooltip("ano:O", title="Ano"),
                        alt.Tooltip(
                            "mean(gols_partida):Q",
                            title="Média de gols",
                            format=".2f",
                        ),
                        alt.Tooltip("count():Q", title="Partidas"),
                    ],
                )
                .properties(
                    title="Evolução da média de gols por ano",
                    width=760,
                    height=260,
                )
            )
            st.altair_chart(
                (grafico_resultados | grafico_torneios) & grafico_tendencia_gols,
                key="kpi_crossfilter",
                on_select=atualizar_selecao_kpi,
                width="stretch",
            )
