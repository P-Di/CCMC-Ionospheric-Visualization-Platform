import json
import pandas as pd
from dash import html, dcc 
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
                formatted_data["model"].append(model)
                formatted_data["TP"].append(data["events"][key]["TP"])
                formatted_data["category"].append(data["events"][key]["category"])
                formatted_data["satellite"].append(satellite)
                formatted_data["ap_max"].append(data["events"][key]["ap_max"])
                formatted_data["f107_max"].append(data["events"][key]["f107_max"])
                formatted_data["mean_OC"].append(data["events"][key]["satellites"][satellite]["total"]["mean_OC"])
                formatted_data["debias_mean_OC"].append(data["events"][key]["satellites"][satellite]["total"]["debias_mean_OC"])
                formatted_data["stddev_OC"].append(data["events"][key]["satellites"][satellite]["total"]["stddev_OC"])
                formatted_data["R"].append(data["events"][key]["satellites"][satellite]["total"]["R"])

thermosphere_df = pd.DataFrame(formatted_data)

###########################
# Declarations
###########################

ap_thresholds = [80, 132, 207, 236, 300]
f107_thresholds = [70, 100, 150, 200, 250]
image_paths = ['assets/CCMC.png', 'assets/airflow1.jpg']
satellites = [" CHAMP", " GOCE", " GRACE-A", " SWARM-A", " GRACE-FO"]

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
        'backgroundColor':'#f4f6f7  ', 
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
                'background-color': '#f4f6f7  ',
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
                "margin-bottom": "100px",
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
                        dcc.Tab(label="Benchmark", value="benckmark", style={"background-color": "white", "color": "#e59b1c"}, 
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
                "margin-top": "100px",
                "textAlign": "center",
                "padding": "10px",
                "backgroundColor": "#f1f1f1",
                "position": "fixed", 
                "bottom": 0,
                "width": "80%"
            }
        )
    ]
)
