#6/10/2024 - Revisions: Deleted imports, check data.py comments to see original.
 
import numpy as np
# Import the dash library and modules 
import dash
from dash import dcc # Dash core componenets (dcc) for graphs and interactivity
from dash import html # Allows html manipultion within dash
from dash.dependencies import Input, Output, State # Modules for creating callback functions
import dash_bootstrap_components as dbc # Allows for easier webpage formatting

# Import plotly function files for each type of graph.
import plots.dstKp as dstKp
import plots.testFunc2 as testFunc2
import plots.testFunc3 as testFunc3
import plots.testFunc4 as testFunc4
import plots.testFunc5 as testFunc5
import plots.testFunc7 as testFunc7
import plots.comp_graph as comp_graph
import multiFunc
import plotSelection

#Import data
csmc2_foF2 = np.load('data/foF2_202111_storm.npz')
csmc2_hmF2 = np.load('data/hmF2_202111_storm.npz')
dst_scatter_map = np.load('data/dst_scatter_map.npz', allow_pickle=True)
image_paths = ['assets/CCMC.png', 'assets/airflow1.jpg']

#Create styles for the graphs and rows
dstyles = [{'display': 'flex','overflowY': 'scroll','maxHeight': '43vh', 'overflowX': 'auto'}, 
           {'height':'200px', 'width': '320px'}, {'margin-top': '20px', 'margin-bottom': '2px'}, 
           {'height':'100%', 'width': '100%', 'min-width': '600px', 'min-height': '400px'}, {'overflowY': 'scroll', 'overflowX': 'auto'}, 
           { 'height':'40vh', 'width': '100%', 'min-width': '33vh'}, {'height':'200px', 'min-width': '320px', 'width': '100%'}, {'height':'1200px', 'min-width': '600px', 'width': '100%'},
           {'display': 'flex','overflowY': 'scroll', 'height': '39vh', 'overflowX': 'auto', 'border-radius': '20px'}]
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
app.layout = html.Div(style = {'backgroundColor':'#f4f6f7  ', 'margin': '0'}, children=[  

    # Add the properly formatted CCMC image and airflow photo to the top of the page
    html.Img(src=image_paths[0], style={'height': '100px', 'width': 'auto%', 'position': 'fixed',
                                    'background-color': '#f4f6f7  ','padding-right': '6%', 'box-shadow': '5px 5px 5px #ededed'}),
    html.Div(id='img_container', children=[ 
                                        html.Img(id = 'picture_bg', src=image_paths[1],
                                                 style={ 'top': '0', 'width': '100%', 'height': '100px', 'object-fit': 'cover'}),
                                        html.Div(id='text_overlay',
                                                children=[
                                                    html.P("CCMC Ionospheric Visualization Platform",id='text_box', 
                                                           style={'position': 'absolute', 'top': '10px', 'left': '10px', 
                                                                  'color': 'white', 'font-size': '54px', 'overflowX': 'hidden', 'white-space': 'nowrap'})])
                                            ],style={'padding': '0', 'margin': '0', 'width': '100%', 'height': '100%', 
                                                  'position': 'relative', 'margin-left': '20%', 'width':'80%'}),

    # Format the window on the left of the webpage to include all the dropdown menus.
    html.Div([
                html.Div(children=[html.B(children='Project')], style=dstyles[2]),
                dcc.Dropdown(id='project', options=[
                    {'label': 'Ionosphere Model Validation', 'value': 'IMV'},
                    {'label': 'Ray Tracing', 'value': 'RT'},
                    {'label': 'GPS Positioning', 'value': 'GPS'},], value = 'IMV'),
                html.Div(children=[html.B(children='Storm ID')], style=dstyles[2]),
                dcc.Dropdown(id='year', options=[
                    {'label': '2013-03-TP-01', 'value': '201303'},
                    {'label': '2021-11-TP-01', 'value': '202111'}], value = '201303'),
                html.Div(children=[html.B(children='Observation')], style=dstyles[2]),
                dcc.Dropdown(id='observation', options=[
                    {'label': 'Madrigal TEC', 'value': 'TEC'},
                    {'label': 'foF2_COSMIC2', 'value': 'FC2'},
                    {'label': 'hmF2_COSMIC2', 'value': 'HC2'},
                    {'label': 'foF2_ionsonde', 'value': 'FI'},
                    {'label': 'hmF2_ionsonde', 'value': 'HI'}], value = 'TEC'),
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
            ], style={'width': '20%', 'background-color': '#f4f6f7', 
                      'padding': '20px', 'height': '100%', 'position': 'fixed',
                      'margin-top': '0px','box-shadow': '5px 5px 5px #ededed '
}),
    #Format the right 80% of the page, which are created from different graphs that are appended to the children of the rows and columns using a callback
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
                    html.Div(id = 'child4', style=dstyles[8], children =[])], width=6)#This one
                        ]),
            dbc.Row([
                dbc.Col(
                    html.Div(style={'height': '15px'}), width=12)]),
            dbc.Row([
                dbc.Col([
                    html.Div(id = 'child5', style=dstyles[8], children =[])], width=6),#This one
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
        ], fluid=True)
    ]),
    html.Footer(id='footer', children=[html.P("CCMC Ionospheric Visualization Platform",id='footer_text')])
])


# Create one callback to handle all graphs, with the input from all the sidebar buttons
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

    # Combine the TEC data from Cosmic 2
    TEC_foF2 = np.concatenate([[csmc2_foF2['C2_foF2_map']], csmc2_foF2['All_model_fof2']])
    TEC_hmF2 = np.concatenate([[csmc2_hmF2['C2_hmF2_map']], csmc2_hmF2['All_model_hmf2']])
    year = yearid[:4]

    fig1=dstKp.dst_kp_plot(int(year), dst_scatter_map['dst_'+year])
    chosen_year = np.load('data/MTEC_'+yearid+'_storm.npz')

    # These are conditionals to set up the TEC plot children. They are specially set up to 
    #   contain multiple different graphs since multiple TEC plots can be selected at once.
    child_multi, child_tec, comp, multi = multiFunc.tec_formatting(multi, obs, task, [chosen_year, TEC_foF2, TEC_hmF2], year, TITLES, dstyles)

    # If no values have been selected for plot, change it to an empty string
    if plot == None:
        plot = ['']

    child1 = dcc.Graph(style=dstyles[3], figure=testFunc3.c2_map_plot(dst_scatter_map['c2_lon'], dst_scatter_map['c2_lat'], dst_scatter_map['II_list']))
    plot_options = ['DEF_F1','DEF_F2', 'DK_F', 'MS_F', 'SN_F1', 'SN_F2', 'RCC', 'SC_F']
    if obs == 'FC2':

        graphs = [
                    child1,
                    child_multi,
                    dcc.Graph(style=dstyles[3], figure=fig1),
                    dcc.Graph(style=dstyles[3], figure=testFunc2.rcpm_plot(csmc2_foF2['Alldata'], '2021', 1)),
                    dcc.Graph(style=dstyles[7], figure=testFunc4.heatmap_sssm_plot(csmc2_foF2['allphase'], 1, '2021')),
                    dcc.Graph(style=dstyles[3], figure=testFunc5.skill_scores_sum_plot(csmc2_foF2['All_nss'], '2021', 1)),
                    dcc.Graph(style=dstyles[3], figure=testFunc7.tec_change_plot(csmc2_foF2['CC'], csmc2_foF2['RP_par'], csmc2_foF2['MP_par'], '2021', 1)),
                    dcc.Graph(style=dstyles[3], figure=comp_graph.model_comparison_plot(TEC_foF2[0], TEC_foF2[comp], TITLES[1], comp, dst_scatter_map['z_foF2'][comp-1]))
                ]
        if comp == 0:
            graphs[-1] = error

        chl = plotSelection.plot_selection_format(plot, plot_options, graphs)
        return chl[0], chl[1], chl[2], chl[3], chl[4], chl[5], chl[6],chl[7], multi, options_list[3], options_list[0]
    elif obs == 'HC2':

        graphs = [
                    child1,
                    child_multi,
                    dcc.Graph(style=dstyles[3], figure=fig1),
                    dcc.Graph(style=dstyles[3], figure=testFunc2.rcpm_plot(csmc2_hmF2['Alldata'], '2021', 2)),
                    dcc.Graph(style=dstyles[7], figure=testFunc4.heatmap_sssm_plot(csmc2_hmF2['allphase'], 2, '2021')),
                    dcc.Graph(style=dstyles[3],figure=testFunc5.skill_scores_sum_plot(csmc2_hmF2['All_nss'], '2021', 2)),
                    dcc.Graph(style=dstyles[3],figure=testFunc7.tec_change_plot(csmc2_hmF2['CC'], csmc2_hmF2['RP_par'], csmc2_hmF2['MP_par'], '2021', 2)),
                    dcc.Graph(style=dstyles[3], figure=comp_graph.model_comparison_plot(TEC_hmF2[0], TEC_hmF2[comp], TITLES[1], comp, dst_scatter_map['z_hmF2'][comp-1]))
                ]
        if comp == 0:
            graphs[-1] = error
   
        chl = plotSelection.plot_selection_format(plot, plot_options, graphs)
        return chl[0], chl[1], chl[2], chl[3], chl[4], chl[5], chl[6],chl[7], multi, options_list[3], options_list[0]
    

    else:
        if task == 'SCE':
            graphs = [
                        child_multi,
                        dcc.Graph(style=dstyles[3],figure=fig1),
                        child_tec, 
                        dcc.Graph(style=dstyles[3],figure=testFunc2.rcpm_plot(chosen_year['Alldata'], year, 0)),
                        dcc.Graph(style=dstyles[7], figure=testFunc4.heatmap_sssm_plot(chosen_year['allphase'], 0, year)),
                        dcc.Graph(style=dstyles[3],figure=testFunc5.skill_scores_sum_plot(chosen_year['All_nss'], year, 0)),
                        dcc.Graph(style=dstyles[3], figure=testFunc7.tec_change_plot(chosen_year['CC'], chosen_year['RP_par'], chosen_year['MP_par'], year, 0)),
                        dcc.Graph(style=dstyles[3],figure=comp_graph.model_comparison_plot(chosen_year['TEC_all'][0], chosen_year['TEC_all'][comp],TITLES[0],comp, dst_scatter_map['z_'+year][comp-1]))
                    ]
            if comp == 0:
                graphs[-1] = error
            
            plot_options = ['DEF_F1', 'DK_F','DEF_F2', 'MS_F', 'SN_F1', 'SN_F2', 'RCC','SC_F',]
            chl = plotSelection.plot_selection_format(plot, plot_options, graphs)

            return chl[0], chl[1], chl[2], chl[3], chl[4], chl[5], chl[6],chl[7], multi, options_list[2], options_list[1]

        else:
            child1 = dcc.Graph(style=dstyles[3], figure=fig1)
            child3 = dcc.Graph(style=dstyles[3], figure=testFunc2.rcpm_plot(chosen_year['Alldata'], year, 0))
            child4 = dcc.Graph(style=dstyles[7], figure=testFunc4.heatmap_sssm_plot(chosen_year['allphase'], 0, year))
            child5 = dcc.Graph(style=dstyles[3], figure=testFunc5.skill_scores_sum_plot(chosen_year['All_nss'], year, 0))
            child6 = dcc.Graph(style=dstyles[3],figure=comp_graph.model_comparison_plot(chosen_year['TEC_all'][0], chosen_year['TEC_all'][comp],TITLES[0],comp, dst_scatter_map['z_'+year][comp-1]))
            if comp == 0:
                child6 = error   

            return child1, child_multi, child3, child4, child5, child6, None, None, multi, options_list[2], options_list[1]
        
if __name__ == '__main__':
    app.run_server(debug=False)