"""
This module implements the Thermosphere Neutral Density Assessment dashboard. It is split into three main sections:
    SECTION 1: DECLARATIONS - Contains declarations for global variables that are used throughout the program
    SECTION 2: APP LAYOUT - Defines the base app layout that does not change
    SECTION 3: DATA LOADING - Loads the json data from data/thermosphere_data and data/benchmark_data into pandas dataframes
    SECTION 4: CALLBACK DEFINITIONS - defines how the page will update based on user input
To navigate to a given section search for the section name exactly as it is displayed above
"""

import json
import pandas as pd
from pandas.api.typing import DataFrameGroupBy
from dash import html, dcc, dash_table 
import dash_bootstrap_components as dbc

import thermosphere_helpers.stripplot as sp
import thermosphere_helpers.description_page as dp


###########################
# SECTION 1: DECLARATIONS
###########################

def dict_from_sat(satellite):
    return {
        "label": html.P(satellite, style={"display": "none"}),
        "value": satellite
    }

def generate_satellite_labels(satellite):
    return html.Span(
        [
            satellite,
            html.Img(src="assets/options-icon.svg", id= f"{satellite}-opts", className="options-icon"),
            # dbc.Tooltip(
            #     f"{satellite} description",
            #     target=f"{satellite}-opts",
            #     placement="right"
            # )
        ],
        id=f"{satellite}-label", className="satellite-label"   
    )

# declare global variables that will be used throughout the program
filtered_df = pd.DataFrame() # this variables is used to share data between callbacks
ap_thresholds = [80, 132, 207, 236, 300]
f107_thresholds = [70, 100, 150, 200, 250]
tpid_base_url = "https://kauai.ccmc.gsfc.nasa.gov/CMR/TimeInterval/viewTI?id="
image_paths = ['assets/CCMC.png', 'assets/airflow1.jpg', "assets/options-icon.svg"]

satellites = ["CHAMP", "GOCE", "GRACE-A", "SWARM-A", "GRACE-FO"]
satellite_opts = list(map(dict_from_sat, satellites))
satellite_labels = list(map(generate_satellite_labels, satellites))



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
                options=satellite_opts,
                value=satellites
            ),
            html.Div(satellite_labels, id="satellite-labels"),
        ]),
        html.Div(
            [
                html.Div( # made an x button for the tpid menu using three divs and css :)
                    id="satellite-desc-x-button",
                    className="x-button",
                    children=[
                        html.Div(className="x-component", id="x-arm1"),
                        html.Div(className="x-component", id="x-arm2")
                    ]
                ),
                html.Div(id="satellite-description-data")
            ],
            id="satellite-description-popup"
        )
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
            html.B("TPID Menu"),
            html.Div( # made an x button for the tpid menu using three divs and css :)
                id="tpid-x-button",
                className="x-button",
                children=[
                    html.Div(className="x-component", id="x-arm1"),
                    html.Div(className="x-component", id="x-arm2")
                ]
            ),
            html.Div(
                id="basic-storm-data"
            )],
            style={
                "padding": "10px",
                "position": "fixed", 
                "top": "0px",
                "right": "0px",
                "width": "20%",
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

def format_data(files: list[str]) -> dict:
    """
    Opens and reads each file in `files` and returns the data in the `formatted_data dictionary that can be easily converted 
    into a dataframe.

    :param `files`: A list of paths to json files

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
    # analysis dashboard data
    dashboard_files = [
        "data/thermosphere_data/DTM2013-01_scores.json", 
        "data/thermosphere_data/DTM2020-01_scores.json", 
        "data/thermosphere_data/JB2008-01_scores.json",
        "data/thermosphere_data/MSIS20-01_scores.json",
        "data/thermosphere_data/MSISE00-01_scores.json"
    ]

    # convert the json data into a dataframe using the "format_data" function
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

    # convert the json data into a dataframe using the "format_data" function
    benchmark_df = pd.DataFrame(format_data(benchmark_files))

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
                    html.Div([ # Data table showing average parameter value for each phase for each model
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
        # declare the variable filtered_df global
        global filtered_df

        # filter benchmark_df for peek ap/f107 values that are >= selected slider values
        filtered_df = benchmark_df.copy()
        filtered_df = filtered_df[filtered_df["ap_max"].ge(ap_thresholds[0])]
        filtered_df = filtered_df[filtered_df["f107_max"].ge(ap_thresholds[0])]

        # make benchmark main plot stats (rendered to the right of the plot)
        # This line does some pandas magic (i.e., I have no idea what it does it just gives me the mean and std)
        bench_main_stats: pd.DataFrame = filtered_df.groupby("model", observed=False)[parameter].agg(["mean", "std"]).reset_index().round(2)
        # reverse the stats df because for some reason this gives it to me in the opposite order that it is rendered in
        bench_main_stats = bench_main_stats.iloc[::-1]

        # main plot only uses total phase data
        main_plot = sp.create_main_stripplot(filtered_df[filtered_df["phase"] == "total"], bench_main_stats, parameter)

        formatted_bench_main_stats = []
        # iterate through the rows of the stats df
        for _, row in bench_main_stats.iterrows():
            # create a div that will have the mean and std data in it
            # seperate code for the first block because it should have no margin-top styling
            if  row["model"] == "TIEGCM-Weimer-01":
                stats_label = html.Div(
                    children=["Mean: " + str(row["mean"]), html.Br(), "StD: " + str(row["std"])]
                )
                formatted_bench_main_stats.append(stats_label)
                continue
            stats_label = html.Div(
                children=["Mean: " + str(row["mean"]), html.Br(), "StD: " + str(row["std"])],
                style={"margin-top": "25px"}
            )
            # add the div to the "formatted_bench_main_stats" variable
            formatted_bench_main_stats.append(stats_label)

        # create a plotly plot for each model and add it to "skill_by_phase_plots"
        skills_plots_stats: pd.DataFrame = filtered_df.groupby("phase", observed=False)[parameter].agg(["mean", "std"]).reset_index().round(2)
        skills_by_phase_plots = sp.create_phase_stripplots(filtered_df, skills_plots_stats, parameter)

        # data  preparation for the pivot table (some more pandas magic)
        skills_by_phase: DataFrameGroupBy = filtered_df.groupby(["model", "phase"], observed=False)[parameter]
        skills_by_phase: pd.DataFrame = (
            skills_by_phase.mean()
            .reset_index()
            .pivot(index="model", columns="phase", values=parameter)
            .round(2)
        )
        skills_by_phase.reset_index(inplace=True)
        table_data = skills_by_phase.to_dict("records")

        tpid_list, basic_storm_data = sp.fetch_tpid_data(filtered_df, tpid_base_url)
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
                            figure=main_plot,
                            style={"height": "650px"}
                        ),
                        html.Div(id="bench-main-stats", className="stats", children=formatted_bench_main_stats, style={"top": "320px"})
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


def display_plots(parameter, category, ap_max_threshold, f107_max_threshold, satellites):
    """
    This callback filters thermosphere_df using the input data and populates the plots and table with the filtered dataframe.
    The filtered dataframe is stored in the global variable `filtered_df` so that the tpid callback can access that data
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
    
    # create the elements for the main plot mean and std display
    main_plot_stats: pd.DataFrame = filtered_df.groupby("model", observed=False)[parameter].agg(["mean", "std"]).reset_index().round(2)
    main_plot_stats = main_plot_stats.iloc[::-1]

    # main plot only uses total phase data
    main_plot = sp.create_main_stripplot(filtered_df[filtered_df["phase"] == "total"], main_plot_stats, parameter)

    # make stats labels dash components
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

    # create skills plots stats
    skills_plots_stats: pd.DataFrame = filtered_df.groupby("phase", observed=False)[parameter].agg(["mean", "std"]).reset_index().round(2) 
    skills_by_phase_plots = sp.create_phase_stripplots(filtered_df, skills_plots_stats, parameter)
    
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

    # get tpid data
    tpid_list, basic_storm_data = sp.fetch_tpid_data(filtered_df, tpid_base_url)

    return (
        main_plot, 
        table_data, 
        skills_by_phase_plots,
        formatted_main_plot_stats,
        tpid_list,
        basic_storm_data
    )


def open_tpid_menu():
    """
    This callback creates the links that will be in the tpid popup. It accesses the correct data using the global variable filtered_df
    """
    pass