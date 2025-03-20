import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def skill_scores_sum_plot(All_nss1, year, TITLES, tt):
    """
    A function to plot the summation of normalized skill scores for each model. 
    """

    fig = make_subplots(1, 3, specs=[
            [{"colspan": 3}, None, None]])


    x = np.arange(len(TITLES))  # the label locations
    fig.add_trace(go.Bar(x=x, y=All_nss1[4][:,0],name="Quiet phase", marker_color='steelblue'), row=1, col=1)
    fig.add_trace(go.Bar(x=x, y=All_nss1[4][:,1],name="Main phase", marker_color='orange'))
    fig.add_trace(go.Bar(x=x, y=All_nss1[4][:,2],name="Recovery phase", marker_color='green'))

    fig.update_xaxes(tickmode = 'array', showticklabels=True, ticktext = TITLES[1:], ticks="outside", tickvals= x)

    fig.update_yaxes(title='\u03A3nSS', range=[0,5])
    fig.update_layout(barmode = "group", title = tt+' total normalized skill score for the '+year+' storm', title_x=0.5)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='white')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='white')

    return fig
