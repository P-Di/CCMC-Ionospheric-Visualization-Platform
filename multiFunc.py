import numpy as np
from dash import html
from dash import dcc

import testFunc
import plotFunc5

def tec_formatting(multi, obs, task, data, year, TITLES, dstyles):
    sub_child = []
    perm_tec = []
    sub_child2=[]
    perm_tec2 = []
    comp = int(multi[0])
    if year == '2013': default = 80
    else: default = 50
    if multi[-1] == '15': 
        multi = '15'
        comp = 1
    elif multi[0] == '15' and len(multi) > 1: 
        del multi[0]
        comp = int(multi[0])
    if len(multi) == 1 and multi[0] != '15':
        if (multi[0] == '10' or multi[0] == '11') and year == '2021': format_tec = 10
        else: format_tec = default

        if obs == 'FC2': 
            fig=testFunc.ctec_plot(data[1], int(multi[0]), '2021', 0, [np.arange(0,73,1), np.arange(-45,46,1)], TITLES[1], "foF2", [14, 1])
        elif obs == 'HC2': 
            fig=testFunc.ctec_plot(data[2], int(multi[0]), '2021', 0, [np.arange(0,73,1), np.arange(-45,46,1)], TITLES[1], "hmF2", [450, 150])
        elif task == 'SCE': 
            fig=plotFunc5.tec_plot(data[0]['TEC_all'], year, int(multi[0]), 0)
        else: 
            fig=testFunc.ctec_plot(data[0]['TEC_all'], int(multi[0]), year, 0, [np.arange(0,72,.5), np.arange(-40,40.5,.5)], TITLES[0], "TECu", [format_tec, 0])
            
        child_multi = html.Div(style=dstyles[4]|dstyles[3], children =dcc.Graph(style=dstyles[3], figure=fig))
        fig=testFunc.ctec_plot(data[0]['TEC_all'], int(multi[0]), year, 0, [np.arange(0,72,.5), np.arange(-40,40.5,.5)], TITLES[0], "TECu", [format_tec, 0])
        child_tec = html.Div(style=dstyles[4]|dstyles[3], children =dcc.Graph(style=dstyles[3], figure=fig))
    else:
        if multi == '15' and (obs == 'FC2' or obs == 'HC2'):tec = range(12)
        elif multi == '15': tec = range(15)
        else:tec = multi

        for i in range((int(len(tec)/2))):
            if (int(tec[i]) == 10 or int(tec[i]) == 11) and year == '2021': format_tec = 10
            else: format_tec = default

            if obs == 'FC2': 
                fig=testFunc.ctec_plot(data[1], int(tec[i]), '2021', 1, [np.arange(0,73,1), np.arange(-45,46,1)], TITLES[2], "foF2", [14, 1])
            elif obs == 'HC2': 
                fig=testFunc.ctec_plot(data[2], int(tec[i]), '2021', 1, [np.arange(0,73,1), np.arange(-45,46,1)], TITLES[2], "hmF2", [450, 150])
            elif task == 'SCE': 
                fig=plotFunc5.tec_plot(data[0]['TEC_all' ], year, int(tec[i]), 1)
            else: 
                fig=testFunc.ctec_plot(data[0]['TEC_all'], int(tec[i]), year, 1, [np.arange(0,72,.5), np.arange(-40,40.5,.5)], TITLES[0], "TECu", [format_tec, 0])

            sub_child.append(dcc.Graph(figure=fig, style=dstyles[6]))
            perm_tec.append(dcc.Graph(figure=testFunc.ctec_plot(data[0]['TEC_all'], int(tec[i]), year, 1, [np.arange(0,72,.5), np.arange(-40,40.5,.5)], TITLES[0], "TECu", [format_tec, 0]), style=dstyles[6]))

        for i in range(int(len(tec)/2), len(tec)):
            if (int(tec[i]) == 10 or int(tec[i]) == 11) and year == '2021': format_tec = 10
            else: format_tec = default

            if obs == 'FC2': 
                fig=testFunc.ctec_plot(data[1], int(tec[i]), '2021', 1, [np.arange(0,73,1), np.arange(-45,46,1)], TITLES[2], "foF2", [14, 1])
            elif obs == 'HC2': 
                fig=testFunc.ctec_plot(data[2], int(tec[i]), '2021', 1, [np.arange(0,73,1), np.arange(-45,46,1)], TITLES[2], "hmF2", [450, 150])
            elif task == 'SCE': 
                fig=plotFunc5.tec_plot(data[0]['TEC_all'], year, int(tec[i]), 1)
            else: 
                fig=testFunc.ctec_plot(data[0]['TEC_all'], int(tec[i]), year, 1, [np.arange(0,72,.5), np.arange(-40,40.5,.5)], TITLES[0], "TECu", [format_tec, 0])

            sub_child2.append(dcc.Graph(figure=fig, style=dstyles[6]))
            perm_tec2.append(dcc.Graph(figure=testFunc.ctec_plot(data[0]['TEC_all'], int(tec[i]), year, 1, [np.arange(0,72,.5), np.arange(-40,40.5,.5)], TITLES[0], "TECu", [format_tec, 0]), style=dstyles[6]))
        child_multi = [html.Div(style=dstyles[5], children =sub_child), 
                html.Div(style=dstyles[5], children =sub_child2)]
        child_tec = [html.Div(style=dstyles[5], children=perm_tec), 
                html.Div(style=dstyles[5], children=perm_tec2)]
        
    return child_multi, child_tec, comp, multi