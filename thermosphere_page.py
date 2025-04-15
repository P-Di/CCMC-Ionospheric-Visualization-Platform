"""
This module implements the Thermosphere Neutral Density Assessment dashboard. It is split into three main sections:
    SECTION 1: DECLARATIONS - Contains declarations for global variables that are used throughout the program
    SECTION 2: APP LAYOUT - Defines the base app layout that does not change
    SECTION 3: DATA LOADING - Loads the json data from data/thermosphere_data and data/benchmark_data into pandas dataframes
    SECTION 4: CALLBACK DEFINITIONS - defines how the page will update based on user input
To navigate to a given section search for the section name exactly as it is displayed above
"""

# Modules to load and store model/solution scores
import json, os
import pandas as pd

# Modules to create the dash layout
from dash import html, dcc, dash_table 
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Modules to create plots and specific components
import thermosphere_helpers.stripplot as sp
import thermosphere_helpers.description_page as dp


###########################
# SECTION 1: DECLARATIONS
###########################

def create_x_button(id: str) -> html.Div:
    '''
    Function to create an x button usually used to close a popup

    :param id: The id to be assigned to the x button
    :return x_button: Dash markup describing the button
    '''

    return html.Div(
        id=id,
        className="x-button",
        children=[
            html.Div(className="x-component", id="x-arm1"),
            html.Div(className="x-component", id="x-arm2")
        ]
    )

def options_from_list(label):
    return {
        "label": html.P(label, style={"display": "none"}),
        "value": label
    }

def generate_labels(label):
    return html.Span(label, id=f"{label}-label", className="checklist-label", n_clicks=0)

# declare global variables that will be used throughout the program

ap_thresholds = [80, 132, 207, 236, 300]
f107_thresholds = [66, 100, 150, 200, 250]
tpid_base_url = "https://kauai.ccmc.gsfc.nasa.gov/CMR/TimeInterval/viewTI?id="
image_paths = ['assets/CCMC.png', 'assets/airflow1.jpg', "assets/options-icon.svg"]
dashboard_data_dir = "data/thermosphere_data"
benchmark_data_dir = "data/benchmark_scores"

satellites = ["CHAMP", "GOCE", "GRACE-A", "SWARM-A", "GRACE-FO"]
satellite_opts = list(map(options_from_list, satellites))
satellite_labels = list(map(generate_labels, satellites))

models = ["MSISE00-01", "MSIS20-01", "JB2008-01", "DTM2020-01", "DTM2013-01", "TIEGCM-Weimer-01", "TIEGCM-Heelis-01", "CTIPe-01", "GITM-01"]
model_opts = list(map(options_from_list, models))
model_labels = list(map(generate_labels, models))


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
        # Begin paramter selection Dropdown
        html.Div([
            html.Div(html.Strong("Select a Parameter to Analyze")),
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
        # End paramter selection Dropdown

        # Begin event catagory selection Dropdown
        html.Div([
            html.Div(html.Strong("Select Event Category")),
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
        # End event category selection Dropdown

        # Begin satellite selection Checklist
        html.Div([
            html.Div(html.Strong("Satellites")),
            dcc.Checklist(
                id="satellites",
                options=satellite_opts,
                value=satellites
            ),
            html.Div(satellite_labels, id="satellite-labels"),
        ]),
        # End satellite selection Checklist

        # Begin model selection Checklist
        html.Div([
            html.Div(html.Strong("Models")),
            dcc.Checklist(
                id="models",
                options=model_opts,
                value=models
            ),
            html.Div(model_labels, id="model-labels")
        ]),
        # End model selection Checklist

        # Begin satellite and model popup
        html.Div(
            [
                create_x_button("satellite-desc-x-button"),
                html.Div(id="satellite-description-data")
            ],
            id="satellite-description-popup"
        )
        # End satellite and model popup
    ]
)

# This is the basic layout for the thermosphere app
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
                            "CCMC Ionospheric and Thermospheric Score Board", 
                            id='text_box', 
                            style={
                                "zIndex": "4",
                                'position': 'absolute', 
                                'top': '10px', 
                                'left': '10px', 
                                'color': 'white', 
                                'font-size': '50px', 
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
                'box-shadow': '5px 5px 5px #ededed',
            },
            children=[
                html.Div([
                    html.Div(html.Strong("Project")),
                    dcc.Dropdown(
                        id="project",
                        options=[
                            {'label': 'Ionosphere Model Validation', 'value': 'IMV'},
                            {'label': 'Thermosphere Neutral Density Assessment', 'value': "TNDA"},
                            {'label': 'Ray Tracing', 'value': 'RT', 'disabled': True},
                            {'label': 'GPS Positioning', 'value': 'GPS', 'disabled': True}
                        ],
                        value="TNDA",
                    )
                ]),
                data_selection,
            ]
        ),
        # This div contains the dcc Tab components that allow the user to switch between tabs
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
                html.Span(children=" | Curators: Paul DiMarzio, Joseph Sypal, and Dr. Min-Yang Chou | NASA Official: Maria Kuznetsova")
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
            html.Strong("TPID Menu"),
            create_x_button("tpid-x-button"),
            html.Div(
                id="basic-storm-data"
            )],
            style={
                "padding": "10px",
                "position": "fixed", 
                "top": "0px",
                "right": "0px",
                "width": "310px",
                "background-color": "#f1f1f1",
                "border-bottom": "1px solid black",
            }
        ),
        html.Div( # This is the target for the "open_tpid_menu" callback 
            html.Ul(id="tpid-list"),
            style={"margin-top": "110px"}
        )
    ]
)   


###########################
# SECTION 3: DATA LOADING

# This section contains code that loads data from two sources, data/thermosphere_data and data/benchmark_data.
# The data is stored as a pandas dataframe in two global variables, thermosphere_df and benchmark_df
###########################

def format_data(data_dir: str) -> dict:
    """
    Opens and reads each json file in `data_dir` and returns the data in the `formatted_data` dictionary that can be easily converted 
    into a dataframe.

    :param `data_dir`: The directory containing the json files

    :return `formatted_data`: A dictionary containing the json data where each key will be a column in the dataframe and maps to
        the values that it will take
    """
    # create the empty dictionary that the data will be returned in
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
    # loop through each file
    files = os.listdir(data_dir)
    files = list(map(lambda file: f"{data_dir}/{file}", files))
    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            for key in data["events"]:
                for satellite in data["events"][key]["satellites"]:
                    for phase in data["events"][key]["satellites"][satellite]:
                        # select the keys we want and append the data to the coorisponding list in the dictionary 
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

def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Defines the lists (`dashboard_files` and `benchmark_files`) that contain the paths to the json sources, 
    loads the data from the two sources into `thermosphere_df` and `benchmark_df` respectively, and ensures proper phase ordering
    in the dataframes.

    :return: A tuple containg the two dataframes with the storm data, `thermosphere_df` and `benchmark_df`
    """

    # convert the json data into a dataframe using the "format_data" function
    thermosphere_df = pd.DataFrame(format_data(dashboard_data_dir))

    # convert the json data into a dataframe using the "format_data" function
    benchmark_df = pd.DataFrame(format_data(benchmark_data_dir))

    # ensure proper ordering of phases column
    phase_order = ["total", "pre_storm", "onset", "main_recovery", "post_storm"]
    thermosphere_df["phase"] = pd.Categorical(thermosphere_df["phase"], categories=phase_order, ordered=True)
    benchmark_df["phase"] = pd.Categorical(benchmark_df["phase"], categories=phase_order, ordered=True)

    return thermosphere_df, benchmark_df

# actually load the data into two global variables
thermosphere_df, benchmark_df = load_data()

################################
# SECTION 4: CALLBACK DEFINITIONS

# This section contains callback implementations for the thermosphere callback page. These functions are called by the actual callbacks
#   in app.py
# There are three callback functions implemented in this section:
#   "update_content" - switches between tabs
#   "display_plots" - populated the plots on the analysis dashboard tab
#   "open_tpid_menu" - opens the tpid popup
# There is one more callback to close the tpid popup but it is a one-liner so it is implemented in app.py
################################

def update_content(tab, parameter):
    '''
    This is a callback function for the thermosphere page that displays the proper page depending on the tab that has been
    selected (description, dashboard, or benchmark)
    '''
    # There are three basic conditions in this function:
    #   if the tab value (passed in by the callback decorator) is description, render the description tab
    #   if the tab value is dashboard, render the analysis dashboard tab
    #   if the tab value is benchmark, render the benchamrk tab
    if tab == "description":
        # The description tab basically contains a bunch of static html
        return dp.description_page
    elif tab == "dashboard":
        # The dashboard block renders the base template for the analysis dashboard page which is populated by the "display_plots" callback
        # on page load/user input
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
                children=[ # Sliders to select peak Ap and F107 thresholds, storms displayed have peak ap/f107 values >= the selected value
                    html.P(["Select the ", html.Strong("peak Ap threshold"), ": greater or equal to"]),
                    dcc.Slider(
                        0, 4, 1, 
                        marks={key: str(value) for key, value in enumerate(ap_thresholds)}, 
                        id="ap_max_slider",
                        value=0,
                        persistence=True, 
                        persistence_type="session",
                        included=False
                    ),
                    html.P(["Select the ", html.Strong("peak F107 threshold"), ": greater or equal to"]),
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
            html.Div( # Target for the "open_tpid_menu" callback 
                id="tpid-menu-button-2",
                className="tpid-menu-button",
                children="Storm IDs"
            ),
            html.Div(
                style={
                    "width": "70%",
                    "margin-left": "auto",
                    "margin-right": "auto"
                },
                children=[
                    html.Div([ # The main plot on the page, compares thermosphere models
                        html.Span(
                            html.Strong(f"Skills By Event: {parameter}"),
                            style={
                                "z-index": "3", 
                                "position": "relative",
                                "top": "50px",
                                "left": "120px"
                            } 
                        ),
                        dcc.Graph(
                            id="skills-by-event-plot"
                        ),
                        html.Div(id="main-plot-stats", className="stats")
                    ]),
                    html.Div([ # Data table showing average parameter value for each phase for each model
                        html.Span(html.Strong("Skills By Phase")),
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
                    # This div is a target for the "update_plots" callback and will be populated with plotly graphs for each model plotted against phase
                    html.Div(id="skills-by-phase-plots")
                ]
            ),
            html.Div( # Target for the "open_tpid_menu" callback 
                id="tpid-menu-button-1",
                className="tpid-menu-button",
                children="Storm IDs"
            ),
            tpid_menu
        ]
    elif tab == "benchmark":

        # filter benchmark_df for peek ap/f107 values that are >= selected slider values
        filtered_df = benchmark_df.copy()
        filtered_df = filtered_df[filtered_df["ap_max"].ge(ap_thresholds[0])]
        filtered_df = filtered_df[filtered_df["f107_max"].ge(ap_thresholds[0])]

        (
            main_plot,
            table_data,
            skills_by_phase_plots,
            formatted_bench_main_stats,
            tpid_list,
            basic_storm_data
        ) = sp.create_plots(filtered_df, parameter, "TIEGCM-Weimer-01", tpid_base_url)

        tpid_menu.children[1].children.children = tpid_list
        tpid_menu.children[0].children[2].children = basic_storm_data

        # The actual dash layout for the benchmark page
        return [
            html.Div( # Target for the "open_tpid_menu" callback 
                id="tpid-menu-button-2",
                className="tpid-menu-button",
                children="Storm IDs"
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
                            html.Strong(f"Skills By Event: {parameter}"),
                            style={
                                "z-index": "3", 
                                "position": "relative",
                                "top": "50px",
                                "left": "160px"
                            } 
                        ),
                        dcc.Graph(
                            id="skills-by-event-plot",
                            figure=main_plot,
                            style={"height": "650px"}
                        ),
                        html.Div(id="bench-main-stats", className="stats", children=formatted_bench_main_stats, style={"top": "320px"})
                    ]),
                    html.Div([
                        html.Span(html.Strong(f"Skills By Phase: {parameter}")),
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
            ),
            html.Div( # target for "open_tpid_menu" callback
                id="tpid-menu-button-1",
                className="tpid-menu-button",
                children="Storm IDs"
            ),
            tpid_menu
        ]


def display_plots(
        parameter: str, 
        category: str, 
        ap_max_threshold: int, 
        f107_max_threshold: int, 
        satellites: list[str], 
        models: list[str]
    ) -> tuple[go.Figure, list[dict], list, list, list, list]:
    """
    This function is the actual implementation of the `display_thermosphere_plots` callback in `app.py`.

    This function filters the dataframe with all of the storm data to include only data included by the user's selection.
    Then it passes that data to the `create_plots` function in `stripplot.py` which returns dash firgures and html
    components that will be displayed on the page.

    :param parameter: A string containing the parameter that will be plotted.
    :param category: A string containing the category of storm that should be plotted (either 'all', 'single_peak', 'multiple_peak')
    :param ap_max_threshold: An int containing the minimum ap max value a storm should have to be plotted.
    :param f107_max_threshold: An int containing the minimum f107 max value a storm should have to be plotted.
    :param satellites: A list of strings where each string is the name of a satellite. If a storm was observed by a satellite in this
        list, that observation data should be plotted.
    :param models: A list of strings where each string is the name of a model/solution. If a model is in this list it will be plotted
        against `parameter`

    :return main_plot: The main stripplot which plots all models for the 'total' phase
    :return table_data: The pivot table data obtained from `filtered_df`
    :return skills_by_phase_plots: A list of figures containing the skills by phase plots for the parameter
    :return formatted_main_plot_stats: A list of dash html components which are the mean and std labels for the main plot
    :return tpid_list: A list of the hyperlinks to the storm home page for each unique storm in `filtered_df`
    :return basic_storm_data: Basic stats on the storms being displayed:
                              
                              * Total Storm Count
                              * Multiple Peak Count
                              * Single Peak Count
    """
    filtered_df = thermosphere_df.copy()

    # data preparation for the one plot (more to come)
    if category != "all":
        filtered_df = filtered_df[filtered_df["category"] == category]
    filtered_df = filtered_df[filtered_df["satellite"].isin(satellites)]
    filtered_df = filtered_df[filtered_df["model"].isin(models)]
    filtered_df = filtered_df[filtered_df["ap_max"].ge(ap_thresholds[ap_max_threshold])]
    filtered_df = filtered_df[filtered_df["f107_max"].ge(f107_thresholds[f107_max_threshold])]
    
    return sp.create_plots(filtered_df, parameter, "MSISE00-01", tpid_base_url)