import plotly.graph_objects as go
import plotly.express as px
from dash import html, dcc
from pandas import DataFrame

def create_main_stripplot(dataframe: DataFrame, dataframe_stats: DataFrame, parameter: str) -> go.Figure:
    '''
    Returns a strip plot with a trace over each strip denoting the mean and one step standard deviation.

    :param dataframe: A dataframe containing the data that will be plotted
    :param dataframe_stats: A dataframe containing the mean and standard deviation for each model
    :param parameter: The parameter that will be plotted against the model

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

def create_phase_stripplots(dataframe: DataFrame, parameter: str) -> list:
    """
    Returns a list of dash html components, each containing the plot for a different model.

    :param dataframe: A dataframe containing the data that will be plotted
    :param dataframe_stats: A dataframe containing the mean and standard deviation for each model
    :param parameter: The parameter that will be plotted against the model

    :return plots: A list of dash html components containing the plots
    """
    skills_by_phase_plots = []
    for model in dataframe["model"].unique():
        df = dataframe[dataframe["model"] == model]
        stats: DataFrame = df.groupby("phase", observed=False)[parameter].agg(["mean", "std"]).reset_index().round(2)
        # since the debias_mean_OC pre_storm value is set to 1 throughout, don't display it on the plots (it adds no info)
        if parameter == "debias_mean_OC":
            debias_df = dataframe[dataframe["phase"] != "pre_storm"]
            fig = px.strip(debias_df[debias_df["model"] == model], x="phase", y=parameter)
        else:
            fig = px.strip(dataframe[dataframe["model"] == model], x="phase", y=parameter)

        for phase in dataframe["phase"].unique():
            if phase == "pre_storm" and parameter == "debias_mean_OC":
                continue

            mean = float(stats[stats["phase"] == phase]["mean"].iloc[0])
            std = float(stats[stats["phase"] == phase]["std"].iloc[0])

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


def fetch_tpid_data(dataframe: DataFrame, tpid_base_url: str) -> tuple[list, list]:
    '''
    Returns dash components for the tpid links and the basic storm data for the tpid menu

    :param dataframe: A dataframe containing all storms and storm data currently displayed on the page
    :param tpid_base_url: The basic url that will be used to construct the specific url for each storm

    :return components: Returns both the Ul of links and a list of three divs containing the basic storm data
    '''
    tpid_list = []
    basic_storm_data = dict(multiple_peak=0, single_peak=0)
    for tpid in dataframe["TP"].drop_duplicates():
        item = html.Li(
            html.A(
                tpid,
                href=tpid_base_url + tpid,
                target="_blank"
            )
        )
        tpid_list.append(item)

        if dataframe[dataframe["TP"] == tpid]["category"].iloc[0] == "multiple_peak":
            basic_storm_data["multiple_peak"] += 1
        else:
            basic_storm_data["single_peak"] += 1

    return tpid_list, [
        html.Div(f"Total Storm Count: {len(tpid_list)}"),
        html.Div(f"Multiple Peak Count: {basic_storm_data['multiple_peak']}"),
        html.Div(f"Single Peak Count: {basic_storm_data['single_peak']}")
    ]