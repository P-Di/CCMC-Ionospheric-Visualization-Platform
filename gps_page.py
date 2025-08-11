import json, os
import pandas as pd

# Modules to create the dash layout
from dash import html, dcc, dash_table 
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

import thermosphere_page as tp
import numpy as np
import thermosphere_helpers.description_page as dp
# Import the dash library and modules 
import dash
from dash import dcc # Dash core componenets (dcc) for graphs and interactivity
from dash import html # Allows html manipultion within dash
from dash.dependencies import Input, Output, State # Modules for creating callback functions
import dash_bootstrap_components as dbc # Allows for easier webpage formatting

# Modules to create plots and specific components
from gpsLayout import *

from thermosphere_helpers import popups
from thermosphere_page import create_x_button

#{'label': 'GNSS RINEX Data SOPAC', 'value': 'A'},
#                        {'label': 'GNSS RINEX Data CORS', 'value': 'B'}
plot_default=[['DK_F', 'DEF_F2', 'SC_F','DEF_F1'], ['SN_F1', 'SN_F2', 'MS_F', 'RCC'], 1]
options_list = [[
                {'label': 'Dst_kp', 'value' : 'DK_F'},
                {'label': 'CSM2 Models', 'value' : 'DEF_F2'},
                {'label': 'F7/C2 Distribution', 'value' : 'SN_F1'},
                {'label': 'OSSE Change', 'value' : 'DEF_F1'},
                {'label': 'Model Comparison', 'value' : 'SC_F'},
                ],
                [
                {'label': 'Dst_kp', 'value' : 'DK_F'},
                {'label': 'Normalized SS', 'value' : 'SN_F1'},
                {'label': 'Sum_nSS', 'value' : 'SN_F2'},
                {'label': 'Metric_Score', 'value' : 'MS_F'},
                {'label': 'Ratios/CC', 'value' : 'RCC'}],
                [
                {'label': 'Dst_kp', 'value' : 'DK_F'},
                {'label': 'TEC', 'value' : 'DEF_F2'},
                {'label': 'TEC Change', 'value' : 'DEF_F1'},
                {'label': 'Model Comparison', 'value' : 'SC_F'},],
                [
                {'label': 'Dst_kp', 'value' : 'DK_F'},
                {'label': 'Normalized SS', 'value' : 'SN_F1'},
                {'label': 'Sum_nSS', 'value' : 'SN_F2'},                
                {'label': 'Metric_Score', 'value' : 'MS_F'},
                {'label': 'Ratios/CC', 'value' : 'RCC'}]]



base = html.Div(style = {'backgroundColor':'#f4f6f7  ', 'margin': '0'}, children=[  
    html.Div(
        id='ion-main-menu-button',
        children=html.Img(src='assets/menu-icon.svg', width="60px")
    ),
    html.Div(
        id='ionosphere-left-side-bar',
        children=[
            create_x_button("close-ion-main-menu"),
            html.Img(
                id="image1", 
                src=image_paths[0], 
                style={
                    "zIndex": "2",
                    'width': '370px', 
                    'position': 'relative',
                    'background-color': 'white',
                    'border-bottom': '2px solid black',
                    'padding-top': '5px',
                    'padding-bottom': '6px',
                }),
            # Format the window on the left of the webpage to include all the dropdown menus.
            html.Div(
                [
                    html.Div(children=[html.B(children='Project')], style=dstyles[2]),
                    dcc.Dropdown(
                        id='project',
                        options=[
                            {'label': 'Ionosphere Model Validation', 'value': 'IMV'},
                            {'label': 'Thermosphere Neutral Density Assessment', 'value': "TNDA"},
                            {'label': 'Ray Tracing', 'value': 'RT', 'disabled': True},
                            {'label': 'GPS Positioning', 'value': 'GPS'}
                        ], 
                        value = 'IMV'
                    ),
                    html.Div(children=[html.B(children='Storm ID')], style=dstyles[2]),
                    dcc.Dropdown(id='year', options=[
                        {'label': '2013-03-TP-01', 'value': '201303'},
                        {'label': '2021-11-TP-01', 'value': '202111'}], multi=True, value = '202111'),
                    html.Div(children=[html.B(children='Observation')], style=dstyles[2]),
                    dcc.Dropdown(id='observation', options=[                        
                        {'label': 'GNSS Rinex Data', 'value': 'A'},
                        ],
                        multi=True,
                        value='A'),
                    html.Div(children=[html.B(children='Model Type')], style=dstyles[2]),
                    dcc.Dropdown(id='multi',
                        options=model_list[0], multi=True,  value = '0'),
                    dcc.Dropdown(
                    id='task',
                    options=[
                        {'label': 'Hidden Option A', 'value': 'A'},
                        {'label': 'Hidden Option B', 'value': 'B'}
                        ],
                        multi=True,
                        value=[],
                        style={'display': 'none'}  # Always hidden
                        ),
                    html.Div(children=[html.B(children='Plot')], style=dstyles[2]),
                    html.Div(dcc.Dropdown(
                    id='plotts',
                    options=[
                        {'label': 'Dst_kp Indices', 'value': 'A'},
                        {'label': 'TEC RMSE Metric Score', 'value': 'B'},
                        {'label': 'SF PPP 3D Error Metric Score', 'value': 'C'}
                        ],
                        multi=True,
                        value='A',

                        ))
                    
                ],
                id="ion-data-selection-menu", 
                style={"zIndex": "2", 'background-color': 'white', 
                            'padding': '20px', 'height': '100%', 'position': 'relative',
                            'margin-top': '0px','box-shadow': '5px 5px 5px #ededed '
                }
            ),
        ]
    ),
    html.Div(
        id='gps-page',
        children=[
            # Add the properly formatted CCMC image and airflow photo to the top of the page.
            dbc.Tooltip( #Airflow Image Credits.
                "Image Credit: NASA/Don Pettit",
                target="picture_bg", 
                placement="bottom"
            ),
            html.Div(
                id='img_container', 
                children=[ #Airflow Image and text.
                    html.Div(
                        id='text_overlay',
                        children=[
                            html.P(
                                "CCMC ITMAP-Ionosphere-Thermosphere Model Assessment and Validation Platform", 
                                id='text_box', 
                                style={
                                    "zIndex": "4",
                                    'color': 'white', 
                                    'background-color': 'black',
                                    'font-size': '38px', 
                                    'overflowX': 'hidden', 
                                    'white-space': 'nowrap',
                                    'padding-left': '5px',
                                    'padding-top': '9px',
                                    'padding-bottom': '9px',
                                    'margin-bottom': '0px',
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
                    'margin-left' : '20%',
                    'overflowX': 'hidden', 
                    'width':'100%'
                }
            ),
    # Format the window on the left of the webpage to include all the dropdown menus.
    #Format the right 80% of the page, which are created from different graphs that are appended to the children of the rows and columns using a callback.
    dcc.Loading(
        
        html.Div(style={'margin-left' : '20%'},children=[ 
        dcc.Tabs(
            id="tabs",
            style={"zIndex": "1"},
            value="description",
            children=[
                dcc.Tab(label="Description", value="description", style={"background-color": "white", "color": "#e59b1c"}, 
                    selected_style={"background-color": "#e59b1c", "color": "white", "border": "none"}),
                    dcc.Tab(label="Animation", value="animation", style={"background-color": "white", "color": "#e59b1c"}, 
                    selected_style={"background-color": "#e59b1c", "color": "white", "border": "none"}),
                dcc.Tab(label="Analysis Dashboard", value="dashboard", style={"background-color": "white", "color": "#e59b1c"}, 
                    selected_style={"background-color": "#e59b1c", "color": "white", "border": "none"}),
                dcc.Tab(label="Skill Score", value="skill", style={"background-color": "white", "color": "#e59b1c"}, 
                    selected_style={"background-color": "#e59b1c", "color": "white", "border": "none"}),
            ]),
            html.Div(id="tabs-display2") 
        ])),
    ]),
            html.Footer(
            id="ion-footer",
            children=[html.A("Accessibility", href='https://www.nasa.gov/accessibility', target="_blank"), html.Span(children =" | ")          
,html.A("Privacy Policy", href='https://www.nasa.gov/privacy/', target="_blank"), html.Span(children =" | Curators: Paul DiMarzio, Joseph Sypal, and Dr. Min-Yang Chou | NASA Official: Maria Kuznetsova")],
            style={
                'margin-left' : '20%',
                "textAlign": "center",
                "padding": "10px",
                "backgroundColor": "#f1f1f1",
                "position": "relative", 
                "bottom": 0})])


def update_gps_content(tab):
    '''
   callback for gps function
    '''

    if tab == "description":
        # The description tab basically contains a bunch of static html
        return gps_layout
    elif tab == "animation":
        return gps_animation
    elif tab == "analysis":
        return gps_analysis
    elif tab == "skillscore":
        return gps_skillscore