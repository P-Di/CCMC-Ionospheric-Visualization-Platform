import json
import pandas as pd
from pandas.api.typing import DataFrameGroupBy
import plotly.express as px
from dash import html, dcc, dash_table 
import dash_bootstrap_components as dbc

###########################
# Data Loading
###########################

files = [
    "data/thermosphere_data/DTM2013-01_scores.json", 
    "data/thermosphere_data/DTM2020-01_scores.json", 
    "data/thermosphere_data/JB2008-01_scores.json",
    "data/thermosphere_data/MSIS20-01_scores.json",
    "data/thermosphere_data/MSISE00-01_scores.json"
]

formatted_data = {
    "model": [],
    "TP": [],
    "category": [],
    "satellite": [],
    "phase": [],
    "ap_max": [],
    "f107_max": [],
    "mean_OC": [],
    "debias_mean_OC": [],
    "stddev_OC": [],
    "R": []
}
for file in files:
    with open(file, 'r') as f:
        data = json.load(f)
        model = file[23:file.find("_scores.json")]
        for key in data["events"]:
            for satellite in data["events"][key]["satellites"]:
                for phase in data["events"][key]["satellites"][satellite]:
                    formatted_data["model"].append(model)
                    formatted_data["TP"].append(data["events"][key]["TP"])
                    formatted_data["category"].append(data["events"][key]["category"])
                    formatted_data["satellite"].append(satellite)
                    formatted_data["phase"].append(phase)
                    formatted_data["ap_max"].append(data["events"][key]["ap_max"])
                    formatted_data["f107_max"].append(data["events"][key]["f107_max"])
                    formatted_data["mean_OC"].append(data["events"][key]["satellites"][satellite][phase]["mean_OC"])
                    formatted_data["debias_mean_OC"].append(data["events"][key]["satellites"][satellite][phase]["debias_mean_OC"])
                    formatted_data["stddev_OC"].append(data["events"][key]["satellites"][satellite][phase]["stddev_OC"])
                    formatted_data["R"].append(data["events"][key]["satellites"][satellite][phase]["R"])

thermosphere_df = pd.DataFrame(formatted_data)

# ensure proper ordering of the phases
phase_order = ["total", "pre_storm", "onset", "main_recovery", "post_storm"]
thermosphere_df["phase"] = pd.Categorical(thermosphere_df["phase"], categories=phase_order, ordered=True)
filtered_df = pd.DataFrame()

###########################
# Declarations
###########################

ap_thresholds = [80, 132, 207, 236, 300]
f107_thresholds = [70, 100, 150, 200, 250]
image_paths = ['assets/CCMC.png', 'assets/airflow1.jpg']
satellites = [" CHAMP", " GOCE", " GRACE-A", " SWARM-A", " GRACE-FO"]
tpid_base_url = "https://kauai.ccmc.gsfc.nasa.gov/CMR/TimeInterval/viewTI?id="

benchmark_tpids = ['2002-05-TP-02', '2002-09-TP-03', '2003-08-TP-02', '2003-11-TP-02', '2004-08-TP-01', '2005-01-TP-02',
                   '2005-01-TP-04', '2005-04-TP-01', '2005-06-TP-01', '2005-06-TP-02', '2005-09-TP-03', '2006-04-TP-02',
                   '2006-12-TP-01', '2010-04-TP-01', '2011-08-TP-01', '2011-10-TP-01', '2012-07-TP-01', '2013-05-TP-01', 
                   '2013-09-TP-01', '2015-03-TP-01', '2015-06-TP-02', '2015-09-TP-02', '2017-05-TP-01', '2021-05-TP-01',
                   '2021-11-TP-01', '2023-03-TP-01', '2023-04-TP-01', '2023-11-TP-01'] 

data_selection = html.Div(
    id="data-selection",
    children=[
        html.Div([
            html.Div(html.B("Select a Parameter to Analyze")),
            dcc.Dropdown(
                options=[
                    "mean_OC", 
                    "debias_mean_OC", 
                    "stddev_OC", 
                    "R"
                ], 
                value="mean_OC", 
                id="parameter_selection",
                style={
                    "margin-top": "15px", 
                }
            )
        ]),
        html.Div([
            html.Div(html.B("Select Event Category")),
            dcc.Dropdown(
                options=[
                    {"label": "All", "value": "all"},
                    {"label": "Single Peak", "value": "single_peak"},
                    {"label": "Multiple Peak", "value": "multiple_peak"}
                ], 
                value="all", 
                id="category_selections",
                style={
                    "margin-top": "10px", 
                }
            )
        ]),
        html.Div([
            html.Div(html.B("Satellites")),
            dcc.Checklist(
                id="satellites",
                options=satellites,
                value=satellites
            )
        ])
    ]
)


##########################
# App Layout Definition
##########################

thermosphere_title = "DRAFT Thermosphere Neutral Density Assessment During Storm Times"
thermosphere_layout = html.Div(
    style = {
        'backgroundColor':'#f4f6f7', 
        'margin': '0'
    }, 
    children=[  
        html.Div( #Create a background for the CCMC logo image.
            style={
            'width': '20%', 
                'background-color': '#f4f6f7', 
                'height': '200px', 
                'position': 'fixed',
                'margin-top': '0px',
                'box-shadow': '5px 5px 5px #ededed ',
                "zIndex": "1" # Control the layers of the title, with this being the lowest layer.
            }
        ),
        # Add the properly formatted CCMC image and airflow photo to the top of the page.
        html.Img(
            id="image1", 
            src=image_paths[0], 
            style={
                "zIndex": "2",
                'height': '100px', 
                'width': 'auto%', 
                'position': 'fixed',
                'background-color': '#f4f6f7'
            }
        ),
        dbc.Tooltip( #Airflow Image Credits.
            "Image Credit: NASA/Don Pettit",
            target="picture_bg", 
            placement="bottom"
        ),
        html.Div(
            id='img_container', 
            children=[ #Airflow Image and text.
                html.Img(
                    id = 'picture_bg', 
                    src=image_paths[1],
                    style={"zIndex": "3", 'top': '0', 'width': '100%', 'height': '100px', 'object-fit': 'cover'}
                ),
                html.Div(
                    id='text_overlay',
                    children=[
                        html.P(
                            "Thermosphere Neutral Density Assessment", 
                            id='text_box', 
                            style={
                                "zIndex": "4",
                                'position': 'absolute', 
                                'top': '10px', 
                                'left': '10px', 
                                'color': 'white', 
                                'font-size': '54px', 
                                'overflowX': 'hidden', 
                                'white-space': 'nowrap'
                            }
                        )
                    ]
                )
            ],
            style={
                "zIndex": "3", 
                'padding': '0', 
                'margin': '0', 
                'width': '100%', 
                'height': '100%', 
                'position': 'relative', 
                'margin-left': '20%',
                'overflowX': 'hidden', 
                'width':'80%'
            }
        ),
        html.Div(
            style={
                "zIndex": "2", 
                'width': '20%', 
                'background-color': '#f4f6f7', 
                'padding': '20px', 
                'height': '100%', 
                'position': 'fixed',
                'margin-top': '0px',
                'box-shadow': '5px 5px 5px #ededed'
            },
            children=[
                html.Div([
                    html.Div(html.B("Project")),
                    dcc.Dropdown(
                        id="project",
                        options=[
                            {'label': 'Ionosphere Model Validation', 'value': 'IMV'},
                            {'label': 'Thermosphere Neutral Density Assessment', 'value': "TNDA"},
                            {'label': 'Ray Tracing', 'value': 'RT', 'disabled': True},
                            {'label': 'GPS Positioning', 'value': 'GPS', 'disabled': True}
                        ],
                        value="TNDA"
                    )
                ]),
                data_selection
            ]
        ),
        html.Div(
            style={
                "width": "80%",
                "margin-left": "20%",
                "background": "white"
            },
            children=[
                dcc.Tabs(
                    id="tabs",
                    value="home",
                    children=[
                        dcc.Tab(label="Home", value="home", style={"background-color": "white", "color": "#e59b1c"}, 
                            selected_style={"background-color": "#e59b1c", "color": "white", "border": "none"}),
                        dcc.Tab(label="Analysis Dashboard", value="dashboard", style={"background-color": "white", "color": "#e59b1c"}, 
                            selected_style={"background-color": "#e59b1c", "color": "white", "border": "none"}),
                        dcc.Tab(label="Benchmark", value="benchmark", style={"background-color": "white", "color": "#e59b1c"}, 
                            selected_style={"background-color": "#e59b1c", "color": "white", "border": "none"})
                    ]),
                html.Div(id="thermosphere-main-content")
            ]
        ),
        html.Footer(
            children=[
                html.A("Accessibility", href='https://www.nasa.gov/accessibility', target="_blank"), 
                html.Span(children=" | "),
                html.A("Privacy Policy", href='https://www.nasa.gov/privacy/', target="_blank"),
                html.Span(children=" | Curators: Paul DiMarzio and Dr. Min-Yang Chou | NASA Official: Maria Kuznetsova")
            ],
            style={
                'margin-left' : '20%',
                "textAlign": "center",
                "padding": "10px",
                "backgroundColor": "#f1f1f1",
                "position": "relative", 
                "bottom": "0px",
                "width": "80%"
            }
        )
    ]
)

#################################
# Callbacks for Thermosphere Page
#################################
def update_content(tab, parameter):
    if tab == "home":
        return html.Div(
            style={"padding-left": "10px"},
            children=[
                html.H1("Thermospheric Analysis Home Page"),
            ]
        )
    elif tab == "dashboard":
        return [
            html.Div(
                style={
                    "padding-top": "10px", 
                    "padding-left": "10px", 
                    "width": "100%",
                    "padding-left": "10%",
                    "padding-right": "10%",
                    "background-color": "#f4f6f7"
                },
                children=[
                    html.P(["Select the ", html.B("peak Ap threshold"), ": greater or equal to"]),
                    dcc.Slider(
                        0, 4, 1, 
                        marks={key: str(value) for key, value in enumerate(ap_thresholds)}, 
                        id="ap_max_slider",
                        value=0,
                        persistence=True, 
                        persistence_type="session",
                        included=False
                    ),
                    html.P(["Select the ", html.B("peak F107 threshold"), ": greater or equal to"]),
                    dcc.Slider(
                        0, 4, 1,
                        marks={key: str(value) for key, value in enumerate(f107_thresholds)},
                        id="f107_max_slider",
                        value=0,
                        persistence=True,
                        persistence_type="session",
                        included=False
                    )
                ],
            ),
            html.Div(
                style={
                    "width": "70%",
                    "margin-left": "auto",
                    "margin-right": "auto"
                },
                children=[
                    html.Div([
                        html.Span(
                            html.B(f"Skills By Event: {parameter}"),
                            style={
                                "z-index": "3", 
                                "position": "relative",
                                "top": "50px",
                                "left": "45%"
                            } 
                        ),
                        dcc.Graph(
                            id="skills-by-event-plot",
                        )
                    ]),
                    html.Div([
                        html.Span(html.B("Skills By Phase")),
                        dash_table.DataTable(
                            id="skills-by-phase-table",
                            style_header={
                                "background-color": "#e59b1c",
                                "text-align": "center"
                            },
                            style_cell={
                                "text-align": "center"
                            } 
                        )
                    ]),
                    html.Div(id="skills-by-phase-plots")
                ]
            ),
            html.Div(
                id="tpid-menu-button",
                children="Storm IDs"
            ),
            html.Div(
                id="tpid-menu",
                children=[
                    html.Div([
                        html.B("TPID Menu"),
                        html.Div(
                            id="tpid-x-button",
                            children=[
                                html.Div(className="x-component", id="x-arm1"),
                                html.Div(className="x-component", id="x-arm2")
                            ]
                        )],
                        style={
                            "padding": "10px",
                            "position": "fixed", 
                            "top": "0px",
                            "right": "0px",
                            "width": "20%",
                            "background-color": "#f1f1f1"
                        }
                    ),
                    html.Div(
                        html.Ul(id="tpid-list"),
                        style={"margin-top": "45px"}
                    )
                ]
            )   
        ]
    elif tab == "benchmark":
        benchmark_df = thermosphere_df[thermosphere_df["TP"].isin(benchmark_tpids)]
        benchmark_df = benchmark_df[benchmark_df["ap_max"].ge(ap_thresholds[0])]
        benchmark_df = benchmark_df[benchmark_df["f107_max"].ge(ap_thresholds[0])]
        main_plot = px.box(benchmark_df, x="mean_OC", y="model")
        main_plot.update_traces(hoverinfo="none", hovertemplate=None)

        skills_by_phase_plots = []
        for file in files:
            model = file[23:file.find("_scores.json")]
            fig = px.box(benchmark_df[benchmark_df["model"] == model], x="phase", y="mean_OC")
            fig.update_traces(hoverinfo="none", hovertemplate=None)
            plot = html.Div([
                html.Span(
                    html.B(f"Skills By Phase: mean_OC ({model})"),
                    style={
                        "z-index": "3", 
                        "position": "relative",
                        "top": "50px",
                        "left": "35%"
                    } 
                ),
                dcc.Graph(figure=fig)
            ])
            skills_by_phase_plots.append(plot)

        # data  preparation for the pivot table
        skills_by_phase: DataFrameGroupBy = benchmark_df.groupby(["model", "phase"], observed=False)["mean_OC"]
        skills_by_phase: pd.DataFrame = (
            skills_by_phase.mean()
            .reset_index()
            .pivot(index="model", columns="phase", values=parameter)
            .round(2)
        )
        skills_by_phase.reset_index(inplace=True)
        table_data = skills_by_phase.to_dict("records")

        return html.Div(
            style={
                "width": "70%",
                "margin-left": "auto",
                "margin-right": "auto"
            },
            children=[
                html.Div([
                    html.Span(
                        html.B(f"Skills By Event: {parameter}"),
                        style={
                            "z-index": "3", 
                            "position": "relative",
                            "top": "50px",
                            "left": "45%"
                        } 
                    ),
                    dcc.Graph(
                        id="skills-by-event-plot",
                        figure=main_plot
                    )
                ]),
                html.Div([
                    html.Span(html.B("Skills By Phase: mean_OC")),
                    dash_table.DataTable(
                        id="skills-by-phase-table",
                        style_header={
                            "background-color": "#e59b1c",
                            "text-align": "center"
                        },
                        style_cell={
                            "text-align": "center"
                        },
                        data=table_data 
                    )
                ]),
                html.Div(id="skills-by-phase-plots", children=skills_by_phase_plots)
            ]
        )


def display_plots(parameter, category, ap_max_threshold, f107_max_threshold, satellites):
    satellites = [satellite.strip() for satellite in satellites] 

    global filtered_df
    filtered_df = thermosphere_df.copy()

    # data preparation for the one plot (more to come)
    if category != "all":
        filtered_df = filtered_df[filtered_df["category"] == category]
    filtered_df = filtered_df[filtered_df["satellite"].isin(satellites)]
    filtered_df = filtered_df[filtered_df["ap_max"].ge(ap_thresholds[ap_max_threshold])]
    filtered_df = filtered_df[filtered_df["f107_max"].ge(f107_thresholds[f107_max_threshold])]
    main_plot = px.box(filtered_df, x=parameter, y="model")
    main_plot.update_traces(hoverinfo="none", hovertemplate=None)

    skills_by_phase_plots = []
    for file in files:
        model = file[23:file.find("_scores.json")]

        fig = px.box(filtered_df[filtered_df["model"] == model], x="phase", y=parameter)
        fig.update_traces(hoverinfo="none", hovertemplate=None)

        plot = html.Div([
            html.Span(
                html.B(f"Skills By Phase: {parameter} ({model})"),
                style={
                    "z-index": "3", 
                    "position": "relative",
                    "top": "50px",
                    "left": "35%"
                } 
            ),
            dcc.Graph(figure=fig)
        ])
        skills_by_phase_plots.append(plot)
    
    # data preparation for the pivot table
    skills_by_phase: DataFrameGroupBy = filtered_df.groupby(["model", "phase"], observed=False)[parameter]
    skills_by_phase: pd.DataFrame = (
        skills_by_phase.mean()
        .reset_index()
        .pivot(index="model", columns="phase", values=parameter)
        .round(2)
    )
    skills_by_phase.reset_index(inplace=True)
    table_data = skills_by_phase.to_dict("records")
    
    return main_plot, table_data, skills_by_phase_plots 

def open_tpid_menu():
    # create the tpid list for the filtered_df
    tpid_list = []
    for tpid in filtered_df["TP"]:
        item = html.Li(
            html.A(
                tpid,
                href=tpid_base_url + tpid,
                target="_blank"
            )
        )
        tpid_list.append(item)
    return tpid_list