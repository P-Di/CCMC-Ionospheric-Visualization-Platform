import plotly.graph_objects as go
import plotly.express as px
from dash import html, dcc
from pandas import DataFrame

def create_main_stripplot(dataframe: DataFrame, dataframe_stats: DataFrame, parameter: str) -> go.Figure:
    '''
    Returns a strip plot with a trace over each strip denoting the mean and one step standard deviation.

    :param dataframe: A dataframe containing the data that will be plotted
    :param dataframe_stats: A dataframe containing the mean and standard deviation for each model
    :param parameter: The parameter that will be plotted agains the model

    :return figure: The plotly figure containing the strip plot
    '''
    plot = px.strip(dataframe, x=parameter, y="model")
    for model in dataframe["model"].unique():
        mean = float(dataframe_stats[dataframe_stats["model"] == model]["mean"].iloc[0])
        std = float(dataframe_stats[dataframe_stats["model"] == model]["std"].iloc[0])
        x_vals = [mean - std, mean, mean + std]
        y_vals = [model, model, model]
        plot.add_trace(go.Scatter(x=x_vals, y=y_vals, marker={"color": "black", "size": 8}))
    plot.update_traces(hoverinfo="none", hovertemplate=None)
    plot.update_layout(showlegend=False)

    return plot

def create_phase_stripplots(dataframe: DataFrame, dataframe_stats: DataFrame, parameter: str):
    skills_by_phase_plots = []
    for model in dataframe["model"].unique():
        # since the debias_mean_OC pre_storm value is set to 1 throughout, don't display it on the plots (it adds no info)
        if parameter == "debias_mean_OC":
            debias_df = dataframe[dataframe["phase"] != "pre_storm"]
            fig = px.strip(debias_df[debias_df["model"] == model], x="phase", y=parameter)
        else:
            fig = px.strip(dataframe[dataframe["model"] == model], x="phase", y=parameter)

        for phase in dataframe["phase"].unique():
            if phase == "pre_storm" and parameter == "debias_mean_OC":
                continue

            mean = float(dataframe_stats[dataframe_stats["phase"] == phase]["mean"].iloc[0])
            std = float(dataframe_stats[dataframe_stats["phase"] == phase]["std"].iloc[0])
            x_vals = [phase, phase, phase]
            y_vals = [mean - std, mean, mean + std]
            fig.add_trace(go.Scatter(x=x_vals, y=y_vals, marker={"color": "black", "size": 8}))
        fig.update_traces(hoverinfo="none", hovertemplate=None) # removes the hover function of the plots
        fig.update_layout(showlegend=False)

        # creates the actual webpage elements for the plots
        plot = html.Div([
            html.Span(
                html.B(f"Skills By Phase: {parameter} ({model})"),
                style={
                    "z-index": "3", 
                    "position": "relative",
                    "top": "50px",
                    "left": "80px"
                } 
            ),
            dcc.Graph(figure=fig)
        ])
        skills_by_phase_plots.append(plot)

    return skills_by_phase_plots