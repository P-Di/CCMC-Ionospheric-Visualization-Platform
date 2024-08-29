
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#
def tec_rcc_plot(CC, RP_par, MP_par, year, TITLES, format):
    """
    The ratios and correlation coefficient of total electron content change (TC).
    """

    range1 = format[0]
    range2 = format[1]
    observation = format[2]
    M_PE_diff= MP_par[1,:]-MP_par[2,:]
    R_PE_diff= RP_par[1,:]-RP_par[2,:]
    M_ratio_diff8020=M_PE_diff/M_PE_diff[0]
    R_ratio_diff8020=R_PE_diff/R_PE_diff[0]
    M_ratio_80=MP_par[1,:]/MP_par[1,0]
    R_ratio_80=RP_par[1,:]/RP_par[1,0]
    x1 = np.arange(len(TITLES))  # The label locations
    width = 0.25  # The width of the bars
    fig = make_subplots(1, 1, shared_xaxes=True, specs=[[{"secondary_y": True}]], subplot_titles=(''), horizontal_spacing=0.02, vertical_spacing=.02)
    fig.add_trace(
        go.Scatter(x = x1, y = M_ratio_diff8020, name="o-", line=dict(color="steelblue")),
        row=1, col=1, secondary_y=False)
    fig.add_trace(
        go.Scatter(x = x1, y = R_ratio_diff8020, name="o-", line=dict(color="orange")),
        row=1, col=1, secondary_y=False)
    fig.add_trace( 
            go.Bar(x = x1-width*.8, y = np.round(M_PE_diff,2), width= width*1.2, name="Main phase", marker_color="steelblue"),
            row=1, col=1, secondary_y=True)
    fig.add_trace( 
            go.Bar(x = x1+ width*.8, y = np.round(R_PE_diff,2), width= width*1.2, name="Recovery phase", marker_color="orange"),
            row=1, col=1, secondary_y=True)

    fig.add_trace(
        go.Scatter(x = x1, y = M_ratio_80, name="o-", line=dict(color="steelblue"),visible='legendonly'),
        row=1, col=1, secondary_y=False)
    fig.add_trace(
        go.Scatter(x = x1, y = R_ratio_80, name="o-", line=dict(color="orange"), visible='legendonly'),
        row=1, col=1, secondary_y=False)
    fig.add_trace( 
            go.Bar(x = x1-width*.8, y = np.round(MP_par[1,:],2), width= width*1.2, name="Main phase", marker_color="steelblue", visible='legendonly'),
            row=1, col=1, secondary_y=True)
    fig.add_trace( 
            go.Bar(x = x1+ width*.8, y = np.round(RP_par[1,:],2), width= width*1.2, name="Recovery phase", marker_color="orange", visible='legendonly'),
            row=1, col=1, secondary_y=True)

    fig.add_trace( 
            go.Bar(x = x1-width*.8, y = np.round(CC[0,:],2), width= width*1.2, name="Main phase", marker_color="steelblue", visible='legendonly'),
            row=1, col=1)
    fig.add_trace( 
            go.Bar(x = x1+ width*.8, y = np.round(CC[1,:],2), width= width*1.2, name="Recovery phase", marker_color="orange", visible='legendonly'),
            row=1, col=1)
    fig.update_yaxes(range=[-2.5, 3], secondary_y = False, ticks="outside", title=observation[0], row=1, col=1)
    fig.update_yaxes(range=range1, secondary_y = True, showgrid=False,zeroline=False, ticks="outside", title=observation[3], row=1, col=1)
    fig.update_xaxes(tickmode = 'array', showticklabels=True, ticktext = TITLES, showgrid=True,ticks="outside", tickvals= x1, row=1, col=1)
    # Create an interactive button to enable switching between graphs types.
    buttons=list([
        dict(args=[{'visible': [True, True, True, True, False, False, False, False, False, False]}, 
                   {'yaxis.range':[-2.5, 3],'yaxis2.range':range1, 'yaxis.title.text':observation[0], 'yaxis2.title.text':observation[3]}], label="RMSE", method="update"),
        dict(args=[{'visible': [False, False, False, False, True, True, True, True, False, False]}, 
                   {'yaxis.range':[-2.5, 3],'yaxis2.range':range2, 'yaxis.title.text':observation[1], 'yaxis2.title.text':observation[2]}], label="P\u03C3/diff", method="update"),
        dict(args=[{'visible': [False, False, False, False, False, False, False, False, True, True]}, 
                   {'yaxis.range':[0, 1.2],'yaxis2.range':[0, 0], 'yaxis.title.text':'Correlation Coefficient (R)', 'yaxis2.title.text':''}], label="Corr. Coeff.", method="update")
    ])
    # Update the layout, removing the legend and adding a dropdown menu to the top right corner.
    fig.update_layout(showlegend=False, title = year+' Storm ' + observation[4] + ' Observation' , title_x=0.5,
        updatemenus=[
            dict(
                buttons=buttons,
                direction="down",
                pad={"l": 10, "t": 10},
                showactive=True,
                x=-0.25,
                xanchor="left",
                y=1.5,
                yanchor="top"
            ),
        ]
    )
    return fig

