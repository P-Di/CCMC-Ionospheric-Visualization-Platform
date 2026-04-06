import numpy as np
import plotly.graph_objects as go
def c2_map_plot(c2_lo, c2_la, II):
    fig = go.Figure()
    color = ['blue', 'orange', 'green']
    names = ['Quiet time: ', 'Main phase: ', 'Recovery phase: ']
    for p in np.arange(0,3): 
        fig.add_trace(go.Scattergeo(lon=c2_lo[II[p]], lat=c2_la[II[p]],name = names[p]+str(len(c2_lo[II[p]])), marker=dict(color=color[p], size=3)))
    fig.update_layout(title="F7/C2 data distribution during the 2021 November Storm",title_x=0.5, legend=dict(orientation = 'h', x=0, y=1, xanchor='left', yanchor='top', font=dict(size=14)))
    fig.update_geos(coastlinewidth=2)
    fig.update_layout(margin=dict(
        b=20,  # bottom margin
        t=40,  # top margin
        l = 20,
        r = 20,
        pad=1
    ))
    fig.update_yaxes(ticksuffix=" ")
    return fig