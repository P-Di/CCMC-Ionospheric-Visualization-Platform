import numpy as np
import plotly.graph_objects as go

# This is a plot of Total Electron Content.
def tec_plot(TEC_all, year, des_model, multi, TITLES, data_sm):
    '''
    Total Electron Content maps of Magnetic Latitude vs. Local Time. TEC_all
    '''
    #Create Titles of all models graphed by the function.
    # Initialize a flag to track desired model.
    model = -1

    # For-loop to iterate through data for each model.
    for z, tl in zip(TEC_all, TITLES):
        model +=1
        # Loop through data for each model.
        if model==des_model: 
            z0=np.tile(z[:,:48],[1,2]) # Data Formatting
            des_tl=tl
            err1=(z[:,48:]-z0)/z0*100 # Data Formatting
            # Create a plotly figure.
            fig = go.Figure(data =
                go.Contour(
                    x = np.arange(0,52,.5), # X range chosen to display full range of Contour
                    y = np.arange(-45,40.5,.55), # Y range which displays full range of Contour
                    z=(err1),
                    y0=-50,
                    colorbar=dict(title = "%", ticks='outside', outlinecolor='black', outlinewidth=1), # Format colorbar with black outline and ticks showing.
                    colorscale="RdBu_r", # Create red and blue colorscheme for the Contour
                    contours=dict( # Change the range of the contours from 100 to -100
                    start = -100,
                    end = 100,
                    size = 50,
                    coloring = 'heatmap',
                    showlabels = True, # Show labels on contours
                    labelfont = dict( # Label font properties
                        size = 12,
                        color = 'black',
                    )
                ))
            )
    # Format including title, outline, and tick range.
    fig.update_yaxes(title='MLat', tickmode="array",range = [-50, 55], tickvals = np.arange(-50,56,25),  ticktext = np.arange(-50,56,25), 
                     showgrid=False, showline=True, linewidth=2, linecolor='black', mirror=True, title_standoff = 4)
    # Format the x-axis similar to y-axis.
    fig.update_xaxes(title_text="Local Time (hr)", showgrid=False,  showline=True, linewidth=2, linecolor='black', mirror=True,
                     tickmode = 'array',tickvals = np.arange(0,49,12), ticks="outside", ticktext = np.mod(np.arange(0,49,12),24))
    # Formatting the figure as a whole, including a title and background color.
    fig.update_layout(title_text = year + ' '+ des_tl, title_x=0.5, plot_bgcolor='white', showlegend=False)

    if not multi:
        fig['layout']['annotations'] += ( 
            dict(x=14, y=47,xref='x', yref='y',text='Main',showarrow=False, font_size=32, font_color='red'),
            dict(x=37, y=47,xref='x', yref='y',text='Recovery',showarrow=False, font_size=32, font_color='red'),
        )
        b = 70
    else:
        fig['layout']['annotations'] += ( 
            dict(x=14, y=47,xref='x', yref='y',text='Main',showarrow=False, font_size=11, font_color='red'),
            dict(x=37, y=47,xref='x', yref='y',text='Recovery',showarrow=False, font_size=11, font_color='red'),
        )
        fig.update_traces(colorbar_thickness=10, colorbar_len=data_sm[0])
        fig.update_yaxes(title_standoff = 0)
        b = data_sm[1]
    fig.update_layout(plot_bgcolor='white', showlegend=False, margin=dict(
        b=b,  # bottom margin
        t=b,  # top margin
        pad=1
    ))
    return fig