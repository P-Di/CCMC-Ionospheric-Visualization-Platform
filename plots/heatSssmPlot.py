import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def heatmap_sssm_plot(allphase, tt, year, TITLES): #remove YY if working

    skillscore = ['nSS_RMSE','nSS_P\u03C3,diff','nSS_R','nSS_ME']
    # plot Figure 4
    PHASE=['Quiet time','Main phase','Recovery phase']
    TITLES = TITLES[1:]
    fig = make_subplots(3, 1, specs=[[{}], [{}], [{}]],subplot_titles=(PHASE[0], PHASE[1], PHASE[2]), vertical_spacing=0.12, horizontal_spacing=0.02)
    flagcol=0
    for z,c in zip(allphase,range(3)):
        
        flagcol+=1
        if c == 0:df = pd.DataFrame(z, columns=skillscore,index=TITLES)
        else:df = pd.DataFrame(z,columns=skillscore)
        fig.add_trace(go.Heatmap(
            z=df.iloc[::-1],
            showscale=False,
            colorscale="RdBu_r",
            text = df.iloc[::-1],
            
            texttemplate="%{text}",

            ), flagcol, 1)
        
        fig.update(layout_coloraxis_showscale=False)
        

    x = np.arange(len(TITLES))  # the label locations

    fig.update_xaxes(tickmode = 'array', showticklabels=True, ticktext = df.columns, ticks="outside", tickvals= x, row=1, col=1)
    fig.update_xaxes(tickmode = 'array', showticklabels=True, ticktext = df.columns, ticks="outside", tickvals= x, row=2, col=1)
    fig.update_xaxes(tickmode = 'array', showticklabels=True, ticktext = df.columns, ticks="outside", tickvals= x, row=3, col=1)
    fig.update_layout(barmode = "group", title = tt+' total normalized skill score for the '+year+' storm', title_x=0.53)
    fig.update_yaxes(title='\u03A3nSS', title_standoff=0) #range=[0,5]
    fig.update_yaxes(showticklabels=False, row = 2, col = 1)
    fig.update_yaxes(showticklabels=False, row = 3, col = 1)
    fig.update_yaxes(tickmode = 'array', showticklabels=True, ticktext = TITLES, ticks="outside", tickvals= x)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='white')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='white')
    fig.update_layout(showlegend=False, margin=dict(
        l = 160,   #left margin
        b=20,  # bottom margin
        t=65,  # top margin
        pad=0
    ))
    return fig