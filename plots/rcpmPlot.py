import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def rcpm_plot(Alldata, year, TITLES, format):
    """
    Root mean square error, Correlation Coefficient, Standard Deviation, and Mean Error plot. Returns a plotly figure data type.
    """
    PHASE=['Quiet time','Main phase','Recovery phase']

    x = np.arange(len(TITLES))

    fig = make_subplots(1, 3, specs=[[{'colspan': 3}, None, None]])
    # metrics score bar 
    p = Alldata
    np.round(p[0][:, 0], 2)
    fig.add_trace(go.Bar(x=x, y=np.round(Alldata[0][:, 0], 2), name=PHASE[0],marker_color='steelblue'))
    fig.add_trace(go.Bar(x=x, y=np.round(Alldata[0][:,1],2), name=PHASE[1],marker_color='orange'))
    fig.add_trace(go.Bar(x=x, y=np.round(Alldata[0][:,2], 2), name=PHASE[2],marker_color='green'))
    fig.update_yaxes(title='RMSE (TECu)', range=format[0])
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='white')
    fig.update_layout(title = format[4] + " scores for the " + str(year) + " storm",title_x=0.5, barmode="group", margin=dict(
        b=40,  # bottom margin
        t=80,  # top margin
        pad=1
    ))
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='white', tickmode = 'array', showticklabels=True, ticktext =TITLES, ticks="outside", tickvals= x)

    # Buttons is a list that updates what is displayed on the y-axis only. It changes
    buttons=list([
    dict(args=[{'y':[np.round(p[0][:, 0], 2),np.round(p[0][:, 1], 2), np.round(p[0][:, 2], 2)]},{'yaxis.range':format[0],'yaxis2.range':format[0],'yaxis3.range':format[0], 'yaxis.title.text':'RMSE (TECu)', 'yaxis2.title.text':'RMSE (TECu)', 'yaxis3.title.text':'RMSE (TECu)'}], label="RMSE", method="update"),
    dict(args=[{'y':[np.round(p[1][:, 0], 2),np.round(p[1][:, 1], 2), np.round(p[1][:, 2], 2)]},{'yaxis.range':format[1], 'yaxis2.range':format[1],'yaxis3.range':format[1],  'yaxis.title.text':'P\u03C3,diff (TECu)', 'yaxis2.title.text':'P\u03C3,diff (TECu)', 'yaxis3.title.text':'P\u03C3,diff (TECu)'}], label="P\u03C3", method="update"),
    dict(args=[{'y':[np.round(p[2][:, 0], 2),np.round(p[2][:, 1], 2), np.round(p[2][:, 2], 2)]},{'yaxis.range':format[2], 'yaxis2.range':format[2], 'yaxis3.range':format[2], 'yaxis.title.text':'Correlation Coefficient (R)', 'yaxis2.title.text':'Correlation Coefficient (R)', 'yaxis3.title.text':'Correlation Coefficient (R)'}], label="Corr. Coeff.", method="update"),
    dict(args=[{'y':[np.round(p[3][:, 0], 2),np.round(p[3][:, 1], 2), np.round(p[3][:, 2], 2)]},{'yaxis.range':format[3], 'yaxis2.range':format[3], 'yaxis3.range':format[3], 'yaxis.title.text':'ME (TECu)', 'yaxis2.title.text':'ME (TECu)', 'yaxis3.title.text':'ME (TECu)'}], label="ME", method="update"),
    ])

    fig.update_layout(
        updatemenus=[
            dict(
                buttons=buttons,
                direction="down",
                pad={"l": 10, "t": 10},
                showactive=True,
                x=-0.25,
                xanchor="left",
                y=1.3,
                yanchor="top"
            ),
        ]
    )
    return fig
