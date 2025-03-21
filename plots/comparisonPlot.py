import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# As each row of graphs is added, the colorbar format must be redone.
format2 = [[[.58], 250, 1.5, 1.35, 80, .22], [[0.849, 0.237], 600,1.2, .53, 80, .22], [[0.91, 0.53, 0.146], 600,1.15, .325, 80, .15], [[0.936, 0.660, 0.384, 0.11],800, 1.1, .240, 80, .1], [[0.945, 0.734, 0.520, 0.30, .084], 1000, 1.05, 0.186, 20, .07], [[0.955, 0.78, 0.6, 0.42, .24, .066], 1250, 1.05, .14, 20, .07], [[0.97, 0.818, 0.665, 0.51, .358, .205, .055], 1500, 1.05, .11, 20, .05], [1000]]
def model_comparison_plot(TEC1, TEC2, TITLES, comp, z, year):

    """ Function that takes in the TEC data, desired models, and year, and returns a single plot of ideal model vs selected models."""
    # If present, remove the first selection, as this is the plot against which other plots are being compared.
    if 0 in comp:
        comp.remove(0)
    if comp == []:
        comp.append(1)

    # If there is more than one plot, create two columns.
    col = 2 if len(comp) > 1 else 1
    
    # Set an adjustment of 0 if there are even number of graphs selected.
    adj = 0 if len(comp)%2 == 0 else 1

    format = [10 if len(comp) > 1 else 20]
    sub_titles = [TITLES[k] for k in comp]

    mid = (len(comp) + 1) // 2
    if col == 1:
        format2[mid-1][1] = 400
        format2[mid-1][3] = 1.1

    # Format titles into two lists for each column
    stitles = [item for pair in zip(sub_titles[:mid], sub_titles[mid:]) for item in pair]

    stitles.extend([" ", sub_titles[mid-1]])


    fig = make_subplots(rows=mid, cols=col,
                        row_heights=[2]*mid,
                        column_widths=[2]*col,
                        vertical_spacing=format2[mid-1][5],
                        horizontal_spacing=.21,
                        subplot_titles=stitles) 

    # Create each graph in comp list.
    for p, j in enumerate(comp):
        y = (TEC2[j].flatten())[np.logical_not(np.isnan(TEC2[j].flatten()))]
        x = (TEC1.flatten())[np.logical_not(np.isnan(TEC1.flatten()))]

        # Adjust formatting 
        col2 = 2 if len(comp) > 1 and p >= mid-adj else 1
        color_loc = 1 if col2 == 2 else 0.40
        if col == 1:
            color_loc = 1
        row2 = list(range(1, mid + 1)) * 2

        # Ensure length of both x and y matches.
        while len(y) != len(x):
            if len(y) > len(x):
                y = np.delete(y, -1)
            else:
                x = np.delete(x, -1)

        x1, y1 = np.array_split(x, 3), np.array_split(y, 3)
        for i in range(3):
            x, y = x1[i], y1[i]
            x2 = np.arange(np.min(x) - 5, np.max(x) + 5)
            a, b = np.polyfit(x, y, 1)

            # Create 9 plots on each graph, three for main, quiet, and recovery phases, and the other 6 being ideal and best fit lines.
            trace_visibility = "legendonly" if i > 0 else True
            fig.add_trace(go.Scattergl(x=x, y=y, mode='markers', visible=trace_visibility,
                                       marker=dict(color=z[j - 1][i],
                                                   colorscale='Viridis', size=14,
                                                   colorbar=dict(thickness=format[0],
                                                                 title=f'P. Dis.',
                                                                 x=color_loc,
                                                                 y=format2[mid-1][0][row2[p] - 1],
                                                                 len=format2[mid-1][3]))),
                          row=row2[p], col=col2)
            fig.add_trace(go.Scattergl(x=x2, y=a * x2 + b, mode='lines', line=dict(color='red'),
                                       hovertext=f"y = {round(a, 3)}*x + {round(b, 3)}",
                                       hoverinfo='text', visible=trace_visibility),
                          row=row2[p], col=col2)
            fig.add_trace(go.Scattergl(x=x2, y=x2, mode='lines', line=dict(color='black'),
                                       hovertext="y = x", hoverinfo='text', visible=trace_visibility),
                          row=row2[p], col=col2)

        fig.update_yaxes(title=TITLES[j], row=row2[p], col=col2)
        
    fig.update_traces(marker=dict(size=4), line=dict(width=2))
    fig.update_layout(coloraxis_colorbar_title_text='Probability Distribution', title_x=0.53)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True, title_standoff=4)
    fig.update_xaxes(title_text=TITLES[0], showline=True, linewidth=2, linecolor='black', mirror=True)

    # Create a button to only show one phase, ideal line, and best fit line at a time.
    buttons = [dict(args=[{'visible': [v for i in range(len(comp)) for v in [True, True, True, False, False, False, False, False, False]]},
                        {'title': f'{year} Quiet'}], label="Quiet", method="update"),
               dict(args=[{'visible': [v for i in range(len(comp)) for v in [False, False, False, True, True, True, False, False, False]]},
                        {'title': f'{year} Main'}], label="Main", method="update"),
               dict(args=[{'visible': [v for i in range(len(comp)) for v in [False, False, False, False, False, False, True, True, True]]},
                        {'title': f'{year} Recovery'}], label="Recovery", method="update")]

    fig.update_layout(showlegend=False, height=format2[mid-1][1], width=680, title=dict(text=f'{year} Quiet Phase', pad=dict(t=10, b=0)),  title_x=0.5,
                      updatemenus=[dict(buttons=buttons, direction="down", pad={"l": 10, "t": 10},
                                        showactive=True, x=-0.10, xanchor="left", y=format2[mid-1][2], yanchor="top")])
    fig.update_layout(margin=dict(
        l = 0,   #left margin
        b=10,  # bottom margin
        t=format2[mid-1][4],  # top margin
        pad=0
    ))
    return fig