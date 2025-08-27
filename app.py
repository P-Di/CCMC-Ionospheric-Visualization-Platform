#6/10/2024 - Revisions: Deleted imports, check data.py comments to see original.

import numpy as np
import thermosphere_helpers.description_page as dp
# Import the dash library and modules 
import dash
from dash import dcc # Dash core componenets (dcc) for graphs and interactivity
from dash import html # Allows html manipultion within dash
from dash.dependencies import Input, Output, State # Modules for creating callback functions
import dash_bootstrap_components as dbc # Allows for easier webpage formatting

# Import plotly function files for each type of graph.
import plots.dstKpPlot as dstKpPlot
import plots.rcpmPlot as rcpmPlot
import plots.globeDistrPlot as globeDistrPlot
import plots.heatSssmPlot as heatSssmPlot
import plots.skip as skip
import plots.sssmPlot as sssmPlot

import plots.tecRccPlot as tecRccPlot
import multiFunc
import plotSelection
import plots.comparisonPlot as comparisonPlot
import des_tab as dt
# Imports image_paths, dstyles, and gps_layout
from gpsLayout import *

import gps_page as gp
import thermosphere_page as tp

from thermosphere_page import create_x_button
from thermosphere_helpers import popups

#Import data.

csmc2_foF2 = np.load('data/foF2_202111_storm.npz')
csmc2_hmF2 = np.load('data/hmF2_202111_storm.npz')
dst_scatter_map = np.load('data/dst_scatter_map.npz', allow_pickle=True)
image_paths = ['assets/CCMC.png', 'assets/airflow1.jpg']
dstyles = [{'display': 'flex','overflowY': 'scroll','maxHeight': '43vh', 'overflowX': 'auto'}, 
           {'height':'200px', 'width': '320px'}, {'margin-top': '20px', 'margin-bottom': '2px'}, 
           {'height':'100%', 'width': '100%', 'min-width': '600px', 'min-height': '400px'}, {'overflowY': 'scroll', 'overflowX': 'auto'}, 
           { 'height':'40vh', 'width': '100%', 'min-width': '33vh'}, {'height':'200px', 'min-width': '320px', 'width': '100%'}, 
           {'height':'1200px', 'min-width': '600px', 'width': '100%'},
           {'overflowY': 'scroll', "maxHeight":"40vh", 'border-radius': '20px', "backgroundColor": "white", }, {"border" : "none", "margin": "0", "padding": "0", "display": "none",}]
gps_options = [[
                        {'label': 'Dst_kp Indices', 'value': 'A'},
                        {'label': 'TEC RMSE Metric Score', 'value': 'B'},
                        {'label': 'SF PPP 3D Error Metric Score', 'value': 'C'}
                        ],
                        [                        {'label': '3D Error', 'value': 'A'},
                        {'label': '2D Error', 'value': 'B'},
                        {'label': 'East Error', 'value': 'C'},
                        {'label': 'North Error', 'value': 'D'},
                        {'label': 'Up Error', 'value': 'E'},
                        ]]

obs_options=[[
                    {'label': 'Madrigal TEC', 'value': 'TEC'},
                    {'label': 'foF2_COSMIC2', 'value': 'FC2', 'disabled': False},
                    {'label': 'hmF2_COSMIC2', 'value': 'HC2', 'disabled': False},
                    {'label': 'foF2_ionsonde', 'value': 'FI', 'disabled': True},
                    {'label': 'hmF2_ionsonde', 'value': 'HI', 'disabled': True}],
                    [
                    {'label': 'Madrigal TEC', 'value': 'TEC'},
                    {'label': 'foF2_COSMIC2', 'value': 'FC2', 'disabled': True},
                    {'label': 'hmF2_COSMIC2', 'value': 'HC2', 'disabled': True},
                    {'label': 'foF2_ionsonde', 'value': 'FI', 'disabled': True},
                    {'label': 'hmF2_ionsonde', 'value': 'HI', 'disabled': True}]]

#Create error message
error = html.Div(
                "No Comparison Available for Standard Model",
                style={
                    'display': 'flex',
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'height': '100%',
                    'backgroundColor': 'white',
                    'fontSize': '24px',
                    'fontWeight': 'bold',
                    'color': 'black',
                    'width': '100%',
                    'margin-top': '199px',
                    'margin-bottom': '200px',
                }
            )

TITLES=[['Madrigal TEC ','GloTEC ','JPL GIM ','SAMI3 ','SAMI3-RCM ','SAMI3-TIEGCM ','IRI-2016 ','IRI-2020 ','WAM-IPE ','WACCM-X ','TIEGCM-Weimer ', 
        'TIEGCM-Heelis ','CTIPe ','GITM-SWMF ','PBMOD '], ['FORM-7/COS-2 ','GIS_NCKU ','IRI2016 ','IRI2020 ','SAMI3-RCM ','SAMI3-TIEGCM ',
               'SAMI3-ICON ','WACCM-X ','GITM-SWMF ','TIEGCM-Weimer ','TIEGCM-Heelis ','WAM-IPE ','CTIPe '], 
               ['F7/C2 ','GIS_NCKU ','IRI2016 ','IRI2020 ','SMI3-RCM ','SMI3-TGCM ',
               'SMI3-ICN ','WACCM-X ','GTM-SWMF ','TGCM-Wmr ','TGCM-Hls ','WAM-IPE ','CTIPe ']]

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
model_list = []


for i in TITLES:
    sub_op_list = [{'label': 'Show All', 'value' : '15'}]
    for j, k in enumerate(i):
        options_element = {'label': k, 'value': str(j)}
        sub_op_list.append(options_element)
    model_list.append(sub_op_list)
        
# Begin Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title="ITMAP", suppress_callback_exceptions=True)
mathjax = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML'
app.config.suppress_callback_exceptions = True
app.scripts.append_script({ 'external_url' : mathjax })
#Define the layout: Set the background to a light gray, delete all margines.
ionosphere_layout = html.Div(style = {'backgroundColor':'#f4f6f7  ', 'margin': '0'}, children=[  
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
                            {'label': 'GPS Positioning', 'value': 'GPS', 'disabled': True}
                        ], 
                        value = 'IMV'
                    ),
                    html.Div(children=[html.B(children='Storm ID')], style=dstyles[2]),
                    dcc.Dropdown(id='year', options=[
                        {'label': '2013-03-TP-01', 'value': '201303'},
                        {'label': '2021-11-TP-01', 'value': '202111'}], multi=True, value = '202111'),
                    html.Div(children=[html.B(children='Observation')], style=dstyles[2]),
                    dcc.Dropdown(id='observation', options=[
                        {'label': 'Madrigal TEC', 'value': 'TEC'},
                        {'label': 'foF2_COSMIC2', 'value': 'FC2'},
                        {'label': 'hmF2_COSMIC2', 'value': 'HC2'},
                        {'label': 'foF2_ionsonde', 'value': 'FI', 'disabled': True},
                        {'label': 'hmF2_ionsonde', 'value': 'HI', 'disabled': True}], value = 'TEC'),
                    html.Div(children=[html.B(children='Model Type')], style=dstyles[2]),
                    dcc.Dropdown(id='multi',
                        options=model_list[0], multi=True,  value = '0'),
                    html.Div(children=[html.B(children='Task')], style=dstyles[2]),
                    dcc.Dropdown(id='task', options=[
                        {'label': 'Model-Data Comparison', 'value': 'MC'},
                        {'label': 'Skill Scores', 'value': 'SCE'}], value = 'MC'),
                    html.Div(children=[html.B(children='Plot')], style=dstyles[2]),
                    dcc.Dropdown(id='plot',
                        options=options_list[1], multi=True, value = plot_default[0]),
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
        id='ionosphere-page',
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
                    'margin-left': '0px',
                    'overflowX': 'hidden', 
                    'width':'100%'
                }
            ),
    # Format the window on the left of the webpage to include all the dropdown menus.
    #Format the right 80% of the page, which are created from different graphs that are appended to the children of the rows and columns using a callback.
    dcc.Loading(
        
        html.Div(children=[ 
        dcc.Tabs(
            id="tabs",
            style={"zIndex": "1"},
            value="description",
            children=[
                dcc.Tab(label="Description", value="description", style={"background-color": "white", "color": "#e59b1c"}, 
                    selected_style={"background-color": "#e59b1c", "color": "white", "border": "none"}),
                dcc.Tab(label="Analysis Dashboard", value="dashboard", style={"background-color": "white", "color": "#e59b1c"}, 
                    selected_style={"background-color": "#e59b1c", "color": "white", "border": "none"})
            ]),
            html.Div(id="tabs-display") 
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

app.layout = html.Div(
    id="main-content",
    children=ionosphere_layout
)

# create a callback to select which project to display
@app.callback(
        Output("main-content", "children"),
        Input("project", "value")
)
def select_project(project):
    if (project == "TNDA"):
        return tp.thermosphere_layout
    elif (project == "IMV"):
        return ionosphere_layout
    elif (project == "GPS"):
        return gp.base
    
@app.callback(
        [Output("tabs-display2", "children"),
         Output("plotts", "options")],

        Input("tabs", "value")
)
def gps_tabs(tab):
    p = 0
    if tab == "animation":
        p = 1
    return gp.update_gps_content(tab), gps_options[p]
    
@app.callback(
        Output("tabs-display", "children"),
        Input("tabs", "value")
)
def tab_select(tabs):
    if tabs == "description":
        return dt.description_page2
    else:
        display = dbc.Container([
            dbc.Row([
                dbc.Col(html.Div(style={'height': '15px'}), width=12)]),
                dbc.Row([
                
                    dbc.Col([
                        dbc.Card(id = 'child1', style=dstyles[8], children =[])], width=6),
                    dbc.Col([
                        dbc.Card(id = 'child2', style=dstyles[8], children =[])], width=6)
        ]),
            dbc.Row([
                    dbc.Col(html.Div(style={'height': '15px'}), width=12)]),
                dbc.Row([
                    dbc.Col([
                        dbc.Card(id = 'child3', style=dstyles[8], children =[])], width=6),
                    dbc.Col([
                        dbc.Card(id = 'child4', style=dstyles[8], children =[])], width=6)
                        ]),
            dbc.Row([
                dbc.Col(
                    html.Div(style={'height': '15px'}), width=12)]),
                dbc.Row([
                    dbc.Col([
                        dbc.Card(id = 'child5', style=dstyles[8], children =[])], width=6),
                    dbc.Col([
                        dbc.Card(id = 'child6', style=dstyles[8], children =[])], width=6)
                        ]),
            dbc.Row([
                dbc.Col(
                    html.Div(style={'height': '15px'}), width=12)]),
                dbc.Row([
                    dbc.Col([
                        dbc.Card(id = 'child7', style=dstyles[8], children =[])], width=6),
                    dbc.Col([
                        dbc.Card(id = 'child8', style=dstyles[8], children =[])], width=6),
                    ])
        ], fluid=True)
        return display

# Create one callback to handle all graphs, with the input from all the sidebar buttons.
@app.callback(
        [Output('child1', 'children'),
         Output('child2', 'children'),
         Output('child3', 'children'),
         Output('child4', 'children'),
         Output('child5', 'children'),
         Output('child6', 'children'),
         Output('child7', 'children'),
         Output('child8', 'children'),
         Output('child1', 'style'),
         Output('child2', 'style'),
         Output('child3', 'style'),
         Output('child4', 'style'),
         Output('child5', 'style'),
         Output('child6', 'style'),
         Output('child7', 'style'),
         Output('child8', 'style'),
         Output('multi', 'value'),
         Output('multi', 'options'),
         Output('plot', 'options'),
         Output('observation', 'options'),
         Output('year', 'value'),
         Output('year', 'disabled'),
         Output('task', 'disabled'),
         Output('plot', 'value'),
         ],
        [Input('multi', 'value'),
         Input('year', 'value'),
         Input('task', 'value'),
         Input('plot', 'value'),
         Input('observation', 'value'),
         ]
)
def update_graph(multi, yearids, task, plot, obs):
    
    # Combine the TEC data from Cosmic 2.
    TEC_foF2 = np.concatenate([[csmc2_foF2['C2_foF2_map']], csmc2_foF2['All_model_fof2']])
    TEC_hmF2 = np.concatenate([[csmc2_hmF2['C2_hmF2_map']], csmc2_hmF2['All_model_hmf2']])
    
    plot_options =['DEF_F1', 'DK_F','DEF_F2', 'MS_F', 'SN_F1', 'SN_F2', 'RCC','SC_F']
    if isinstance(yearids, list) and len(yearids) == 2:
        yearid = yearids[0]
        year2id = yearids[1]
        year = yearid[:4]
        year2 = year2id[:4]
        chosen_year2 = np.load('data/MTEC_'+year2id+'_storm.npz')
        fig2=dstKpPlot.dst_kp_plot(int(year2), dst_scatter_map['dst_'+year2])
        child_multi2, child_tec2, multi2, cm2, child_osse2 = multiFunc.tec_formatting(multi, obs, task, [chosen_year2, TEC_foF2, TEC_hmF2], year2, TITLES, dstyles)
        if year == '2013' or year2 == '2013': obs_op = obs_options[1]
        else: obs_op = obs_options[0]
        graphs2 = [
            child_multi2,
            dcc.Graph(style=dstyles[3], figure=fig2),
            child_tec2, 
            dcc.Graph(style=dstyles[3], figure=rcpmPlot.rcpm_plot(chosen_year2['Alldata'], year2, TITLES[0], [[0, 30], [-15, 15], [0, 1.2], [-25, 25], "TEC"])),
            dcc.Graph(style=dstyles[3], figure=skip.heatmap_sssm_plot(chosen_year2['allphase'], "TEC", year2, TITLES[0])),
            dcc.Graph(style=dstyles[3], figure=sssmPlot.skill_scores_sum_plot(chosen_year2['All_nss'], year2, TITLES[0], "TEC")),
            dcc.Graph(style=dstyles[3], figure=tecRccPlot.tec_rcc_plot(chosen_year2['CC'], chosen_year2['RP_par'], chosen_year2['MP_par'], year2, TITLES[0], [[0, 200], [0, 200], ["Ratio(80th-20th)", "Ratio(80th)", "TC_80th", "TC(80th)-TC(20th)", "TEC"]])),
            child_tec2 #Placeholder for model_comparison_plot
            ]
        cm2 = list(map(int, cm2))
        # Swap in Model comparison plot
        if len(cm2) == 1 and cm2[0] == 0: graphs2[-1] = error
        else:
            graphs2[-1] = dcc.Graph(style=dstyles[3], figure=comparisonPlot.model_comparison_plot(chosen_year2['TEC_all'][0], chosen_year2['TEC_all'], TITLES[0], cm2, dst_scatter_map['z_' + year2], year2))
        
        
    else:
        if isinstance(yearids, list): yearids = yearids[0]
        yearid = yearids
        year = yearid[:4]
        graphs2 = [None, None, None, None, None, None, None, None] 
        chl2 = [None, None, None, None, None, None, None, None]
        if year == '2013': obs_op = obs_options[1]
        else: obs_op = obs_options[0]


    fig1=dstKpPlot.dst_kp_plot(int(year), dst_scatter_map['dst_'+year])
    chosen_year = np.load('data/MTEC_'+yearid+'_storm.npz')

    # These are conditionals to set up the TEC plot children. They are specially set up to  
    #   contain multiple different graphs since multiple TEC plots can be selected at once.
    child_multi, child_tec, multi, cm, child_osse  = multiFunc.tec_formatting(multi, obs, task, [chosen_year, TEC_foF2, TEC_hmF2], year, TITLES, dstyles)
    # If no values have been selected for plot, change it to an empty string.
    if plot == None: plot = ['']
    if year == '2013': obs_op = obs_options[1]
    else: obs_op = obs_options[0]

    child1 = dcc.Graph(style=dstyles[3], figure=globeDistrPlot.c2_map_plot(dst_scatter_map['c2_lon'], dst_scatter_map['c2_lat'], dst_scatter_map['II_list']))
    plot_options = ['DEF_F1', 'DK_F','DEF_F2', 'MS_F', 'SN_F1', 'SN_F2', 'RCC','SC_F']
    if obs == 'FC2':
        # A list of all possible selected graphs.
        if task == "SCE":
            options_list_final = options_list[1]
            first_graph = dcc.Graph(style=dstyles[3], figure=skip.heatmap_sssm_plot(csmc2_foF2['allphase'], "foF2", '2021', TITLES[1]))
            if plot_default[2] == 0:
                plot_value = plot_default[1]
                plot_default[2] = 1
                plot = plot_value
            else:
                plot_value = plot
        else:
            options_list_final = options_list[0]
            first_graph = child1
            if plot_default[2] == 1:
                plot_value = plot_default[0]
                plot = plot_value
                plot_default[2] = 0

            else:
                plot_value = plot
        plot_value = plot
        graphs = [ 
                    child_osse,
                    dcc.Graph(style=dstyles[3], figure=fig1),
                    child_multi,
                    dcc.Graph(style=dstyles[3], figure=rcpmPlot.rcpm_plot(csmc2_foF2['Alldata'], '2021', TITLES[1], [[0,10],[-5,5],[0,1.2],[-5,5], "foF2"])),
                    first_graph,
                    dcc.Graph(style=dstyles[3], figure=sssmPlot.skill_scores_sum_plot(csmc2_foF2['All_nss'], '2021', TITLES[1], "foF2")),
                    dcc.Graph(style=dstyles[3], figure=tecRccPlot.tec_rcc_plot(csmc2_foF2['CC'], csmc2_foF2['RP_par'], csmc2_foF2['MP_par'], '2021', TITLES[1], [[0, 200], [0, 100], ["Ratio(95th-5th)", "Ratio_95th",  "RD_95th", "RD(95th)-RD(5th)", "foF2"]])),
                    child_multi #Placeholder for model_comparison_plot
                ]
        # Generate the comparison graph based off all selected model excluding comparison model.
        cm = list(map(int, cm))
        # Swap in Model comparison plot
        if len(cm) == 1 and cm[0] == 0: graphs[-1] = error 
        else:      
            graphs[-1] = dcc.Graph(style=dstyles[3], figure=comparisonPlot.model_comparison_plot(TEC_foF2[0], TEC_foF2, TITLES[1], cm, dst_scatter_map['z_foF2'], year))
        # Add selected plots and take out others.
        chl, style_sel = plotSelection.plot_selection_format(plot, plot_options, graphs)
        return chl[0], chl[1], chl[2], chl[3], chl[4], chl[5], chl[6],chl[7], dstyles[style_sel[0]],dstyles[style_sel[1]],dstyles[style_sel[2]],dstyles[style_sel[3]],dstyles[style_sel[4]],dstyles[style_sel[5]],dstyles[style_sel[6]],dstyles[style_sel[7]],multi, model_list[1], options_list_final, obs_options[0], yearids, True, False, plot_value
    
    elif obs == 'HC2':
        if task == "SCE":
            options_list_final = options_list[1]
            first_graph = dcc.Graph(style=dstyles[3], figure=skip.heatmap_sssm_plot(csmc2_hmF2['allphase'], "hmF2", '2021', TITLES[1])),
            if plot_default[2] == 0:
                plot_value = plot_default[1]
                plot_default[2] = 1
                plot = plot_value
            else:
                plot_value = plot
        else:
            options_list_final = options_list[0]
            first_graph = child1
            if plot_default[2] == 1:
                plot_value = plot_default[0]
                plot = plot_value
                plot_default[2] = 0

            else:
                plot_value = plot
        plot_value = plot
        graphs = [
                    child_osse,
                    dcc.Graph(style=dstyles[3], figure=fig1),
                    child_multi,
                    dcc.Graph(style=dstyles[3], figure=rcpmPlot.rcpm_plot(csmc2_hmF2['Alldata'], '2021', TITLES[1], [[0,200],[-50,100],[0,1],[-100,100], "hmF2"])),
                    first_graph,
                    dcc.Graph(style=dstyles[3], figure=sssmPlot.skill_scores_sum_plot(csmc2_hmF2['All_nss'], '2021', TITLES[1], "hmF2")),
                    dcc.Graph(style=dstyles[3], figure=tecRccPlot.tec_rcc_plot(csmc2_hmF2['CC'], csmc2_hmF2['RP_par'], csmc2_hmF2['MP_par'], '2021', TITLES[1], [[0, 150], [0, 100], ["Ratio(90th-10th)", "Ratio_90th", "TC_90th", "TC(90th)-TC(10th)", "hmF2"]])),
                    child_multi #Placeholder for model_comparison_plot
                ]
        # Generate the comparison graph based off all selected model excluding comparison model.
        cm = list(map(int, cm))
        # Swap in Model comparison plot
        if len(cm) == 1 and cm[0] == 0: graphs[-1] = error 
        else:      
            graphs[-1] = dcc.Graph(style=dstyles[3], figure=comparisonPlot.model_comparison_plot(TEC_hmF2[0], TEC_hmF2, TITLES[1], cm, dst_scatter_map['z_hmF2'], year))
        # Add selected plots and take out others.
        chl, style_sel = plotSelection.plot_selection_format(plot, plot_options, graphs)
        return chl[0], chl[1], chl[2], chl[3], chl[4], chl[5], chl[6],chl[7],dstyles[style_sel[0]],dstyles[style_sel[1]],dstyles[style_sel[2]],dstyles[style_sel[3]],dstyles[style_sel[4]],dstyles[style_sel[5]],dstyles[style_sel[6]],dstyles[style_sel[7]], multi, model_list[1], options_list_final, obs_options[0], yearids, True, False, plot_value 
    

    else:
        if task == 'SCE':
            if plot_default[2] == 0:
                plot_value = plot_default[1]
                plot_default[2] = 1
                plot = plot_value

            else:
                plot_value = plot
            graphs = [
                        child_multi,
                        dcc.Graph(style=dstyles[3], figure=fig1),
                        child_tec, 
                        dcc.Graph(style=dstyles[3], figure=rcpmPlot.rcpm_plot(chosen_year['Alldata'], year, TITLES[0], [[0, 30], [-15, 15], [0, 1.2], [-25, 25], "TEC"])),
                        dcc.Graph(style=dstyles[3], figure=skip.heatmap_sssm_plot(chosen_year['allphase'], "TEC", year, TITLES[0])),
                        dcc.Graph(style=dstyles[3], figure=sssmPlot.skill_scores_sum_plot(chosen_year['All_nss'], year, TITLES[0], "TEC")),
                        dcc.Graph(style=dstyles[3], figure=tecRccPlot.tec_rcc_plot(chosen_year['CC'], chosen_year['RP_par'], chosen_year['MP_par'], year, TITLES[0], [[0, 200], [0, 200], ["Ratio(80th-20th)", "Ratio(80th)", "TC_80th", "TC(80th)-TC(20th)", "TEC"]])),
                        child_tec #Placeholder for model_comparison_plot
                    ]
            cm = list(map(int, cm))
            # Swap in Model comparison plot
            if len(cm) == 1 and cm[0] == 0: graphs[-1] = error 
            else:      
                graphs[-1] = dcc.Graph(style=dstyles[3], figure=comparisonPlot.model_comparison_plot(chosen_year['TEC_all'][0], chosen_year['TEC_all'], TITLES[0], cm, dst_scatter_map['z_' + year], year))
            # Generate the comparison graph based off all selected model excluding comparison model.
            plot_options = ['DEF_F1', 'DK_F','DEF_F2', 'MS_F', 'SN_F1', 'SN_F2', 'RCC','SC_F']
            chl2, style_sel2 = plotSelection.plot_selection_format(plot, plot_options, graphs2)
            chl, style_sel = plotSelection.plot_selection_format(plot, plot_options, graphs)
            if chl2[0] != None:
                chl.insert(1, chl2[0])
                style_sel.insert(1, 8)
                chl.insert(3, chl2[1])
                style_sel.insert(3, 8)
                chl.insert(5, chl2[2])
                style_sel.insert(5, 8)
                chl.insert(7, chl2[3])
                style_sel.insert(7, 8)
            # Add selected plots and take out others.
            return chl[0], chl[1], chl[2], chl[3], chl[4], chl[5], chl[6], chl[7], dstyles[style_sel[0]],dstyles[style_sel[1]],dstyles[style_sel[2]],dstyles[style_sel[3]],dstyles[style_sel[4]],dstyles[style_sel[5]],dstyles[style_sel[6]],dstyles[style_sel[7]],multi, model_list[0], options_list[3], obs_op, yearids, False, False, plot_value

        else:
            if plot_default[2] == 1:
                plot_value = plot_default[0]
                plot = plot_value
                plot_default[2] = 0

            else:
                plot_value = plot

            graphs = [
                        child_multi,
                        dcc.Graph(style=dstyles[3], figure=fig1),
                        child_tec, 
                        dcc.Graph(style=dstyles[3], figure=rcpmPlot.rcpm_plot(chosen_year['Alldata'], year, TITLES[0], [[0, 30], [-15, 15], [0, 1.2], [-25, 25], "TEC"])),
                        dcc.Graph(style=dstyles[3], figure=skip.heatmap_sssm_plot(chosen_year['allphase'], "TEC", year, TITLES[0])),
                        dcc.Graph(style=dstyles[3], figure=sssmPlot.skill_scores_sum_plot(chosen_year['All_nss'], year, TITLES[0], "TEC")),
                        dcc.Graph(style=dstyles[3], figure=tecRccPlot.tec_rcc_plot(chosen_year['CC'], chosen_year['RP_par'], chosen_year['MP_par'], year, TITLES[0], [[0, 200], [0, 200], ["Ratio(80th-20th)", "Ratio(80th)", "TC_80th", "TC(80th)-TC(20th)", "TEC"]])),
                        child_tec #Placeholder for model_comparison_plot
                    ]
            child1 = dcc.Graph(style=dstyles[3], figure=fig1)
            # Generate the comparison graph based off all selected model excluding comparison model.
            cm = list(map(int, cm))
            # Swap in Model comparison plot
            if len(cm) == 1 and cm[0] == 0: graphs[-1] = error 
            else:     
                graphs[-1] = dcc.Graph(style=dstyles[3], figure=comparisonPlot.model_comparison_plot(chosen_year['TEC_all'][0], chosen_year['TEC_all'], TITLES[0], cm, dst_scatter_map['z_' + year], year))
            plot_options = ['DEF_F1', 'DK_F','DEF_F2', 'MS_F', 'SN_F1', 'SN_F2', 'RCC','SC_F']
            chl2, style_sel2 = plotSelection.plot_selection_format(plot, plot_options, graphs2)
            chl, style_sel = plotSelection.plot_selection_format(plot, plot_options, graphs)
            if chl2[0] != None:
                chl.insert(1, chl2[0])
                style_sel.insert(1, 8)
                chl.insert(3, chl2[1])
                style_sel.insert(3, 8)
                chl.insert(5, chl2[2])
                style_sel.insert(5, 8)
                chl.insert(7, chl2[3])
                style_sel.insert(7, 8)

            return chl[0], chl[1], chl[2], chl[3], chl[4], chl[5], chl[6], chl[7],dstyles[style_sel[0]],dstyles[style_sel[1]],dstyles[style_sel[2]],dstyles[style_sel[3]],dstyles[style_sel[4]],dstyles[style_sel[5]],dstyles[style_sel[6]],dstyles[style_sel[7]],  multi, model_list[0], options_list[2], obs_op, yearids, False, False, plot_value

        
# The following callbacks are all used to update elements of the thermosphere page
# For the sake of keeping all the thermosphere code together, I implemented the callbacks in thermosphere_page.py and 
#   simply called those functions in their respective callbacks in this file
@app.callback(
    Output("thermosphere-main-content", "children"),
    [Input("tabs", "value"),
     Input("parameter_selection", "value")]
)
def update_thermosphere_content(tab, parameter):
    """
    Callback to switch between tabs (Description, Analysis Dashboard, Benchmark) on the thermosphere page.
    """
    return tp.update_content(tab, parameter)

@app.callback(
    [Output("skills-by-event-plot", "figure"),
     Output("skills-by-phase-table", "data"),
     Output("skills-by-phase-plots", "children"),
    #  Output("main-plot-stats", "children"),
     Output("tpid-list", "children"),
     Output("basic-storm-data", "children")],
    [Input("parameter_selection", "value"),
     Input("category_selections", "value"),
     Input("ap_max_slider", "value"),
     Input("f107_max_slider", "value"),
     Input("satellites", "value"),
     Input("models", "value")]
)
def display_thermosphere_plots(parameter, category, ap_max_threshold, f107_max_threshold, satellites, models):
    """
    This callback is called whenever the user changes some data selection and it updates the data displayed on the page.
    """
    (
        main_plot,
        table_data,
        skills_by_phase_plots,
        _,
        tpid_list,
        basic_storm_data
    ) = tp.display_plots(parameter, category, ap_max_threshold, f107_max_threshold, satellites, models)
    return main_plot, table_data, skills_by_phase_plots, tpid_list, basic_storm_data


@app.callback(
    [Output("tpid-menu", "style")],
    [Input("tpid-menu-button-1", "n_clicks"),
     Input("tpid-menu-button-2", "n_clicks")],
    prevent_initial_call=True
)
def open_thermosphere_tpid_menu(n_clicks_1, n_clicks_2):
    """
    This callback only displays the tpid popup, that values are populated in the `display_thermosphere_plots` callback.
    This alows the tpid popup to update immediately when the data selection changes (i.e., the user does not need to 
    close the popup and re-open it for the changes to be reflected.)
    """
    return [{"display": "block"}]

@app.callback(
    Output("tpid-menu", "style", allow_duplicate=True),
    Input("tpid-x-button", "n_clicks"),
    prevent_initial_call=True
)
def close_thermosphere_tpid_menu(n_clicks):
    return {"display": "none"}

@app.callback(
    Output("fig-1-collapse", "is_open"),
    Input("fig-1-btn", "n_clicks"),
    State("fig-1-collapse", "is_open"),
)
def toggle_fig1_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("fig-2-collapse", "is_open"),
    Input("fig-2-btn", "n_clicks"),
    State("fig-2-collapse", "is_open")
)
def toggle_fig2_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("phase-table-collapse", "is_open"),
    Input("phase-table-btn", "n_clicks"),
    State("phase-table-collapse", "is_open")
)
def toggle_phase_table_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("comp-collapse", "is_open"),
    Input("comp-btn", "n_clicks"),
    State("comp-collapse", "is_open")
)
def toggle_comp_collapse(n, is_open):
    """
    callback to toggle the computations displayed on the description page
    """
    if n:
        return not is_open
    return is_open

@app.callback(
    [Output("satellite-description-popup", "style"),
     Output("satellite-description-data", "children")],
    [Input("CHAMP-label", "n_clicks"),
     Input("GOCE-label", "n_clicks"),
     Input("GRACE-A-label", "n_clicks"),
     Input("SWARM-A-label", "n_clicks"),
     Input("GRACE-FO-label", "n_clicks"),
     Input("MSISE00-01-label", "n_clicks"),
     Input("MSIS20-01-label", "n_clicks"),
     Input("JB2008-01-label", "n_clicks"),
     Input("DTM2020-01-label", "n_clicks"),
     Input("DTM2013-01-label", "n_clicks"),
     Input("TIEGCM-Weimer-01-label", "n_clicks"),
     Input("TIEGCM-Heelis-01-label", "n_clicks"),
     Input("WACCMX-Weimer-01-label", "n_clicks"),
     Input("WACCMX-Heelis-01-label", "n_clicks"),
     Input("GITM-01-label", "n_clicks"),
     Input("WAM-IPE-label", "n-clicks")],
    prevent_initial_call=True
)
def open_description_popup(CHAMP_clicks, GOCE_clicks, GRACE_A_clicks, SWARM_A_clicks, GRACE_FO_clicks,
                                     MSISE00_01_clicks, MSIS20_01_clicks, JB2008_01_clicks, DTM2020_01_clicks,
                                     DTM2013_01_clicks, TIEGCM_Weimer_01_clicks, TIEGCM_Heelis_01_clicks, 
                                     WACCMX_Weimer_01_clicks, WACCMX_Heelis_01_clicks, GITM_01_clicks, WAM_IPE_clicks):
    """
    :Description:

    This callback handles opening and populating the popup for the satellite and model info. It is triggered by 
    a change to the n_clicks property for any of the checklist labels (n_clicks is initially set to 0). When the 
    popup is closed, all label's n_clicks property are set to 0. This ensures that whenever a label is clicked,
    that label's n_clicks property will be 1 and all other n_clicks properties will be 0.
    """

    # CHAMP click
    if (CHAMP_clicks == 1 and GOCE_clicks == 0 and GRACE_A_clicks == 0 and SWARM_A_clicks == 0 
          and GRACE_FO_clicks == 0 and MSISE00_01_clicks == 0 and MSIS20_01_clicks == 0
          and JB2008_01_clicks == 0 and DTM2020_01_clicks == 0 and DTM2013_01_clicks == 0
          and TIEGCM_Weimer_01_clicks == 0 and TIEGCM_Heelis_01_clicks == 0 and WACCMX_Weimer_01_clicks == 0 
          and WACCMX_Heelis_01_clicks == 0 and GITM_01_clicks == 0 and WAM_IPE_clicks == 0):

        return {"display": "block"}, popups.gen_CHAMP_data()
    
    # GOCE click
    elif (CHAMP_clicks == 0 and GOCE_clicks == 1 and GRACE_A_clicks == 0 and SWARM_A_clicks == 0 
          and GRACE_FO_clicks == 0 and MSISE00_01_clicks == 0 and MSIS20_01_clicks == 0
          and JB2008_01_clicks == 0 and DTM2020_01_clicks == 0 and DTM2013_01_clicks == 0
          and TIEGCM_Weimer_01_clicks == 0 and TIEGCM_Heelis_01_clicks == 0 and WACCMX_Weimer_01_clicks == 0 
          and WACCMX_Heelis_01_clicks == 0 and GITM_01_clicks == 0 and WAM_IPE_clicks == 0):
        
        return {"display": "block"}, popups.gen_GOCE_data()
    
    # GRACE-A click
    elif (CHAMP_clicks == 0 and GOCE_clicks == 0 and GRACE_A_clicks == 1 and SWARM_A_clicks == 0 
          and GRACE_FO_clicks == 0 and MSISE00_01_clicks == 0 and MSIS20_01_clicks == 0
          and JB2008_01_clicks == 0 and DTM2020_01_clicks == 0 and DTM2013_01_clicks == 0
          and TIEGCM_Weimer_01_clicks == 0 and TIEGCM_Heelis_01_clicks == 0 and WACCMX_Weimer_01_clicks == 0 
          and WACCMX_Heelis_01_clicks == 0 and GITM_01_clicks == 0 and WAM_IPE_clicks == 0):
        
        return {"display": "block"}, popups.gen_GRACE_A_data()
    
    # SWARM-A click
    elif (CHAMP_clicks == 0 and GOCE_clicks == 0 and GRACE_A_clicks == 0 and SWARM_A_clicks == 1
          and GRACE_FO_clicks == 0 and MSISE00_01_clicks == 0 and MSIS20_01_clicks == 0
          and JB2008_01_clicks == 0 and DTM2020_01_clicks == 0 and DTM2013_01_clicks == 0
          and TIEGCM_Weimer_01_clicks == 0 and TIEGCM_Heelis_01_clicks == 0 and WACCMX_Weimer_01_clicks == 0 
          and WACCMX_Heelis_01_clicks == 0 and GITM_01_clicks == 0 and WAM_IPE_clicks == 0):
        
        return {"display": "block"}, popups.gen_SWARM_A_data()
    
    # GRACE-FO click
    elif (CHAMP_clicks == 0 and GOCE_clicks == 0 and GRACE_A_clicks == 0 and SWARM_A_clicks == 0 
          and GRACE_FO_clicks == 1 and MSISE00_01_clicks == 0 and MSIS20_01_clicks == 0
          and JB2008_01_clicks == 0 and DTM2020_01_clicks == 0 and DTM2013_01_clicks == 0
          and TIEGCM_Weimer_01_clicks == 0 and TIEGCM_Heelis_01_clicks == 0 and WACCMX_Weimer_01_clicks == 0 
          and WACCMX_Heelis_01_clicks == 0 and GITM_01_clicks == 0 and WAM_IPE_clicks == 0):
        
        return {"display": "block"}, popups.gen_GRACE_FO_data()
    
    # MSISE00_01 click
    elif (CHAMP_clicks == 0 and GOCE_clicks == 0 and GRACE_A_clicks == 0 and SWARM_A_clicks == 0 
          and GRACE_FO_clicks == 0 and MSISE00_01_clicks == 1 and MSIS20_01_clicks == 0
          and JB2008_01_clicks == 0 and DTM2020_01_clicks == 0 and DTM2013_01_clicks == 0
          and TIEGCM_Weimer_01_clicks == 0 and TIEGCM_Heelis_01_clicks == 0 and WACCMX_Weimer_01_clicks == 0 
          and WACCMX_Heelis_01_clicks == 0 and GITM_01_clicks == 0 and WAM_IPE_clicks == 0):

        return {"display": "block"}, popups.gen_MSISE00_01_data()

    # MSIS20_01 click
    elif (CHAMP_clicks == 0 and GOCE_clicks == 0 and GRACE_A_clicks == 0 and SWARM_A_clicks == 0 
          and GRACE_FO_clicks == 0 and MSISE00_01_clicks == 0 and MSIS20_01_clicks == 1
          and JB2008_01_clicks == 0 and DTM2020_01_clicks == 0 and DTM2013_01_clicks == 0
          and TIEGCM_Weimer_01_clicks == 0 and TIEGCM_Heelis_01_clicks == 0 and WACCMX_Weimer_01_clicks == 0 
          and WACCMX_Heelis_01_clicks == 0 and GITM_01_clicks == 0 and WAM_IPE_clicks == 0):
        
        return {"display": "block"}, popups.gen_MSIS20_01_data()
    
    # JB2008-01 click
    elif (CHAMP_clicks == 0 and GOCE_clicks == 0 and GRACE_A_clicks == 0 and SWARM_A_clicks == 0 
          and GRACE_FO_clicks == 0 and MSISE00_01_clicks == 0 and MSIS20_01_clicks == 0
          and JB2008_01_clicks == 1 and DTM2020_01_clicks == 0 and DTM2013_01_clicks == 0
          and TIEGCM_Weimer_01_clicks == 0 and TIEGCM_Heelis_01_clicks == 0 and WACCMX_Weimer_01_clicks == 0 
          and WACCMX_Heelis_01_clicks == 0 and GITM_01_clicks == 0 and WAM_IPE_clicks == 0):

        return {"display": "block"}, popups.gen_JB2008_01_data()
    
    # DTM2020-01 click
    elif (CHAMP_clicks == 0 and GOCE_clicks == 0 and GRACE_A_clicks == 0 and SWARM_A_clicks == 0 
          and GRACE_FO_clicks == 0 and MSISE00_01_clicks == 0 and MSIS20_01_clicks == 0
          and JB2008_01_clicks == 0 and DTM2020_01_clicks == 1 and DTM2013_01_clicks == 0
          and TIEGCM_Weimer_01_clicks == 0 and TIEGCM_Heelis_01_clicks == 0 and WACCMX_Weimer_01_clicks == 0 
          and WACCMX_Heelis_01_clicks == 0 and GITM_01_clicks == 0 and WAM_IPE_clicks == 0):
        
        return {"display": "block"}, popups.gen_DTM2020_01_data()
    
    # DTM2013-01 click
    elif (CHAMP_clicks == 0 and GOCE_clicks == 0 and GRACE_A_clicks == 0 and SWARM_A_clicks == 0 
          and GRACE_FO_clicks == 0 and MSISE00_01_clicks == 0 and MSIS20_01_clicks == 0
          and JB2008_01_clicks == 0 and DTM2020_01_clicks == 0 and DTM2013_01_clicks == 1
          and TIEGCM_Weimer_01_clicks == 0 and TIEGCM_Heelis_01_clicks == 0 and WACCMX_Weimer_01_clicks == 0 
          and WACCMX_Heelis_01_clicks == 0 and GITM_01_clicks == 0 and WAM_IPE_clicks == 0):
        
        return {"display": "block"}, popups.gen_DTM2013_01_data()
    
    # TIEGCM-Weimer-01 click
    elif (CHAMP_clicks == 0 and GOCE_clicks == 0 and GRACE_A_clicks == 0 and SWARM_A_clicks == 0 
          and GRACE_FO_clicks == 0 and MSISE00_01_clicks == 0 and MSIS20_01_clicks == 0
          and JB2008_01_clicks == 0 and DTM2020_01_clicks == 0 and DTM2013_01_clicks == 0
          and TIEGCM_Weimer_01_clicks == 1 and TIEGCM_Heelis_01_clicks == 0 and WACCMX_Weimer_01_clicks == 0 
          and WACCMX_Heelis_01_clicks == 0 and GITM_01_clicks == 0 and WAM_IPE_clicks == 0):
        
        return {"display": "block"}, popups.gen_TIEGCM_Weimer_01_data()
    
    # TIEGCM-Heelis-01 click
    elif (CHAMP_clicks == 0 and GOCE_clicks == 0 and GRACE_A_clicks == 0 and SWARM_A_clicks == 0 
          and GRACE_FO_clicks == 0 and MSISE00_01_clicks == 0 and MSIS20_01_clicks == 0
          and JB2008_01_clicks == 0 and DTM2020_01_clicks == 0 and DTM2013_01_clicks == 0
          and TIEGCM_Weimer_01_clicks == 0 and TIEGCM_Heelis_01_clicks == 1 and WACCMX_Weimer_01_clicks == 0 
          and WACCMX_Heelis_01_clicks == 0 and GITM_01_clicks == 0 and WAM_IPE_clicks == 0):
        
        return {"display": "block"}, popups.gen_TIEGCM_Heelis_01_data()
    
    # WACCMX-Weimer-01 click
    elif (CHAMP_clicks == 0 and GOCE_clicks == 0 and GRACE_A_clicks == 0 and SWARM_A_clicks == 0 
          and GRACE_FO_clicks == 0 and MSISE00_01_clicks == 0 and MSIS20_01_clicks == 0
          and JB2008_01_clicks == 0 and DTM2020_01_clicks == 0 and DTM2013_01_clicks == 0
          and TIEGCM_Weimer_01_clicks == 0 and TIEGCM_Heelis_01_clicks == 0 and WACCMX_Weimer_01_clicks == 1 
          and WACCMX_Heelis_01_clicks == 0 and GITM_01_clicks == 0 and WAM_IPE_clicks == 0):

        return {"display": "block"}, popups.gen_WACCMX_Weimer_01_data()

    # WACCMX-Heelis-01 click
    elif (CHAMP_clicks == 0 and GOCE_clicks == 0 and GRACE_A_clicks == 0 and SWARM_A_clicks == 0 
          and GRACE_FO_clicks == 0 and MSISE00_01_clicks == 0 and MSIS20_01_clicks == 0
          and JB2008_01_clicks == 0 and DTM2020_01_clicks == 0 and DTM2013_01_clicks == 0
          and TIEGCM_Weimer_01_clicks == 0 and TIEGCM_Heelis_01_clicks == 0 and WACCMX_Weimer_01_clicks == 0 
          and WACCMX_Heelis_01_clicks == 1 and GITM_01_clicks == 0 and WAM_IPE_clicks == 0):

        return {"display": "block"}, popups.gen_WACCMX_Heelis_01_data()

    # GITM-01 click
    elif (CHAMP_clicks == 0 and GOCE_clicks == 0 and GRACE_A_clicks == 0 and SWARM_A_clicks == 0 
          and GRACE_FO_clicks == 0 and MSISE00_01_clicks == 0 and MSIS20_01_clicks == 0
          and JB2008_01_clicks == 0 and DTM2020_01_clicks == 0 and DTM2013_01_clicks == 0
          and TIEGCM_Weimer_01_clicks == 0 and TIEGCM_Heelis_01_clicks == 0 and WACCMX_Weimer_01_clicks == 0 
          and WACCMX_Heelis_01_clicks == 0 and GITM_01_clicks == 1 and WAM_IPE_clicks == 0):
        
        return {"display": "block"}, popups.gen_GITM_01_data()

    # WAM-IPE
    elif (CHAMP_clicks == 0 and GOCE_clicks == 0 and GRACE_A_clicks == 0 and SWARM_A_clicks == 0 
          and GRACE_FO_clicks == 0 and MSISE00_01_clicks == 0 and MSIS20_01_clicks == 0
          and JB2008_01_clicks == 0 and DTM2020_01_clicks == 0 and DTM2013_01_clicks == 0
          and TIEGCM_Weimer_01_clicks == 0 and TIEGCM_Heelis_01_clicks == 0 and WACCMX_Weimer_01_clicks == 0 
          and WACCMX_Heelis_01_clicks == 0 and GITM_01_clicks == 0 and WAM_IPE_clicks == 1):

        return {"display": "block"}, popups.gen_WAM_IPE_data() 

    # No click. This state is necessary because setting all n_clicks values to 0 when the x button is clicked 
    # triggers this callback.
    elif (CHAMP_clicks == 0 and GOCE_clicks == 0 and GRACE_A_clicks == 0 and SWARM_A_clicks == 0 
          and GRACE_FO_clicks == 0 and MSISE00_01_clicks == 0 and MSIS20_01_clicks == 0
          and JB2008_01_clicks == 0 and DTM2020_01_clicks == 0 and DTM2013_01_clicks == 0
          and TIEGCM_Weimer_01_clicks == 0 and TIEGCM_Heelis_01_clicks == 0 and WACCMX_Weimer_01_clicks == 0 
          and WACCMX_Heelis_01_clicks == 0 and GITM_01_clicks == 0 and WAM_IPE_clicks == 0):
        
        return {"display": "none"}, ""

    # Error
    else:
        print("Unrecognized click state:")
        print(f"CHAMP_clicks = {CHAMP_clicks}")
        print(f"GOCE_clicks = {GOCE_clicks}")
        print(f"GRACE_A_clicks = {GRACE_A_clicks}")
        print(f"SWARM_A_clicks = {SWARM_A_clicks}")
        print(f"GRACE_FO_clicks = {GRACE_FO_clicks}")
        print(f"MSISE00_01_clicks = {MSISE00_01_clicks}")
        print(f"MSIS20_01_clicks = {MSIS20_01_clicks}")
        print(f"JB2008_01_clicks = {JB2008_01_clicks}")
        print(f"DTM2020_01_clicks = {DTM2020_01_clicks}")
        print(f"DTM2013_01_clicks = {DTM2013_01_clicks}")
        print(f"TIEGCM_Weimer_01_clicks = {TIEGCM_Weimer_01_clicks}")
        print(f"TIEGCM_Heelis_01_clicks = {TIEGCM_Heelis_01_clicks}")
        print(f"WACCMX_Weimer_01_clicks = {WACCMX_Weimer_01_clicks}")
        print(f"WACCMX_Heelis_01_clicks = {WACCMX_Heelis_01_clicks}")
        print(f"GITM_01_clicks = {GITM_01_clicks}")
        print(f"WAM_IPE_clicks = {WAM_IPE_clicks}")
        return {"display": "block"}, "ERROR: satellite click state unrecognized."
        
@app.callback(
    [Output("satellite-description-popup", "style", allow_duplicate=True),
     Output("CHAMP-label", "n_clicks"),
     Output("GOCE-label", "n_clicks"),
     Output("GRACE-A-label", "n_clicks"),
     Output("SWARM-A-label", "n_clicks"),
     Output("GRACE-FO-label", "n_clicks"),
     Output("MSISE00-01-label", "n_clicks"),
     Output("MSIS20-01-label", "n_clicks"),
     Output("JB2008-01-label", "n_clicks"),
     Output("DTM2020-01-label", "n_clicks"),
     Output("DTM2013-01-label", "n_clicks"),
     Output("TIEGCM-Weimer-01-label", "n_clicks"),
     Output("TIEGCM-Heelis-01-label", "n_clicks"),
     Output("WACCMX-Weimer-01-label", "n_clicks"),
     Output("WACCMX-Heelis-01-label", "n_clicks"),
     Output("GITM-01-label", "n_clicks"),
     Output("WAM-IPE-label", "n_clicks")],
    Input("satellite-desc-x-button", "n_clicks"),
    prevent_initial_call=True
)
def close_description_popup(n_clicks):
    return {"display": "none"}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

@app.callback(
    Output("left-side-bar", "style"),
    Input("therm-main-menu-button", "n_clicks"),
    prevent_initial_call=True
)
def open_main_menu(n_clicks):
    return {"display": "block"}

@app.callback(
    Output("left-side-bar", "style", allow_duplicate=True),
    Input("close-main-menu", "n_clicks"),
    prevent_initial_call=True
)
def close_main_menu(n_clicks):
    return {"display": "none"}

@app.callback(
    Output("ionosphere-left-side-bar", "style", allow_duplicate=True),
    Input("ion-main-menu-button", "n_clicks"),
    prevent_initial_call=True
)
def open_ion_main_menu(n_clicks):
    return {"display": "block"}

@app.callback(
    Output("ionosphere-left-side-bar", "style", allow_duplicate=True),
    Input("close-ion-main-menu", "n_clicks"),
    prevent_initial_call=True
)
def close_ion_main_menu(n_clicks):
    return {"display": "none"}
    
server = app.server # Expose the Flask server for Gunicorn

if __name__ == '__main__':
    app.run_server(debug=True)
