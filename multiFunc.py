import numpy as np
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import plots.ctecPlot as ctecPlot
import plots.tecContPlot as tecContPlot
import plots.osseChangePlot as ossePlot

def tec_formatting(multi, obs, task, data, year, TITLES, dstyles):

    #Initialize all lists.
    sub_child, perm_tec, osse1, sub_child2, perm_tec2, osse2, child_osse = [], [], [], [], [], [], []
    if multi == []: multi = ['0']
    data_sm = [1.4, 15, 1, 60, 0]
    dstyles[6] = {'height':'200px', 'min-width': '320px', 'width': '100%'}
    dstyles[5] =  { 'height':'40vh', 'width': '100%', 'min-width': '33vh'}
    #Set default values.
    if year == '2013': default = 80
    else: default = 50
    if len(multi) == 2:
        if multi[1] != '15' and multi != '15':
            data_sm = [1, 80, 0, 60, 0]
            dstyles[6] = {'height':'400px', 'min-width': '320px', 'width': '100%'}
            dstyles[5] =  { 'height':'80vh', 'width': '100%', 'min-width': '33vh'}
    comp_mult = multi # Copy and preserve multi value.

    # If '15' or "All Graphs" is selected first, change to all graphs.

    if multi[-1] == '15':
        multi = '15'
    # If '15 or "All Graphs" is behind other selections, delete all graphs and keep selected graphs.
    elif multi[0] == '15' and len(multi) > 1: 
        del multi[0]
    # Depending on all selected value, create a list of graphs in two columns, then return list of two columns.
    if len(multi) == 1 and multi[0] != '15':
        if (multi[0] == '10' or multi[0] == '11') and year == '2021': format_tec = 10

        else: format_tec = default

        if obs == 'FC2':
            fig=ctecPlot.ctec_plot(data[1], int(multi[0]), '2021', 0, [np.arange(0,73,1), np.arange(-45,46,1)], TITLES[1], data_sm, "foF2", [14, 1])
            fig2 = ossePlot.secPlot(int(multi[0]), 0, data_sm, "fo")
            child_osse = html.Div(style=dstyles[4]|dstyles[3], children =dcc.Graph(style=dstyles[3], figure=fig2))

        elif obs == 'HC2':
            fig=ctecPlot.ctec_plot(data[2], int(multi[0]), '2021', 0, [np.arange(0,73,1), np.arange(-45,46,1)], TITLES[1], data_sm, "hmF2", [450, 150])
            fig2 = ossePlot.secPlot(int(multi[0]), 0, data_sm, "hm")
            child_osse = html.Div(style=dstyles[4]|dstyles[3], children =dcc.Graph(style=dstyles[3], figure=fig2))

        elif task == 'SCE' or task == 'MC': 
            fig=tecContPlot.tec_plot(data[0]['TEC_all'], year, int(multi[0]), 0, TITLES[0], data_sm)#data_sm[0]

        else: 
            fig=ctecPlot.ctec_plot(data[0]['TEC_all'], int(multi[0]), year, 0, [np.arange(0,72,.5), np.arange(-40,40.5,.5)], TITLES[0], data_sm, "TECu", [format_tec, 0])
            
        child_multi = html.Div(style=dstyles[4]|dstyles[3], children =dcc.Graph(style=dstyles[3], figure=fig))
        fig=ctecPlot.ctec_plot(data[0]['TEC_all'], int(multi[0]), year, 0, [np.arange(0,72,.5), np.arange(-40,40.5,.5)], TITLES[0], data_sm, "TECu", [format_tec, 0])
        child_tec = html.Div(style=dstyles[4]|dstyles[3], children =dcc.Graph(style=dstyles[3], figure=fig))



    else:
        if multi == '15' and (obs == 'FC2' or obs == 'HC2'):
            tec = range(12)
            comp_mult = range(1,12)
        elif multi == '15': 
            tec = range(15)
            comp_mult = range(1,15)
        else:tec = multi
        for i in range((int(len(tec)/2))):
            if (int(tec[i]) == 10 or int(tec[i]) == 11) and year == '2021': format_tec = 10
            else: format_tec = default

            if obs == 'FC2': 
                fig=ctecPlot.ctec_plot(data[1], int(tec[i]), '2021', 1, [np.arange(0,73,1), np.arange(-45,46,1)], TITLES[2], data_sm, "foF2", [14, 1])
                osse1.append(dcc.Graph(figure=ossePlot.secPlot(int(tec[i]), 1, data_sm, "fo"), style=dstyles[6])) #data_sm[0]
            
            elif obs == 'HC2': 
                fig=ctecPlot.ctec_plot(data[2], int(tec[i]), '2021', 1, [np.arange(0,73,1), np.arange(-45,46,1)], TITLES[2], data_sm, "hmF2", [450, 150])
                osse1.append(dcc.Graph(figure=ossePlot.secPlot(int(tec[i]), 1, data_sm, "hm"), style=dstyles[6])) #data_sm[0]
            elif task == 'SCE' or task == 'MC': 
                fig=tecContPlot.tec_plot(data[0]['TEC_all' ], year, int(tec[i]), 1, TITLES[0], data_sm)#data_sm[0]
            
            else: 
                fig=ctecPlot.ctec_plot(data[0]['TEC_all'], int(tec[i]), year, 1, [np.arange(0,72,.5), np.arange(-40,40.5,.5)], TITLES[0], data_sm, "TECu", [format_tec, 0])
           
            sub_child.append(dcc.Graph(figure=fig, style=dstyles[6]))
            perm_tec.append(dcc.Graph(figure=ctecPlot.ctec_plot(data[0]['TEC_all'], int(tec[i]), year, 1, [np.arange(0,72,.5), np.arange(-40,40.5,.5)], TITLES[0], data_sm, "TECu", [format_tec, 0]), style=dstyles[6]))
        for i in range(int(len(tec)/2), len(tec)):
            if (int(tec[i]) == 10 or int(tec[i]) == 11) and year == '2021': format_tec = 10
            else: format_tec = default

            if obs == 'FC2': 
                fig=ctecPlot.ctec_plot(data[1], int(tec[i]), '2021', 1, [np.arange(0,73,1), np.arange(-45,46,1)], TITLES[2], data_sm, "foF2", [14, 1])
                osse2.append(dcc.Graph(figure=ossePlot.secPlot(int(tec[i]), 1, data_sm, "fo"), style=dstyles[6]))#data_sm[0]
            elif obs == 'HC2': 
                fig=ctecPlot.ctec_plot(data[2], int(tec[i]), '2021', 1, [np.arange(0,73,1), np.arange(-45,46,1)], TITLES[2], data_sm, "hmF2", [450, 150])
                osse2.append(dcc.Graph(figure=ossePlot.secPlot(int(tec[i]), 1, data_sm, "hm"), style=dstyles[6]))

            elif task == 'SCE' or task == 'MC': 
                fig=tecContPlot.tec_plot(data[0]['TEC_all'], year, int(tec[i]), 1, TITLES[0], data_sm) #data_sm[0]
            
            else: 
                fig=ctecPlot.ctec_plot(data[0]['TEC_all'], int(tec[i]), year, 1, [np.arange(0,72,.5), np.arange(-40,40.5,.5)], TITLES[0], data_sm, "TECu", [format_tec, 0])
               
            sub_child2.append(dcc.Graph(figure=fig, style=dstyles[6]))
            perm_tec2.append(dcc.Graph(figure=ctecPlot.ctec_plot(data[0]['TEC_all'], int(tec[i]), year, 1, [np.arange(0,72,.5), np.arange(-40,40.5,.5)], TITLES[0], data_sm, "TECu", [format_tec, 0]), style=dstyles[6]))

        child_multi = dbc.Row([dbc.Col(style=dstyles[5], children =sub_child), 
                dbc.Col(style=dstyles[5], children =sub_child2)])
        child_tec = dbc.Row([dbc.Col(style=dstyles[5], children=perm_tec), 
                dbc.Col(style=dstyles[5], children=perm_tec2)])
        child_osse = dbc.Row([dbc.Col(style=dstyles[5], children=osse1), 
                dbc.Col(style=dstyles[5], children=osse2)])
     
    return child_multi, child_tec, multi, comp_mult, child_osse