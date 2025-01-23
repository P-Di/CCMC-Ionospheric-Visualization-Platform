#6/10/2024 - Revisions: Deleted imports, check data.py comments to see original.
 
import numpy as np
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
import plots.sssmPlot as sssmPlot
import plots.tecRccPlot as tecRccPlot
import multiFunc
import plotSelection
import plots.comparisonPlot as comparisonPlot

# import thermosphere page layout
import plotly.express as px
import plotly.graph_objects as go
from thermosphere_layout import thermosphere_layout, ap_thresholds, f107_thresholds, thermosphere_df

#Import data.
csmc2_foF2 = np.load('data/foF2_202111_storm.npz')
csmc2_hmF2 = np.load('data/hmF2_202111_storm.npz')
dst_scatter_map = np.load('data/dst_scatter_map.npz', allow_pickle=True)
image_paths = ['assets/CCMC.png', 'assets/airflow1.jpg']

obs_options=[[
                    {'label': 'Madrigal TEC', 'value': 'TEC'},
                    {'label': 'foF2_COSMIC2', 'value': 'FC2', 'disabled': False},
                    {'label': 'hmF2_COSMIC2', 'value': 'HC2', 'disabled': False},
                    {'label': 'foF2_ionsonde', 'value': 'FI', 'disabled': True},
                    {'label': 'hmF2_ionsonde', 'value': 'HI', 'disabled': True}],[
                    {'label': 'Madrigal TEC', 'value': 'TEC'},
                    {'label': 'foF2_COSMIC2', 'value': 'FC2', 'disabled': True},
                    {'label': 'hmF2_COSMIC2', 'value': 'HC2', 'disabled': True},
                    {'label': 'foF2_ionsonde', 'value': 'FI', 'disabled': True},
                    {'label': 'hmF2_ionsonde', 'value': 'HI', 'disabled': True}]]

#Create styles for the graphs and rows
dstyles = [{'display': 'flex','overflowY': 'scroll','maxHeight': '43vh', 'overflowX': 'auto'}, 
           {'height':'200px', 'width': '320px'}, {'margin-top': '20px', 'margin-bottom': '2px'}, 
           {'height':'100%', 'width': '100%', 'min-width': '600px', 'min-height': '400px'}, {'overflowY': 'scroll', 'overflowX': 'auto'}, 
           { 'height':'40vh', 'width': '100%', 'min-width': '33vh'}, {'height':'200px', 'min-width': '320px', 'width': '100%'}, {'height':'1200px', 'min-width': '600px', 'width': '100%'},
           {'display': 'flex','overflowY': 'scroll', 'height': '39vh', 'border-radius': '20px'}]
#Create error message
error = html.P('No Comparison Available for Standard Model.',
                style={
                    'backgroundColor': 'white',
                    'textAlign' : 'center',
                    'fontWeight': 'bold',
                    'fontSize': '24px',
                    'height': 'auto',
                    'paddingTop': '25%',
                    'width': '100%'})

TITLES=[['Madrigal TEC ','GloTEC ','JPL GIM ','SAMI3 ','SAMI3-RCM ','SAMI3-TIEGCM ','IRI-2016 ','IRI-2020 ','WAM-IPE ','WACCM-X ','TIEGCM-Weimer ', 
        'TIEGCM-Heelis ','CTIPe ','GITM-SWMF ','PBMOD '], ['FORM-7/COS-2 ','GIS_NCKU ','IRI2016 ','IRI2020 ','SAMI3-RCM ','SAMI3-TIEGCM ',
               'SAMI3-ICON ','WACCM-X ','GITM-SWMF ','TIEGCM-Weimer ','TIEGCM-Heelis ','WAM-IPE ','CTIPe '], 
               ['F7/C2 ','GIS_NCKU ','IRI2016 ','IRI2020 ','SMI3-RCM ','SMI3-TGCM ',
               'SMI3-ICN ','WACCM-X ','GTM-SWMF ','TGCM-Wmr ','TGCM-Hls ','WAM-IPE ','CTIPe ']]

common_options =[{'label': 'Dst_kp', 'value' : 'DK_F'},
                {'label': 'Ratios/CC', 'value' : 'RCC'},
                {'label': 'Metric_Score', 'value' : 'MS_F'},
                {'label': 'First sum_nSS', 'value' : 'SN_F1'},
                {'label': 'Second sum_nSS', 'value' : 'SN_F2'},
                {'label': 'Model Comparison', 'value' : 'SC_F'}]

options_list = [[{'label': 'F7/C2 Distribution', 'value' : 'DEF_F1'},
                {'label': 'CSM2 Models', 'value' : 'DEF_F2'}]+common_options,
                [
                {'label': 'TEC Change', 'value' : 'DEF_F1'},
                {'label': 'TEC', 'value' : 'DEF_F2'}]+common_options]

for i in TITLES:
    sub_op_list = [{'label': 'Show All', 'value' : '15'},]
    for j, k in enumerate(i):
        options_element = {'label': k, 'value': str(j)}
        sub_op_list.append(options_element)
    options_list.append(sub_op_list)
        

# Begin Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

#Define the layout: Set the background to a light gray, delete all margines.
ionosphere_layout = html.Div(style = {'backgroundColor':'#f4f6f7  ', 'margin': '0'}, children=[  
    html.Div( #Create a background for the CCMC logo image.
        style={'width': '20%', 'background-color': '#f4f6f7', 
                      'height': '200px', 'position': 'fixed',
                      'margin-top': '0px','box-shadow': '5px 5px 5px #ededed ',
            "zIndex": "1" # Control the layers of the title, with this being the lowest layer.
        }
    ),

    # Add the properly formatted CCMC image and airflow photo to the top of the page.
    html.Img(id="image1", src=image_paths[0], style={"zIndex": "2",'height': '100px', 'width': 'auto%', 'position': 'fixed',
                                    'background-color': '#f4f6f7  ','padding-right': '6%', }),
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
                        "CCMC Ionospheric Validation Campaign", 
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
    # Format the window on the left of the webpage to include all the dropdown menus.
    html.Div([
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
                    {'label': '2021-11-TP-01', 'value': '202111'}], value = '201303'),
                html.Div(children=[html.B(children='Observation')], style=dstyles[2]),
                dcc.Dropdown(id='observation', options=[
                    {'label': 'Madrigal TEC', 'value': 'TEC'},
                    {'label': 'foF2_COSMIC2', 'value': 'FC2'},
                    {'label': 'hmF2_COSMIC2', 'value': 'HC2'},
                    {'label': 'foF2_ionsonde', 'value': 'FI', 'disabled': True},
                    {'label': 'hmF2_ionsonde', 'value': 'HI', 'disabled': True}], value = 'TEC'),
                html.Div(children=[html.B(children='Model Type')], style=dstyles[2]),
                dcc.Dropdown(id='multi',
                    options=options_list[2], multi=True,  value = '0'),
                html.Div(children=[html.B(children='Task')], style=dstyles[2]),
                dcc.Dropdown(id='task', options=[
                    {'label': 'Model-data comparison', 'value': 'MC'},
                    {'label': 'Storm Capability Evaluation', 'value': 'SCE'}], value = 'MC'),
                html.Div(children=[html.B(children='Plot')], style=dstyles[2]),
                dcc.Dropdown(id='plot',
                    options=options_list[1], multi=True, value = ['DEF_F1', 'DEF_F2']),
            ], style={"zIndex": "2", 'width': '20%', 'background-color': '#f4f6f7', 
                      'padding': '20px', 'height': '100%', 'position': 'fixed',
                      'margin-top': '0px','box-shadow': '5px 5px 5px #ededed '
}),
    #Format the right 80% of the page, which are created from different graphs that are appended to the children of the rows and columns using a callback.
    html.Div(style = {'margin-left' : '25%'}, children=[

        dbc.Container
        ([
            dbc.Row([
                dbc.Col(html.Div(style={'height': '15px'}), width=12)]),
            dbc.Row([
                dbc.Col([
                    html.Div(id = 'child1', style=dstyles[8], children =[])], width=6),
                dbc.Col([
                    html.Div(id = 'child2', style=dstyles[8], children =[])], width=6)
                    ]),
            dbc.Row([
                dbc.Col(html.Div(style={'height': '15px'}), width=12)]),
            dbc.Row([
                dbc.Col([
                    html.Div(id = 'child3', style=dstyles[8], children =[])], width=6),
                dbc.Col([
                    html.Div(id = 'child4', style=dstyles[8], children =[])], width=6)
                        ]),
            dbc.Row([
                dbc.Col(
                    html.Div(style={'height': '15px'}), width=12)]),
            dbc.Row([
                dbc.Col([
                    html.Div(id = 'child5', style=dstyles[8], children =[])], width=6),
                dbc.Col([
                    html.Div(id = 'child6', style=dstyles[8], children =[])], width=6)
                        ]),
            dbc.Row([
                dbc.Col(
                    html.Div(style={'height': '15px'}), width=12)]),
            dbc.Row([
                dbc.Col([
                    html.Div(id = 'child7', style=dstyles[8], children =[])], width=6),
                dbc.Col([
                    html.Div(id = 'child8', style=dstyles[8], children =[])], width=6),
                    ])
        ], fluid=True), 
    ]),
            html.Footer(
            children=[html.A("Accessibility", href='https://www.nasa.gov/accessibility', target="_blank"), html.Span(children =" | ")          
,html.A("Privacy Policy", href='https://www.nasa.gov/privacy/', target="_blank"), html.Span(children =" | Curators: Paul DiMarzio and Dr. Min-Yang Chou | NASA Official: Maria Kuznetsova")],
            style={
                'margin-left' : '20%',
                "textAlign": "center",
                "padding": "10px",
                "backgroundColor": "#f1f1f1",
                "position": "relative", 
                "bottom": 0,
                "width": "80%",})
])

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
        return thermosphere_layout
    elif (project == "IMV"):
        return ionosphere_layout


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
         Output('multi', 'value'),
         Output('multi', 'options'),
         Output('plot', 'options'),
         Output('observation', 'options'),
         Output('year', 'value'),
         Output('year', 'disabled'),
         Output('task', 'disabled'),
         Output('plot', 'disabled')
         ],
        [Input('multi', 'value'),
         Input('year', 'value'),
         Input('task', 'value'),
         Input('plot', 'value'),
         Input('observation', 'value'),
         State('child1', 'children'),
         State('child2', 'children'),
         State('child3', 'children'),
         State('child4', 'children'),
         State('child5', 'children'),
         State('child6', 'children'),
         State('child7', 'children'),
         State('child8', 'children')
         ]
)
def update_graph(multi, yearid, task, plot, obs, child1, child2, child3, child4, child5, child6, child7, child8):

    # Combine the TEC data from Cosmic 2.
    TEC_foF2 = np.concatenate([[csmc2_foF2['C2_foF2_map']], csmc2_foF2['All_model_fof2']])
    TEC_hmF2 = np.concatenate([[csmc2_hmF2['C2_hmF2_map']], csmc2_hmF2['All_model_hmf2']])
    year = yearid[:4]

    fig1=dstKpPlot.dst_kp_plot(int(year), dst_scatter_map['dst_'+year])
    chosen_year = np.load('data/MTEC_'+yearid+'_storm.npz')

    # These are conditionals to set up the TEC plot children. They are specially set up to  
    #   contain multiple different graphs since multiple TEC plots can be selected at once.
    child_multi, child_tec, comp, multi, cm = multiFunc.tec_formatting(multi, obs, task, [chosen_year, TEC_foF2, TEC_hmF2], year, TITLES, dstyles)

    # If no values have been selected for plot, change it to an empty string.
    if plot == None: plot = ['']
    if year == '2013': obs_op = obs_options[1]
    else: obs_op = obs_options[0]

    child1 = dcc.Graph(style=dstyles[3], figure=globeDistrPlot.c2_map_plot(dst_scatter_map['c2_lon'], dst_scatter_map['c2_lat'], dst_scatter_map['II_list']))
    plot_options = ['DEF_F1','DEF_F2', 'DK_F', 'MS_F', 'SN_F1', 'SN_F2', 'RCC', 'SC_F']
    if obs == 'FC2':
        # A list of all possible selected graphs.
        graphs = [ 
                    child1,
                    child_multi,
                    dcc.Graph(style=dstyles[3], figure=fig1),
                    dcc.Graph(style=dstyles[3], figure=rcpmPlot.rcpm_plot(csmc2_foF2['Alldata'], '2021', TITLES[1], [[0,10],[-5,5],[0,1.2],[-5,5], "foF2"])),
                    dcc.Graph(style=dstyles[7], figure=heatSssmPlot.heatmap_sssm_plot(csmc2_foF2['allphase'], "foF2", '2021', TITLES[1])),
                    dcc.Graph(style=dstyles[3], figure=sssmPlot.skill_scores_sum_plot(csmc2_foF2['All_nss'], '2021', TITLES[1], "foF2")),
                    dcc.Graph(style=dstyles[3], figure=tecRccPlot.tec_rcc_plot(csmc2_foF2['CC'], csmc2_foF2['RP_par'], csmc2_foF2['MP_par'], '2021', TITLES[1], [[0, 200], [0, 100], ["Ratio(95th-5th)", "Ratio_95th",  "RD_95th", "RD(95th)-RD(5th)", "foF2"]])),
                    child_multi #Placeholder for model_comparison_plot
                ]
        # Generate the comparison graph based off all selected model excluding comparison model.
        cm = list(map(int, cm))
        if len(cm) == 1 and cm[0] == 0: graphs[-1] = error 
        else:      
            graphs[-1] = dcc.Graph(style=dstyles[3], figure=comparisonPlot.model_comparison_plot(TEC_foF2[0], TEC_foF2, TITLES[1], cm, dst_scatter_map['z_foF2'], year))
        # Add selected plots and take out others.
        chl = plotSelection.plot_selection_format(plot, plot_options, graphs)
        return chl[0], chl[1], chl[2], chl[3], chl[4], chl[5], chl[6],chl[7], multi, options_list[3], options_list[0], obs_options[0], yearid, True, True, False
    
    elif obs == 'HC2':

        graphs = [
                    child1,
                    child_multi,
                    dcc.Graph(style=dstyles[3], figure=fig1),
                    dcc.Graph(style=dstyles[3], figure=rcpmPlot.rcpm_plot(csmc2_hmF2['Alldata'], '2021', TITLES[1], [[0,200],[-50,100],[0,1],[-100,100], "hmF2"])),
                    dcc.Graph(style=dstyles[7], figure=heatSssmPlot.heatmap_sssm_plot(csmc2_hmF2['allphase'], "hmF2", '2021', TITLES[1])),
                    dcc.Graph(style=dstyles[3], figure=sssmPlot.skill_scores_sum_plot(csmc2_hmF2['All_nss'], '2021', TITLES[1], "hmF2")),
                    dcc.Graph(style=dstyles[3], figure=tecRccPlot.tec_rcc_plot(csmc2_hmF2['CC'], csmc2_hmF2['RP_par'], csmc2_hmF2['MP_par'], '2021', TITLES[1], [[0, 150], [0, 100], ["Ratio(90th-10th)", "Ratio_90th", "TC_90th", "TC(90th)-TC(10th)", "hmF2"]])),
                    child_multi #Placeholder for model_comparison_plot
                ]
        # Generate the comparison graph based off all selected model excluding comparison model.
        cm = list(map(int, cm))
        if len(cm) == 1 and cm[0] == 0: graphs[-1] = error 
        else:      
            graphs[-1] = dcc.Graph(style=dstyles[3], figure=comparisonPlot.model_comparison_plot(TEC_hmF2[0], TEC_hmF2, TITLES[1], cm, dst_scatter_map['z_hmF2'], year))
        # Add selected plots and take out others.
        chl = plotSelection.plot_selection_format(plot, plot_options, graphs)
        return chl[0], chl[1], chl[2], chl[3], chl[4], chl[5], chl[6],chl[7], multi, options_list[3], options_list[0], obs_options[0], yearid, True, True, False
    

    else:
        if task == 'SCE':
            graphs = [
                        child_multi,
                        dcc.Graph(style=dstyles[3], figure=fig1),
                        child_tec, 
                        dcc.Graph(style=dstyles[3], figure=rcpmPlot.rcpm_plot(chosen_year['Alldata'], year, TITLES[0], [[0, 30], [-15, 15], [0, 1.2], [-25, 25], "TEC"])),
                        dcc.Graph(style=dstyles[7], figure=heatSssmPlot.heatmap_sssm_plot(chosen_year['allphase'], "TEC", year, TITLES[0])),
                        dcc.Graph(style=dstyles[3], figure=sssmPlot.skill_scores_sum_plot(chosen_year['All_nss'], year, TITLES[0], "TEC")),
                        dcc.Graph(style=dstyles[3], figure=tecRccPlot.tec_rcc_plot(chosen_year['CC'], chosen_year['RP_par'], chosen_year['MP_par'], year, TITLES[0], [[0, 200], [0, 200], ["Ratio(80th-20th)", "Ratio(80th)", "TC_80th", "TC(80th)-TC(20th)", "TEC"]])),
                        child_tec #Placeholder for model_comparison_plot
                    ]

            cm = list(map(int, cm))
            if len(cm) == 1 and cm[0] == 0: graphs[-1] = error 
            else:      
                graphs[-1] = dcc.Graph(style=dstyles[3], figure=comparisonPlot.model_comparison_plot(chosen_year['TEC_all'][0], chosen_year['TEC_all'], TITLES[0], cm, dst_scatter_map['z_' + year], year))
            # Generate the comparison graph based off all selected model excluding comparison model.
            plot_options = ['DEF_F1', 'DK_F','DEF_F2', 'MS_F', 'SN_F1', 'SN_F2', 'RCC','SC_F']
            chl = plotSelection.plot_selection_format(plot, plot_options, graphs)
            # Add selected plots and take out others.
            return chl[0], chl[1], chl[2], chl[3], chl[4], chl[5], chl[6], chl[7], multi, options_list[2], options_list[1], obs_options[0], yearid, False, False, False

        else:

            child1 = dcc.Graph(style=dstyles[3], figure=fig1)
            child3 = dcc.Graph(style=dstyles[3], figure=rcpmPlot.rcpm_plot(chosen_year['Alldata'], year, TITLES[0], [[0, 30], [-15, 15], [0, 1.2], [-25, 25], "TEC"]))
            child4 = dcc.Graph(style=dstyles[7], figure=heatSssmPlot.heatmap_sssm_plot(chosen_year['allphase'], "TEC", year, TITLES[0]))
            child5 = dcc.Graph(style=dstyles[3], figure=sssmPlot.skill_scores_sum_plot(chosen_year['All_nss'], year, TITLES[0], "TEC"))
            # Generate the comparison graph based off all selected model excluding comparison model.
            cm = list(map(int, cm))
            if len(cm) == 1 and cm[0] == 0: child6 = error 
            else:     
                child6 = dcc.Graph(style=dstyles[3], figure=comparisonPlot.model_comparison_plot(chosen_year['TEC_all'][0], chosen_year['TEC_all'], TITLES[0], cm, dst_scatter_map['z_' + year], year))

            return child1, child_multi, child3, child4, child5, child6, None, None, multi, options_list[2], options_list[1], obs_op, yearid, False, False, True
        
# create a callback to handle updates for the thermosphere page
@app.callback(
    Output("thermosphere-main-content", "children"),
    Input("tabs", "value")
)
def update_thermosphere_content(tab):
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
                children=dcc.Graph(
                    id="example-graph"
                )
            )   
        ]
    elif tab == "benchmark":
        pass

@app.callback(
    Output("example-graph", "figure"),
    [Input("parameter_selection", "value"),
     Input("category_selections", "value"),
     Input("ap_max_slider", "value"),
     Input("f107_max_slider", "value"),
     Input("satellites", "value")]
)
def display_plots(parameter, category, ap_max_threshold, f107_max_threshold, satellites):
    satellites = [satellite.strip() for satellite in satellites] 
    filtered_df = thermosphere_df.copy()

    if category != "all":
        filtered_df = filtered_df[filtered_df["category"] == category]
    filtered_df = filtered_df[filtered_df["satellite"].isin(satellites)]
    filtered_df = filtered_df[filtered_df["ap_max"].ge(ap_thresholds[ap_max_threshold])]
    filtered_df = filtered_df[filtered_df["f107_max"].ge(f107_thresholds[f107_max_threshold])]
    
    return px.box(filtered_df, x=parameter, y="model", color="category")


if __name__ == '__main__':
    app.run_server(debug=False, port=3000)