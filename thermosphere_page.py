"""
This module implements the Thermosphere Neutral Density Assessment dashboard. It is split into three main sections:
    1. DECLARATIONS - Contains declarations for global variables that are used throughout the program
    2. APP LAYOUT - Defines the base app layout that does not change
    3. DATA LOADING - Loads the json data from data/thermosphere_data and data/benchmark_data into pandas dataframes
    4. CALLBACK DEFINITIONS - defines how the page will update based on user input
To navigate to a given section search for the section name exactly as it is displayed above
"""

import json
import pandas as pd
from pandas.api.typing import DataFrameGroupBy
import plotly.express as px
from dash import html, dcc, dash_table 
import dash_bootstrap_components as dbc


###########################
# SECTION 1: DECLARATIONS
###########################

# declare global variables that will be used throughout the program
filtered_df = pd.DataFrame() # this variables is used to share data between callbacks
ap_thresholds = [80, 132, 207, 236, 300]
f107_thresholds = [70, 100, 150, 200, 250]
image_paths = ['assets/CCMC.png', 'assets/airflow1.jpg']
satellites = [" CHAMP", " GOCE", " GRACE-A", " SWARM-A", " GRACE-FO"]
tpid_base_url = "https://kauai.ccmc.gsfc.nasa.gov/CMR/TimeInterval/viewTI?id="


##########################
# SECTION 2: APP LAYOUT

# This section defines three dash app layouts.
# The "data_selection" layout is the portion of the lefthand menu where the user can select different parameters to filter the data
# The "thermosphere_layout" is the entire base layout that does not change. It includes the lefthand menu, the CCMC logo, the footer,
#   the airflow image and page title, and the tabs to select the description, dashboard, and benchmark pages
# The "tpid_menu" layout is the layout for the tpid popup that displays a list of links to the storm home page for each storm included
#   in the current displayed plot
##########################

# This is the dash layout for the lefthand data selection menu
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

# This is the basic layout for the thermosphere app
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
                    value="description",
                    children=[
                        dcc.Tab(label="Description", value="description", style={"background-color": "white", "color": "#e59b1c"}, 
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

# layout for the tpid menu popup
tpid_menu = html.Div(
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


###########################
# SECTION 3: DATA LOADING

# This section contains code that loads data from two sources, data/thermosphere_data and data/benchmark_data.
###########################

def format_data(files):
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
            for key in data["events"]:
                for satellite in data["events"][key]["satellites"]:
                    for phase in data["events"][key]["satellites"][satellite]:
                        formatted_data["model"].append(data["solution"])
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
    return formatted_data

def load_data():
    # analysis dashboard data
    dashboard_files = [
        "data/thermosphere_data/DTM2013-01_scores.json", 
        "data/thermosphere_data/DTM2020-01_scores.json", 
        "data/thermosphere_data/JB2008-01_scores.json",
        "data/thermosphere_data/MSIS20-01_scores.json",
        "data/thermosphere_data/MSISE00-01_scores.json"
    ]

    thermosphere_df = pd.DataFrame(format_data(dashboard_files))

    # benchmark data
    benchmark_files = [
        "data/benchmark_scores/CTIPe-01_benchmark_scores.json",
        "data/benchmark_scores/DTM2013-01_benchmark_scores.json",
        "data/benchmark_scores/DTM2020-01_benchmark_scores.json",
        "data/benchmark_scores/JB2008-01_benchmark_scores.json",
        "data/benchmark_scores/MSIS20-01_benchmark_scores.json",
        "data/benchmark_scores/MSISE00-01_benchmark_scores.json",
        "data/benchmark_scores/TIEGCM-Heelis-01_benchmark_scores.json",
        "data/benchmark_scores/TIEGCM-Weimer-01_benchmark_scores.json"
    ]

    benchmark_df = pd.DataFrame(format_data(benchmark_files))

    # ensure proper ordering of the phases
    phase_order = ["total", "pre_storm", "onset", "main_recovery", "post_storm"]
    thermosphere_df["phase"] = pd.Categorical(thermosphere_df["phase"], categories=phase_order, ordered=True)
    benchmark_df["phase"] = pd.Categorical(benchmark_df["phase"], categories=phase_order, ordered=True)

    return thermosphere_df, benchmark_df

# actually load the data into two global variables
thermosphere_df, benchmark_df = load_data()

################################
# SECTION 4: CALLBACK DEFINTIONS
################################

def update_content(tab, parameter):
    '''
    This is a callback function for the thermosphere page that displays the proper page depending on the tab that has been
    selected (description, dashboard, or benchmark)
    '''
    if tab == "description":
        return html.Div(
            style={"padding-left": "30px", "padding-right": "30px", "padding-bottom": "30px"},
            children=[
                html.H1("Introduction"),
                html.P(
                    """
                    Thermospheric density is the dominant source of uncertainty in the atmospheric drag. The diagram in Figure 1
                    shows how the data and model are involved in drag calculation. Thermosphere models estimate neutral density, 
                    composition, and temperature based on the solar and geomagnetic drivers. Physics-based models with the lower 
                    boundary located around the mesopause also need to specify the lower boundary condition representing the variability 
                    from the lower atmosphere. Biases from thermospheric models are amplified due to the satellite shape and aerodynamic 
                    model when calculating the drag force. This, in turn, introduces several error sources originating from the modeled 
                    thermospheric states in orbit computation. To make advances in orbit computation and determination, accurate 
                    specification and forecasting of thermosphere are required. Modelled neutral density must be validated against 
                    high-quality and high-spatial resolution neutral density datasets to identify strengths and weaknesses, establish 
                    error budgets, and improve the models after ingestion.
                    """
                ),
                html.Div(
                    [html.Img(className="description-fig", src="assets/Thermosphere_fig_1.png", 
                              alt="Figure 1: Diagram showing the data and models of a drag calculation."),
                     html.P(html.I("Firgure 1. Diagram showing the data and models of a drag calculation."))],
                    className="img-container"
                ),
                html.P("However, there are still several challenges remaining in the validation of neutral density."),
                html.Ol([
                    html.Li(
                        """
                        Validation studies often invloved only one or two events and a subset of models. this approach may not 
                        be robust or comprehansive.
                        """
                    ),
                    html.Li(
                        """
                        Staying updated with the growing number of models and their various versions remains chellenging, 
                        especially with open source models.
                        """
                    ),
                    html.Li(
                        """
                        Unified validation effort requires an online platform to keep track of the progress of model development.
                        """
                    )
                ]),
                html.P(
                    """
                    To addres these challenges, an assessment of thermosphere models under storm conditions was initiated within the COSPR 
                    ISWAT framework, leveraging the international collborative network. This allows the ocmmunity to systematically track
                    the progress of thermosphere models over time.
                    """
                ),
                html.P(
                    """
                    This validation campaign focuses on validating 1-D neutral density output from various model runs/solutions with
                    observation data from GOCE, CHAMP, GRACE, SWARM, and/or GRACE_FO for different time periods. The thermophsere models
                    are executed in-house using CCMC Runs-on-Request system and accessed. The model performance during the selected 
                    geomagnetically storm times from 2001 to 2023 are assessed for this study.
                    """
                ),
                html.H1("Methodology"),
                html.P(
                    """
                    An updated metric for thermospheric model assessment under geomagnetic storm conditions were proposed and implemented 
                    in the validation project (Sutton, 2018; Bruinsma et al., 2021; Bruinsma & Laurens, 2024). The metrics for 
                    comprehensive thermospheric model-data comparison are applied to establish the thermospheric model scorecard. 
                    """
                ),
                html.P(
                    """
                    Figure 2 (top) illustrates the four phases of a single-peak (SP) storm. Phase 1, the pre-storm interval, is used to 
                    de-bias the models relative to observations. A scaling factor is determined by computing the observed-to-computed (O/C) 
                    density ratio in the pre-storm phase, then applied to the model densities in all four phases. This de-biasing procedure 
                    is used to minimize the effect of non-storm related model errors on the assessment. 
                    """
                ),
                html.P(
                    """
                    Density data for the SP storms are selected from 30 hours before to 48 hours after the time when ap reaches 80, which 
                    defines t₀ and marks the end of Phase 2 (storm onset). Phase 3 encompasses the main and recovery phase, while Phase 4 
                    represents the post-storm phase.
                    """
                ),
                html.P(
                    """
                    Figure 2 (bottom) illustrates the phases for double- or multiple-peaked (MP) storms, exemplified by the 10–16 July 2004 
                    event. For the MP storms, t₀ is defined as the time when ap reaches 80, similar to SP storms. In Figure 2 (bottom), 
                    Phase 3 for MP storms is extended due to a second occurrence of ap = 80 at t = 1.4. The duration of Phase 3 varies, 
                    ending when ap falls below 80 again (at t ≈ 3.0 in this example), plus an additional 36 hours. Phase 4 then extends 
                    for 12 hours beyond the end of Phase 3. Table 1 summarizes the phases and their duration for SP and MP storms computed 
                    as list below with respect to t0.
                    """
                ),
                html.Div(
                    [html.Img(className="description-fig", src="assets/Thermosphere_fig_2.png", alt="Figure 2"),
                     html.P(html.I("""
                        Figure 2. The four phases of the assessment interavl for single-peak (top) and multiple-peak (bottom) storms, with t0
                        centered on the time of the first peak in ap with a minimum of 80. The X-axis represents the day relative to t0.
                        Adapted from Bruinsma and Laurens (2024).
                    """))], 
                    className="img-container"),
                html.Table([
                    html.Tr([
                        html.Th("Phase"),
                        html.Th("Single-Peak (SP) Storm"),
                        html.Th("Multiple-Peaked (MP) Storm")
                    ]),
                    html.Tr([
                        html.Td("Phase 1"),
                        html.Td("t0 - 30 h to t0 - 18 h"),
                        html.Td("t0 - 30 h to t0 - 18 h"),
                    ]),
                    html.Tr([
                        html.Td("Phase 2"),
                        html.Td("t0 - 18 h to t0"),
                        html.Td("t0 - 18 h to t0")
                    ]),
                    html.Tr([
                        html.Td("Phase 3"),
                        html.Td("t0  to t0 + 36 h"),
                        html.Td("t0 to t0 + variable duration + 36 h")
                    ]),
                    html.Tr([
                        html.Td("Phase 4"),
                        html.Td("t0 + 36 h to t0 + 48 h"),
                        html.Td("End of Phase 3 + 12 h")
                    ])
                ]), 
                html.Br(),
                html.P(html.I(
                    """Table 1. The phases and their durations for single-peak (SP) and multiple-peaked (MP) storms, 
                    computed relative to t0, as listed below. Adapted from Bruinsma and Laurens (2024)."""
                )),
                html.P(
                    """
                    After debiasing, the observed-to-computed (O/C) density ratio is re-computed for the main and recovery phases of each 
                    storm to express model’s skill to reproduce observations during the geomagnetically storm times. Density ratios of one 
                    indicate perfect duplication of the observations, i.e., an unbiased model that reproduces all features; deviation from 
                    unity points to under (larger than one) or overestimation (smaller than one). A model bias, i.e., the mean of the 
                    density ratios differs from unity, is most damaging to orbit extrapolation because it causes position errors that 
                    increase with time.
                    """
                ),
                html.P(
                    """
                    The standard deviation (Std. Dev.) of the density ratios, computed as percentage of the observation, represents a 
                    combination of the ability of the model to reproduce observed density variations, and the geophysical noise 
                    (e.g., waves, the short duration effect of large flares) and instrumental noise in the observations.
                    """
                ),
                html.P(
                    """
                    The mean and Std. Dev. of the O/C density ratios, due to their distribution, are computed in log space (Sutton, 2018; 
                    Bruinsma et al., 2021):
                    """
                ),
                html.Ul([
                    html.Li([
                        "Average Observed-to-Compute Density (O/C) (= mean scaling factor of the model)",
                        html.Ul(html.Li(html.Img(src="assets/Thermosphere_equation_1.png", alt="Mean_OC computation")))
                    ]),
                    html.Li([
                        "Average standard deviation (Std. Dev.) of Observed-to-Compute Density (O/C)",
                        html.Ul(html.Li(html.Img(src="assets/Thermosphere_equation_2.png", alt="StdDev_OC computation")))
                    ])
                ]),
                html.P("where N is the total number of observations."),
                html.H1("References:"),
                html.P([
                    """
                    Sutton EK. 2018. A new method of physics-based data assimilation for the quiet and disturbed thermosphere. 
                    Space Weather 16: 736–753.
                    """,
                    html.A("https://doi.org/10.1002/2017SW00178.", href="https://doi.org/10.1002/2017SW00178", target="_blank")
                ]),
                html.P([
                    """
                    Bruinsma S, Boniface C, Sutton EK & Fedrizzi M 2021. Thermosphere modeling capabilities assessment: geomagnetic storms. 
                    J. Space Weather Space Clim. 11, 12.
                    """,
                    html.A("https://doi.org/10.1051/swsc/2021002.", href="https://doi.org/10.1051/swsc/2021002", target="_blank")
                ]),
                html.P([
                    """
                    Bruinsma S & Laurens S. 2024. Thermosphere model assessment for geomagnetic storms from 2001 to 2023. J. Space Weather 
                    Space Clim. 14, 28. 
                    """,
                    html.A("https://doi.org/10.1051/swsc/2024027.", href="https://doi.org/10.1051/swsc/2024027", target="_blank")
                ])
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
                                "left": "120px"
                            } 
                        ),
                        dcc.Graph(
                            id="skills-by-event-plot",
                        ),
                        html.Div(id="main-plot-stats", className="stats")
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
            tpid_menu
        ]
    elif tab == "benchmark":
        global filtered_df

        filtered_df = benchmark_df.copy()
        filtered_df = filtered_df[filtered_df["ap_max"].ge(ap_thresholds[0])]
        filtered_df = filtered_df[filtered_df["f107_max"].ge(ap_thresholds[0])]
        main_plot = px.box(filtered_df, x=parameter, y="model")
        main_plot.update_traces(hoverinfo="none", hovertemplate=None)

        # make benchmark main plot stats
        bench_main_stats: pd.DataFrame = filtered_df.groupby("model", observed=False)[parameter].agg(["mean", "std"]).reset_index().round(2)
        bench_main_stats = bench_main_stats.iloc[::-1]
        formatted_bench_main_stats = []
        for _, row in bench_main_stats.iterrows():
            if  row["model"] == "MSISE00-01":
                stats_label = html.Div(
                    children=["Mean: " + str(row["mean"]), html.Br(), "StD: " + str(row["std"])]
                )
                formatted_bench_main_stats.append(stats_label)
                continue
            stats_label = html.Div(
                children=["Mean: " + str(row["mean"]), html.Br(), "StD: " + str(row["std"])],
                style={"margin-top": "25px"}
            )
            formatted_bench_main_stats.append(stats_label)
        # TODO: Need to find a way to return "formatted_bench_main_stats". I don't think I can do it from the "update_content" callback

        skills_by_phase_plots = []
        for model in filtered_df["model"].unique():
            if parameter == "debias_mean_OC":
                debias_df = filtered_df[filtered_df["phase"] != "pre_storm"]
                fig = px.box(debias_df[debias_df["model"] == model], x="phase", y=parameter)
            else:
                fig = px.box(filtered_df[filtered_df["model"] == model], x="phase", y=parameter)

            fig.update_traces(hoverinfo="none", hovertemplate=None)
            plot = html.Div([
                html.Span(
                    html.B(f"Skills By Phase: {parameter} ({model})"),
                    style={
                        "z-index": "3", 
                        "position": "relative",
                        "top": "50px",
                        "left": "80px"
                    } 
                ),
                dcc.Graph(figure=fig)
            ])
            skills_by_phase_plots.append(plot)

        # data  preparation for the pivot table
        skills_by_phase: DataFrameGroupBy = filtered_df.groupby(["model", "phase"], observed=False)[parameter]
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
                            "left": "160px"
                        } 
                    ),
                    dcc.Graph(
                        id="skills-by-event-plot",
                        figure=main_plot
                    ),
                    html.Div(id="bench-main-stats", className="stats")
                ]),
                html.Div([
                    html.Span(html.B(f"Skills By Phase: {parameter}")),
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
                html.Div(id="skills-by-phase-plots", children=skills_by_phase_plots),
                html.Div(
                    id="tpid-menu-button",
                    children="Storm IDs"
                ),
                tpid_menu
            ]
        )


def display_plots(parameter, category, ap_max_threshold, f107_max_threshold, satellites):
    """
    This callback filters thermosphere_df using the input data and populates the plots and table with the filtered dataframe.
    The filtered dataframe is stored in the global variable filtered_df so that the tpid callback can access that data
    """
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
    
    # create the elements for the main plot mean and std display
    main_plot_stats: pd.DataFrame = filtered_df.groupby("model", observed=False)[parameter].agg(["mean", "std"]).reset_index().round(2)
    main_plot_stats = main_plot_stats.iloc[::-1]
    formatted_main_plot_stats = []
    for _, row in main_plot_stats.iterrows():
        if  row["model"] == "MSISE00-01":
            stats_label = html.Div(
                children=["Mean: " + str(row["mean"]), html.Br(), "StD: " + str(row["std"])]
            )
            formatted_main_plot_stats.append(stats_label)
            continue
        stats_label = html.Div(
            children=["Mean: " + str(row["mean"]), html.Br(), "StD: " + str(row["std"])],
            style={"margin-top": "25px"}
        )
        formatted_main_plot_stats.append(stats_label)

    # create the skills by phase plots for each model
    skills_by_phase_plots = []
    for model in filtered_df["model"].unique():
        # since the debias_mean_OC pre_storm value is set to 1 throughout, don't display it on the plots (it adds no info)
        if parameter == "debias_mean_OC":
            debias_df = filtered_df[filtered_df["phase"] != "pre_storm"]
            fig = px.box(debias_df[debias_df["model"] == model], x="phase", y=parameter)
        else:
            fig = px.box(filtered_df[filtered_df["model"] == model], x="phase", y=parameter)
        fig.update_traces(hoverinfo="none", hovertemplate=None) # removes the hover function of the plots

        # creates the actual webpage elements for the plots
        plot = html.Div([
            html.Span(
                html.B(f"Skills By Phase: {parameter} ({model})"),
                style={
                    "z-index": "3", 
                    "position": "relative",
                    "top": "50px",
                    "left": "80px"
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

    return (
        main_plot, 
        table_data, 
        skills_by_phase_plots,
        formatted_main_plot_stats 
    )


def open_tpid_menu():
    """
    This callback creates the links that will be in the tpid popup. It accesses the correct data using the global variable filtered_df
    """
    tpid_list = []
    for tpid in filtered_df["TP"].drop_duplicates():
        item = html.Li(
            html.A(
                tpid,
                href=tpid_base_url + tpid,
                target="_blank"
            )
        )
        tpid_list.append(item)
    return tpid_list