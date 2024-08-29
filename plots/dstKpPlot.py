from datetime import datetime
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def dst_kp_plot(YR, dstdata):
    YR=[YR]
    dst_ut=np.arange(24*3)
    #Create a 2x2 subplot with the two upper plots given an extra y axis, 
    #   all are given names which will be replaced with the "annotate functionality"
    fig = make_subplots(specs=[[{"secondary_y": True}]], rows=1, cols =1, subplot_titles=("p1"))
    for c,YY in enumerate(YR):

        if YY==2013:DoM1=16;MM=3;ut_idx0=29;ut_idx1=30;ut_idx2=45
        else:DoM1=3;MM=11;ut_idx0=19;ut_idx1=21;ut_idx2=37
        dataDate = datetime(YY,MM,DoM1,0,0)
        yymmdd1 = dataDate.strftime("%Y/%m/%d")
        dataDate = datetime(YY,MM,DoM1+2,0,0)
        yymmdd2 = dataDate.strftime("%Y/%m/%d")
        yymm = dataDate.strftime("%Y%m")

        #Add the bar plot with the data formatted with the above code. Title y axis, and give the line a color.
        fig.add_trace( 
            go.Bar( x = dst_ut, y = dstdata[:,3]/10, name="yaxis data", marker_color="steelblue"),
            row=1, col=c+1,
            secondary_y=False)
        fig.add_trace(
            go.Scatter(x = dst_ut, y = dstdata[:,4], name="Kp", line=dict(color="red")),
            row=1, col=c+1,
            secondary_y=True)
        fig.add_trace(
            go.Scatter(x = [dst_ut[ut_idx1], dst_ut[ut_idx1]], y = [-150, 50], mode = 'lines', line=dict(color="black", dash='dash')),
            row=1, col=c+1,
            secondary_y=True)
        fig.add_trace(
            go.Scatter(x = [dst_ut[ut_idx2], dst_ut[ut_idx2]], y = [-150, 50], mode = 'lines', line=dict(color="black", dash='dash')),
            row=1, col=c+1,
            secondary_y=True)
        #Overall title for entire figure
        fig.update_layout(
        title_text='DST/KP Index',  title_x=0.5)

        #update first y-axis
        fig.update_yaxes(title='Kp',  range=[0, 15], secondary_y = False, showgrid=False, showline=True, linewidth=2, linecolor='black', mirror=True)
        #update second y-axis
        fig.update_yaxes(title='Dst',range=[-150,50], secondary_y = True, showgrid = True, zeroline=True, zerolinewidth=2, zerolinecolor="gray",gridcolor='gray', gridwidth = 2 )
        fig.update_xaxes(title_text="UT (hr)", showgrid=False,  showline=True, linewidth=2, linecolor='black', mirror=True,tickmode = 'array',tickvals = np.arange(0, 72, 6), ticks="outside", ticktext = np.mod(np.arange(0,72,6),24))
        fig.layout.annotations[c].update(text=yymmdd1+'-'+yymmdd2)
        fig.update_yaxes(titlefont_color="steelblue", secondary_y = False, tickmode='array', ticks='outside', tickvals = np.arange(0,16,3))
        fig.update_yaxes(titlefont_color="red", secondary_y = True, ticks="outside")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")

    fig.update_layout(plot_bgcolor= "white", paper_bgcolor= "white")
    fig.update_layout(showlegend=False)
    fig['layout'].update(annotations=[
        dict(x=15, y=13,xref='x', yref='y',text='Quiet phase',showarrow=False, font_size=16),
        dict(x=37.5, y=13,xref='x', yref='y',text='Main phase',showarrow=False, font_size=16),
        dict(x=58, y=13, xref='x', yref='y', text='Recovery phase',showarrow=False, font_size=16),
        dict(x=15, y=13,xref='x', yref='y',text='Quiet phase',showarrow=False, font_size=16),
        dict(x=37.5, y=13,xref='x', yref='y',text='Main phase',showarrow=False, font_size=16),
        dict(x=58, y=13, xref='x', yref='y', text='Recovery phase',showarrow=False, font_size=16),

        ])
    return fig

