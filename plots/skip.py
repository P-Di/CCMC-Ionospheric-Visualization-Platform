import numpy as np
import plotly.graph_objects as go
import pandas as pd

from plotly.subplots import make_subplots

csmc2_foF2 = np.load('data/foF2_202111_storm.npz')
TITLES = ['Madrigal TEC ','GloTEC ','JPL GIM ','SAMI3 ','SAMI3-RCM ','SAMI3-TIEGCM ','IRI-2016 ','IRI-2020 ','WAM-IPE ','WACCM-X ','TIEGCM-Weimer ', 
        'TIEGCM-Heelis ','CTIPe ','GITM-SWMF ','PBMOD ']
"""
def heatmap_sssm_plot(allphase, tt, year, TITLES):
"""
    #Normalized skill score data plotted using a heatmap.
    #A button is added to switch between phases.
"""
    # Define column names and phases
    skillscore = ['nSS_RMSE', 'nSS_P\u03C3,diff', 'nSS_R', 'nSS_ME']
    PHASE = ['Quiet time', 'Main phase', 'Recovery phase']
    
    # Adjust TITLES as in your original code
    TITLES = TITLES[1:]
    TITLES.reverse()
    
    # Create a figure (using a single subplot)
    fig = go.Figure()
    
    # Loop over each phase and add a heatmap trace.
    # Only the first trace is initially visible.
    for i, z in enumerate(allphase):
        if i == 0:
            # For the first phase, use TITLES as index labels
            df = pd.DataFrame(z, columns=skillscore, index=TITLES)
            y_labels = df.index
        else:
            # For the other phases, you may not have row labels
            df = pd.DataFrame(z, columns=skillscore)
            y_labels = list(range(df.shape[0]))
            
        fig.add_trace(go.Heatmap(
            z = df.iloc[::-1].values,  # reverse rows if needed
            x = df.columns,
            y = y_labels,
            colorscale = "RdBu_r",
            showscale = False,
            text = df.iloc[::-1].values,
            texttemplate = "%{text}",
            visible = (i == 0)  # only first trace is visible initially
        ))
    
    # Create button definitions – one for each phase.
    buttons = []
    for i, phase in enumerate(PHASE):
        # Create a list of booleans: only the i-th trace is visible
        vis = [False] * len(PHASE)
        vis[i] = True
        buttons.append(dict(
            label = phase,
            method = "update",
            args = [
                {"visible": vis},  # update trace visibility
                {"title": f"{phase} - {tt} normalized skill score for the {year} storm"}
            ]
        ))
    
    # Update the layout to add the update menu (the buttons)
    fig.update_layout(
        updatemenus = [
            dict(
                #type = "buttons",
                direction = "down",
                buttons = buttons,
                showactive = True,
                x = 0.5,
                xanchor = "center",
                y = 1.15,
                yanchor = "top"
            )
        ],
        title = f"{PHASE[0]} - {tt} normalized skill score for the {year} storm",
        margin = dict(l=160, b=20, t=65, pad=0)
    )
    
    # Optionally, update the axes formatting
    fig.update_xaxes(tickmode='array', tickvals=np.arange(len(skillscore)), ticktext=skillscore, ticks="outside", gridcolor='white')
    fig.update_yaxes(tickmode='array', ticks="outside", gridcolor='white')
    
    return fig
"""
# Example usage:"hmF2", '2021', TITLES[1]


import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
##Figure out initial subplot title issues
def heatmap_sssm_plot(allphase, tt, year, TITLES):
    """ Normalized skill score data plotted using a heatmap"""

    skillscore = ['nSS_RMSE','nSS_P\u03C3,diff','nSS_R','nSS_ME']
    # plot Figure 4
    PHASE=['Quiet','Main','Recovery']
    TITLES = TITLES[1:]
    TITLES.reverse()
    fig = make_subplots(1, 1, specs=[[{}]],subplot_titles=(" "), vertical_spacing=0.12, horizontal_spacing=0.02)
    for z,c in zip(allphase,range(3)):
        
        if c == 0:df = pd.DataFrame(z, columns=skillscore,index=TITLES)
        else:df = pd.DataFrame(z,columns=skillscore)
        fig.add_trace(go.Heatmap(
            z=df.iloc[::-1],
            showscale=False,
            colorscale="RdBu_r",
            text = df.iloc[::-1],
            
            texttemplate="%{text}",
            visible = (c == 0) 
            ), 1, 1)
        
        fig.update(layout_coloraxis_showscale=False)
        

    x = np.arange(len(TITLES))  # the label locations

    fig.update_xaxes(tickmode = 'array', showticklabels=True, ticktext = df.columns, ticks="outside", tickvals= x, row=1, col=1)
    fig.update_xaxes(tickmode = 'array', showticklabels=True, ticktext = df.columns, ticks="outside", tickvals= x, row=2, col=1)
    fig.update_xaxes(tickmode = 'array', showticklabels=True, ticktext = df.columns, ticks="outside", tickvals= x, row=3, col=1)
    fig.update_layout(barmode = "group", title = tt+' normalized skill score for the '+year+' storm', title_x=0.53)
    #fig.update_yaxes(title='\u03A3nSS', title_standoff=0) #range=[0,5]
    fig.update_yaxes(title='\u03A3nSS', title_standoff=0)
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


    buttons = []
    for i, phase in enumerate(PHASE):
        # Create a list of booleans: only the i-th trace is visible
        vis = [False] * len(PHASE)
        vis[i] = True
        buttons.append(dict(
            label = phase,
            method = "update",
            args = [
                {"visible": vis},  # update trace visibility
                {"annotations[0].text": f"{phase}"}
                #{"title": f"{tt} normalized skill score for the {year} storm"}
            ]
        ))
    
    # Update the layout to add the update menu (the buttons)
    fig.update_layout(
        updatemenus = [
            dict(
                #type = "buttons",
                direction = "down",
                buttons = buttons,
                showactive = True,
                x = -0.35,
                pad={"l": 10, "t": 10},
                xanchor = "left",
                y = 1.3,
                yanchor = "top"
            )
        ],
        #title = f"{tt} normalized skill score for the {year} storm",
        margin = dict(l=160, b=20, t=65, pad=0)
    )
    return fig

#fig = heatmap_sssm_plot(csmc2_foF2['allphase'], "Test Title", "2013", TITLES[2:])
#fig.show()