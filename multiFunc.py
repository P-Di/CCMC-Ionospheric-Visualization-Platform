import numpy as np
from dash import html
from dash import dcc

import plots.ctecPlot as ctecPlot
import plots.tecContPlot as tecContPlot
import plots.comparePlot as comparePlot

def tec_formatting(multi, obs, task, data, year, TITLES, dstyles, dst_scatter_map):
    sub_child = []
    perm_tec = []
    scatter_subc = []
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
            fig=ctecPlot.ctec_plot(data[1], int(multi[0]), '2021', 0, [np.arange(0,73,1), np.arange(-45,46,1)], TITLES[1], "foF2", [14, 1])
            fig2 = comparePlot.model_comparison_plot(data[1][0], data[1][comp], TITLES[1], comp, dst_scatter_map['z_foF2'][comp-1])
        elif obs == 'HC2': 
            fig=ctecPlot.ctec_plot(data[2], int(multi[0]), '2021', 0, [np.arange(0,73,1), np.arange(-45,46,1)], TITLES[1], "hmF2", [450, 150])
            fig2 = comparePlot.model_comparison_plot(data[1][0], data[1][comp], TITLES[1], comp, dst_scatter_map['z_hmF2'][comp-1])
        elif task == 'SCE': 
            fig=tecContPlot.tec_plot(data[0]['TEC_all'], year, int(multi[0]), 0, TITLES[0])
            fig2 = comparePlot.model_comparison_plot(data[0]['TEC_all'][0], data[0]['TEC_all'][comp], TITLES[0], comp, dst_scatter_map['z_'+year][comp-1])
        else: 
            fig=ctecPlot.ctec_plot(data[0]['TEC_all'], int(multi[0]), year, 0, [np.arange(0,72,.5), np.arange(-40,40.5,.5)], TITLES[0], "TECu", [format_tec, 0])
            fig2 = comparePlot.model_comparison_plot(data[0]['TEC_all'][0], data[0]['TEC_all'][comp], TITLES[0], comp, dst_scatter_map['z_'+year][comp-1])
            
        child_multi = html.Div(style=dstyles[4]|dstyles[3], children =dcc.Graph(style=dstyles[3], figure=fig))
        fig=ctecPlot.ctec_plot(data[0]['TEC_all'], int(multi[0]), year, 0, [np.arange(0,72,.5), np.arange(-40,40.5,.5)], TITLES[0], "TECu", [format_tec, 0])
        child_tec = html.Div(style=dstyles[4]|dstyles[3], children =dcc.Graph(style=dstyles[3], figure=fig))

        child_compare = html.Div(style=dstyles[4]|dstyles[3], children =dcc.Graph(style=dstyles[3], figure=fig2))
    else:
        if multi == '15' and (obs == 'FC2' or obs == 'HC2'):tec = range(12)
        elif multi == '15': tec = range(15)
        else:tec = multi

        for i in range((int(len(tec)/2))):
            if (int(tec[i]) == 10 or int(tec[i]) == 11) and year == '2021': format_tec = 10
            else: format_tec = default

            if obs == 'FC2': 
                fig=ctecPlot.ctec_plot(data[1], int(tec[i]), '2021', 1, [np.arange(0,73,1), np.arange(-45,46,1)], TITLES[2], "foF2", [14, 1])
                fig2 = comparePlot.model_comparison_plot(data[1][0], data[1][int(tec[i])], TITLES[1], int(tec[i]), dst_scatter_map['z_foF2'][int(tec[i])-1])
           
            elif obs == 'HC2': 
                fig=ctecPlot.ctec_plot(data[2], int(tec[i]), '2021', 1, [np.arange(0,73,1), np.arange(-45,46,1)], TITLES[2], "hmF2", [450, 150])
                fig2 = comparePlot.model_comparison_plot(data[2][0], data[2][int(tec[i])], TITLES[1], int(tec[i]), dst_scatter_map['z_hmF2'][int(tec[i])-1])
            
            elif task == 'SCE': 
                fig=tecContPlot.tec_plot(data[0]['TEC_all' ], year, int(tec[i]), 1, TITLES[0])
                fig2 = comparePlot.model_comparison_plot(data[0]['TEC_all'][0], data[0]['TEC_all'][int(tec[i])], TITLES[0], int(tec[i]), dst_scatter_map['z_'+year][int(tec[i])-1])

            else: 
                fig=ctecPlot.ctec_plot(data[0]['TEC_all'], int(tec[i]), year, 1, [np.arange(0,72,.5), np.arange(-40,40.5,.5)], TITLES[0], "TECu", [format_tec, 0])
                fig2 = comparePlot.model_comparison_plot(data[0]['TEC_all'][0], data[0]['TEC_all'][int(tec[i])], TITLES[0], int(tec[i]), dst_scatter_map['z_'+year][int(tec[i])-1])

            sub_child.append(dcc.Graph(figure=fig, style=dstyles[6]))
            perm_tec.append(dcc.Graph(figure=ctecPlot.ctec_plot(data[0]['TEC_all'], int(tec[i]), year, 1, [np.arange(0,72,.5), np.arange(-40,40.5,.5)], TITLES[0], "TECu", [format_tec, 0]), style=dstyles[6]))
            if int(tec[i]) >0:
                scatter_subc.append(dcc.Graph(figure=fig2,style=dstyles[3],))
        for i in range(int(len(tec)/2), len(tec)):
            if (int(tec[i]) == 10 or int(tec[i]) == 11) and year == '2021': format_tec = 10
            else: format_tec = default

            if obs == 'FC2': 
                fig=ctecPlot.ctec_plot(data[1], int(tec[i]), '2021', 1, [np.arange(0,73,1), np.arange(-45,46,1)], TITLES[2], "foF2", [14, 1])
                fig2 = comparePlot.model_comparison_plot(data[1][0], data[1][int(tec[i])], TITLES[2], int(tec[i]), dst_scatter_map['z_foF2'][int(tec[i])-1])
           
            elif obs == 'HC2': 
                fig=ctecPlot.ctec_plot(data[2], int(tec[i]), '2021', 1, [np.arange(0,73,1), np.arange(-45,46,1)], TITLES[2], "hmF2", [450, 150])
                fig2 = comparePlot.model_comparison_plot(data[2][0], data[2][int(tec[i])], TITLES[2], int(tec[i]), dst_scatter_map['z_hmF2'][int(tec[i])-1])
            
            elif task == 'SCE': 
                fig=tecContPlot.tec_plot(data[0]['TEC_all'], year, int(tec[i]), 1, TITLES[0])
                fig2 = comparePlot.model_comparison_plot(data[0]['TEC_all'][0], data[0]['TEC_all'][int(tec[i])], TITLES[0], int(tec[i]), dst_scatter_map['z_'+year][int(tec[i])-1])
            
            else: 
                fig=ctecPlot.ctec_plot(data[0]['TEC_all'], int(tec[i]), year, 1, [np.arange(0,72,.5), np.arange(-40,40.5,.5)], TITLES[0], "TECu", [format_tec, 0])
                fig2 = comparePlot.model_comparison_plot(data[0]['TEC_all'][0], data[0]['TEC_all'][int(tec[i])], TITLES[0], int(tec[i]), dst_scatter_map['z_'+year][int(tec[i])-1])

            sub_child2.append(dcc.Graph(figure=fig, style=dstyles[6]))
            perm_tec2.append(dcc.Graph(figure=ctecPlot.ctec_plot(data[0]['TEC_all'], int(tec[i]), year, 1, [np.arange(0,72,.5), np.arange(-40,40.5,.5)], TITLES[0], "TECu", [format_tec, 0]), style=dstyles[6]))
            if int(tec[i]) > 0:
                scatter_subc.append(dcc.Graph(figure=fig2, style=dstyles[3],))
        child_multi = [html.Div(style=dstyles[5], children =sub_child), 
                html.Div(style=dstyles[5], children =sub_child2)]
        child_tec = [html.Div(style=dstyles[5], children=perm_tec), 
                html.Div(style=dstyles[5], children=perm_tec2)]
        child_compare = [html.Div(children=scatter_subc, style=dstyles[4]|dstyles[3])]
        
    return child_multi, child_tec, comp, multi, child_compare