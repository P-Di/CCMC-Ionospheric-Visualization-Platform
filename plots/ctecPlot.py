import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

        
def ctec_plot(TEC_all, flag, year, multi, xy_range, TITLES, obs_type, c_max_min):
    if obs_type[0].lower() == 't': 
        unit="TECu"
        if flag == 0:
            obs_type = ''
    else: unit = "MHz"
    
    fig = make_subplots(1, 1, subplot_titles=(''))

    fig.add_trace(go.Heatmap(
            y=xy_range[1],
            x = xy_range[0],
            z=TEC_all[flag],
            zmax = c_max_min[0],
            zmin = c_max_min[1],
            colorscale="RdBu_r",
            colorbar=dict(title = unit, ticks='outside', outlinecolor='black', outlinewidth=1),
        ))


    fig.update_yaxes(title='MLat', range=[-50, 56], tickvals =np.arange(-50,55,25), showgrid=False, 
                     showline=True, linewidth=1, linecolor='black',ticks="outside", mirror=True, title_standoff = 4)
    fig.update_xaxes(title_text="MLT (hr)", showgrid=False,  showline=True, linewidth=2, linecolor='black', 
                     mirror=True,tickmode = 'array',tickvals = np.arange(0, 73, 12), ticks="outside", ticktext = np.mod(np.arange(0,73,12),24))

    if not multi:
        fig['layout']['annotations'] += ( 
            dict(x=14, y=50,xref='x', yref='y',text='Quiet',showarrow=False, font_size=32, font_color='red'),
            dict(x=37, y=50,xref='x', yref='y',text='Main',showarrow=False, font_size=32, font_color='red'),
            dict(x=58, y=50, xref='x', yref='y', text='Recovery',showarrow=False, font_size=32, font_color='red'))
        b = 70
    else:
        fig['layout']['annotations'] += ( 
            dict(x=14, y=47,xref='x', yref='y',text='Quiet',showarrow=False, font_size=11, font_color='red'),
            dict(x=37, y=47,xref='x', yref='y',text='Main',showarrow=False, font_size=11, font_color='red'),
            dict(x=58, y=47, xref='x', yref='y', text='Recovery',showarrow=False, font_size=11, font_color='red'))
        fig.update_traces(colorbar_thickness=10, colorbar_len=1.4)
        fig.update_yaxes(title_standoff = 0)
        b = 15
    fig.update_layout(title=year+' '+TITLES[flag]+obs_type,title_x=0.5, plot_bgcolor='white', showlegend=False, margin=dict(b=b,  # bottom margin 
                                                                          t=b,  # top margin
                                                                          pad=1))
    return fig