from dash import Dash, html, dcc, Input, Output, dash
import dash_bootstrap_components as dbc
import pandas as pd
from plotly import express as px
import plotly.graph_objects as go
from datetime import datetime
import dash_mantine_components as dmc
from dash_bootstrap_templates import ThemeSwitchAIO

# tratamento dos dados
df = pd.read_csv(r"sales_dataset.csv")
df["Valor Pago"] = df["Valor Pago"].str.lstrip("R$ ").astype(int)
meses_ordem = [
    "Jan",
    "Fev",
    "Mar",
    "Abr",
    "Mai",
    "Jun",
    "Jul",
    "Ago",
    "Set",
    "Out",
    "Nov",
    "Dez",
]
df["Ano"] = 2023
meses = {
    "Jan": 1,
    "Fev": 2,
    "Mar": 3,
    "Abr": 4,
    "Mai": 5,
    "Jun": 6,
    "Jul": 7,
    "Ago": 8,
    "Set": 9,
    "Out": 10,
    "Nov": 11,
    "Dez": 12,
}
df["Mês_"] = df["Mês"].map(lambda x: meses[x]).astype(int)
df["Data"] = pd.to_datetime(
    df[["Ano", "Mês_", "Dia"]].rename(
        columns={"Ano": "year", "Mês_": "month", "Dia": "day"}
    )
)
data_antiga = df["Data"].min()
data_nova = df["Data"].max()
status = {"Pago": 1, "Não pago": 0}
df["Status de Pagamento"] = (
    df["Status de Pagamento"].map(lambda x: status[x]).astype(int)
)
df["Mês"] = pd.Categorical(df["Mês"], categories=meses_ordem, ordered=True)

dict_cores_ad = {
    "Facebook": "#002fff",
    "Google Ad": "#fbff00",
    "Website": "#f700ff",
    "Televisão": "#ffae00",
    "WhatsApp": "#1eff00",
    "Youtube": "#ff0000",
}

config_graph = {"showTips": False, "displayModeBar": False}

template_theme_dark = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "font": {"color": "rgb(255, 255, 255)"},
    "plot_bgcolor": "#191919",
}

template_theme_light = {
    "paper_bgcolor": "rgba(255,255,255,0)",
    "font": {"color": "rgb(0, 0, 0)"},
    "plot_bgcolor": "#d6d6d6",
}


axes_theme_dark = {
    "mirror": True,
    "ticks": "outside",
    "showline": True,
    "gridcolor": "black",
    "linecolor": "white",
    "linewidth": 1,
}

axes_theme_light = {
    "mirror": True,
    "ticks": "outside",
    "showline": True,
    "gridcolor": "white",
    "linecolor": "black",
    "linewidth": 2,
}

dash._dash_renderer._set_react_version("18.2.0")
app = Dash(
    __name__,
    external_stylesheets=[
        dbc.icons.BOOTSTRAP,
        "https://unpkg.com/@mantine/dates@7/styles.css",
    ],
)

filtro_ad = html.Div(
    [
        html.Span(["Filtrar Propagandas"], className="filtro_title"),
        dcc.Checklist(options=[
                {
                    "label": [
                        html.Img(src="/assets/facebook.svg", className="imagem_check"),
                        html.Span(
                            "Facebook", style={"fontSize": 15, "paddingLeft": 10}
                        ),
                    ],
                    "value": "Facebook"
                },
                {
                    "label": [
                        html.Img(
                            src="/assets/website.svg", className="imagem_check"
                        ),
                        html.Span("Website", style={"fontSize": 15, "paddingLeft": 10}),
                    ],
                    "value": "Website",
                },
                {
                    "label": [
                        html.Img(src="/assets/google.svg", className="imagem_check"),
                        html.Span(
                            "Google Ad", style={"fontSize": 15, "paddingLeft": 10}
                        ),
                    ],
                    "value": "Google Ad",
                },
                {
                    "label": [
                        html.Img(src="/assets/Televisão.svg", className="imagem_check"),
                        html.Span(
                            "Televisão", style={"fontSize": 15, "paddingLeft": 10}
                        ),
                    ],
                    "value": "televisão",
                },
                {
                    "label": [
                        html.Img(src="/assets/whatsapp.svg", className="imagem_check"),
                        html.Span(
                            "WhatsApp", style={"fontSize": 15, "paddingLeft": 10}
                        ),
                    ],
                    "value": "WhatsApp",
                },
                {
                    "label": [
                        html.Img(src="/assets/youtube.svg", className="imagem_check"),
                        html.Span("Youtube", style={"fontSize": 15, "paddingLeft": 10}),
                    ],
                    "value": "Youtube",
                },
            ],
            labelStyle={"display": "flex", "alignItems": "center"},
            className="checklist",
            id="ad_check",
        ),
    ],
    className="container_ad",
)

filtro_equipe = html.Div(
    [
        html.Span(["Filtrar Equipes"], className="filtro_title"),
        dcc.Checklist(
            options=["Todas", "Equipe 1", "Equipe 2", "Equipe 3", "Equipe 4"],
            inline=True,
            value=["Todas"],
            className="checklist",
            id="equipe_check",
        ),
    ],
    className="cont_drop",
)

theme_switch = html.Div(
    [
        ThemeSwitchAIO(
            aio_id="theme",
            themes=["/assets/dark-theme.css", "/assets/light-theme.css"],
            icons={"left": "bi bi-sun", "right": "bi bi-moon"},
        )
    ],
    className="theme-div",
)

filtro_meses = dmc.MantineProvider(
    [
        html.Div(
            [
                dmc.DatePicker(
                    id="date-input-range-picker",
                    label="Selecionar Período",
                    valueFormat="DD-MM-YYYY",
                    labelSeparator="até",
                    minDate=data_antiga,
                    type="range",
                    maxDate=data_nova,
                    numberOfColumns=2,
                    value=[data_antiga, data_nova],
                    w=200,
                    className="filtro_meses",
                    dropdownType="modal",
                    modalProps={"zIndex": 2000},
                )
            ]
        )
    ]
)
app.layout = html.Div(
    [
        # sidebar
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [html.I(className="bi bi-chevron-double-right")],
                            className="icone_container",
                        ),
                        html.Div(
                            [
                                theme_switch,
                                html.Div(
                                    [filtro_meses],
                                    className="filtro",
                                    style={"position": "relative", "top": "-23px"},
                                ),
                                html.Div([filtro_equipe], className="filtro"),
                                html.Div([filtro_ad], className="filtro"),
                            ],
                            className="content",
                        ),
                    ]
                )
            ],
            className="coluna",
            id="coluna-id",
        ),
        # conteudo da pagina 8 graphics
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(
                                    className="graph", config=config_graph, id="graph1"
                                )
                            ],
                            className="col1",
                            style={"height": "fit-content"},
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    id="graph2", className="graph", config=config_graph
                                )
                            ],
                            style={"height": "fit-content"},
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dbc.Card(
                                            [
                                                dcc.Graph(
                                                    style={"height": "180px"},
                                                    config=config_graph,
                                                    id="graph3",
                                                )
                                            ],
                                            className="card",
                                        ),
                                        dbc.Card(
                                            [
                                                dcc.Graph(
                                                    style={"height": "175px"},
                                                    config=config_graph,
                                                    id="graph4",
                                                )
                                            ],
                                            className="card",
                                            style={"marginTop": "9px"},
                                        ),
                                    ],
                                    style={"height": "fit-content"},
                                )
                            ],
                            style={"height": "fit-content"},
                        ),
                    ],
                    className="pag_content",
                ),
                # 2row
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(
                                    id="graph5", className="graph", config=config_graph
                                )
                            ]
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    id="graph6", className="graph", config=config_graph
                                )
                            ]
                        ),
                        html.Div(
                            [
                                dbc.Card(
                                    [
                                        dcc.Graph(
                                            id="graph7",
                                            style={"height": "143px"},
                                            config=config_graph,
                                        )
                                    ],
                                    className="card2",
                                    style={"marginTop": "5px"},
                                ),
                                dbc.Card(
                                    [
                                        dcc.Graph(
                                            id="graph8",
                                            style={"height": "155px"},
                                            config=config_graph,
                                        )
                                    ],
                                    className="card2",
                                    style={"marginTop": "7px"},
                                ),
                            ]
                        ),
                    ],
                    className="pag_content",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(
                                    id="graph9", className="graph", config=config_graph
                                )
                            ]
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    id="graph10", className="graph", config=config_graph
                                )
                            ]
                        ),
                    ],
                    className="pag_content",
                ),
            ]
        ),
        dcc.Store(id="store-date"),
    ],
    className="pagina",
    id="pagina_",
)

    
    
@app.callback(
    [
        Output(component_id="graph1", component_property="figure"),
        Output(component_id="graph2", component_property="figure"),
        Output(component_id="graph3", component_property="figure"),
        Output(component_id="graph4", component_property="figure"),
        Output(component_id="graph5", component_property="figure"),
        Output(component_id="graph6", component_property="figure"),
        Output(component_id="graph7", component_property="figure"),
        Output(component_id="graph8", component_property="figure"),
        Output(component_id="graph9", component_property="figure"),
        Output(component_id="graph10", component_property="figure"),
    ],
    [
        Input(component_id="equipe_check", component_property="value"),
        Input(component_id="ad_check", component_property="value"),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
        Input(component_id="date-input-range-picker", component_property="value"),
    ],
)
def filtro(equipe, propaganda, theme, periodo):
    
    if None in periodo or periodo is None:
        return dash.no_update
    data_inicio = datetime.fromisoformat(periodo[0])
    data_final = datetime.fromisoformat(periodo[1])

    if data_inicio.month == data_final.month and data_inicio.year == data_final.year:
        axis_x = "Dia"
        title = f'Valores para {data_inicio.strftime("%B %Y")}'
        number_to_month = {}
    else:
        axis_x = "Mês_"
        title = "Valores por Mês"
        number_to_month = dict(
            xaxis=dict(
                tickmode="array", tickvals=list(range(1, 13)), ticktext=meses_ordem
            )
        )

    if theme:
        template = template_theme_dark
        axes_theme = axes_theme_dark
    else:
        template = template_theme_light
        axes_theme = axes_theme_light

    dff = df.copy()

    if "Todas" not in equipe and equipe:
        dff = dff[dff["Equipe"].isin(equipe)]

    if propaganda:
        dff = dff[dff["Meio de Propaganda"].isin(propaganda)]

    dff = dff[(dff["Data"] >= data_inicio) & (dff["Data"] <= data_final)]


    fig = px.histogram(
        dff,
        x="Valor Pago",
        y="Equipe",
        barmode="group",
        orientation="h",
        text_auto=True,
    )
    fig.update_layout(
        {"margin": {"l": 0, "r": 30, "t": 30, "b": 0}},
        height=320,
        xaxis_title="",
        yaxis_title="",
    )
    fig.update_layout(template)
    fig.update_xaxes(axes_theme)
    fig.update_yaxes(axes_theme)

    # segundo grafico   chamada por propaganda

    fig10 = px.histogram(
        dff,
        x="Chamadas Realizadas",
        y="Meio de Propaganda",
        barmode="group",
        text_auto=True,
    )
    fig10.update_layout(
        {"margin": {"l": 0, "r": 30, "t": 30, "b": 0}},
        height=320,
        xaxis_title="",
        yaxis_title="",
        legend_itemclick="toggleothers",
    )
    fig10.update_layout(template)
    fig10.update_xaxes(axes_theme)
    fig10.update_yaxes(axes_theme)

    # 3 grafico 1 card

    fig9 = go.Figure()
    fig9.add_trace(
        go.Indicator(
            mode="number",
            title={
                "text": f"<span style='font-size:190%'>Valor Total </span><br><span style='font-size:90%'>Em vendas</span><br>"
            },
            value=dff["Valor Pago"].sum(),
            number={"prefix": "R$", "font": {"size": 55}},
        )
    )
    fig9.update_layout(template)

    # 4 grafico 2 card

    fig11 = go.Figure()
    fig11.add_trace(
        go.Indicator(
            mode="number",
            title={
                "text": f"<span style='font-size:190%'>Chamadas Totais</span><br><span style='font-size:70%'></span><br>"
            },
            value=dff["Chamadas Realizadas"].sum(),
            number={"font": {"size": 55}},
        )
    )
    fig11.update_layout(template)

    # 5 grafico grafico linhas propaganda

    df4 = (
        dff.groupby(["Meio de Propaganda", "Mês_"], observed=True)["Valor Pago"]
        .sum()
        .reset_index()
    )
    df4 = df4.sort_values("Mês_")
    fig4 = px.line(
        df4,
        y="Valor Pago",
        x="Mês_",
        color="Meio de Propaganda",
        color_discrete_map=dict_cores_ad,
        markers="lines+markers",
    )
    fig4.update_layout(
        {"margin": {"l": 0, "r": 30, "t": 30, "b": 0}},
        yaxis_title="",
        xaxis_title="",
        width=890,
        height=300,
        legend_itemclick="toggleothers",
        xaxis=dict(tickmode="array", tickvals=list(range(1, 13)), ticktext=meses_ordem),
    )
    fig4.update_layout(template)
    fig4.update_xaxes(axes_theme)
    fig4.update_yaxes(axes_theme)

    # 6 grafico pizza

    fig5 = px.pie(
        dff,
        names="Meio de Propaganda",
        values="Valor Pago",
        color="Meio de Propaganda",
        hole=0.5,
        color_discrete_map=dict_cores_ad,
    )
    fig5.update_layout(
        {"margin": {"l": 0, "r": 10, "t": 10, "b": 10}},
        height=300,
        width=510,
    )
    fig5.update_layout(template)

    # 7 grafico card top consultor

    df6 = dff.groupby(["Consultor", "Equipe"], observed=True)["Valor Pago"].sum()
    df6.sort_values(ascending=False, inplace=True)
    df6 = df6.reset_index()
    fig8 = go.Figure()
    fig8.add_trace(
        go.Indicator(
            mode="number+delta",
            title={
                "text": f"<span style='font-size:170%'>{df6['Consultor'].iloc[0]} - Top Consultant</span><br><span style='font-size:110%'>Em vendas - em relação a média</span><br>"
            },
            value=df6["Valor Pago"].iloc[0],
            number={"prefix": "R$", "font": {"size": 45}},
            delta={
                "relative": True,
                "valueformat": ".1%",
                "reference": df6["Valor Pago"].mean(),
            },
        )
    )
    fig8.update_layout({"margin": {"l": 0, "r": 0, "t": 47, "b": 0}})
    fig8.update_layout(template)
    # 8 grafico melhor equipe

    df8 = dff.groupby("Equipe")["Valor Pago"].sum()
    df8.sort_values(ascending=False, inplace=True)
    df8 = df8.reset_index()
    fig12 = go.Figure()
    fig12.add_trace(
        go.Indicator(
            mode="number+delta",
            title={
                "text": f"<span style='font-size:170%'>{df8['Equipe'].iloc[0]} - Top Team</span><br><span style='font-size:110%'>Em vendas - em relação a média</span><br>"
            },
            value=df8["Valor Pago"].iloc[0],
            number={"prefix": "R$", "font": {"size": 45}},
            delta={
                "relative": True,
                "valueformat": ".1%",
                "reference": df8["Valor Pago"].mean(),
            },
        )
    )
    fig12.update_layout({"margin": {"l": 0, "r": 0, "t": 35, "b": 0}})
    fig12.update_layout(template)

    # 9 grafico equipe por mes

    df5 = (
        dff.groupby(["Mês_", "Equipe"], observed=True)["Valor Pago"].sum().reset_index()
    )
    df5_all = dff.groupby("Mês_", observed=True)["Valor Pago"].sum().reset_index()
    fig6 = px.line(df5, x="Mês_", y="Valor Pago", color="Equipe")
    fig6.add_trace(
        go.Scatter(
            y=df5_all["Valor Pago"],
            x=df5_all["Mês_"],
            mode="lines+markers",
            fill="tonexty",
            fillcolor="rgba(255, 0, 0, 0.2)",
            name="Total de Vendas",
        )
    )
    fig6.update_layout(
        {"margin": {"l": 0, "r": 30, "t": 30, "b": 0}},
        yaxis_title="",
        xaxis_title="",
        width=890,
        height=253,
        legend_itemclick="toggleothers",
        xaxis=dict(tickmode="array", tickvals=list(range(1, 13)), ticktext=meses_ordem),
    )
    fig6.update_layout(template)
    fig6.update_xaxes(axes_theme)
    fig6.update_yaxes(axes_theme)

    # 10 grafico soma de chamdas por mes

    df3 = dff.groupby(axis_x, observed=True)["Chamadas Realizadas"].sum().reset_index()
    fig3 = px.area(df3, x=axis_x, y="Chamadas Realizadas")
    fig3.add_annotation(
        text=f'Soma de Chamadas por {axis_x.replace("_","")}',
        xref="paper",
        yref="paper",
        align="center",
        bgcolor="rgba(0,0,0,1)",
        x=0.02,
        y=0.95,
        showarrow=False,
        font=dict(color="white", size=20),
    )
    fig3.add_annotation(
        text=f"Média: {round(df3['Chamadas Realizadas'].mean(),1)}",
        xref="paper",
        yref="paper",
        align="center",
        bgcolor="rgba(0,0,0,1)",
        x=0.02,
        y=0.78,
        showarrow=False,
        font=dict(color="white", size=20),
    )
    fig3.update_layout(
        {"margin": {"l": 0, "r": 30, "t": 30, "b": 0}},
        yaxis_title="",
        xaxis_title="",
        width=890,
        height=253,
        **number_to_month,
        # xaxis=dict(tickmode="array", tickvals=list(range(1, 13)), ticktext=meses_ordem),
    )
    fig3.update_layout(template)
    fig3.update_xaxes(axes_theme)
    fig3.update_yaxes(axes_theme)
    fig3.update_traces(mode="lines+markers")

    return fig, fig10, fig9, fig11, fig4, fig5, fig8, fig12, fig6, fig3


if __name__ == "__main__":
    app.run_server(debug=False,)
