"""
**stripplot.py**

| This module is the what actually creates all the plots and data that is displayed on the Thermosphere page.
| 
| It contains the following functions:

1. `create_main_stripplot`: creates the figure for the main plot on the page
2. `create_phase_stripplots`: creates the firgures for the rest of the stripplots on the page
3. `fetch_tpid_data`: returns hyperlinks to the displayed storm home pages
4. `create_plots`: The main function in this module. Returns all necessary data to the callbacks. Calls the three above functions

"""

from math import exp
import plotly.graph_objects as go
import plotly.express as px
from dash import html, dcc
import pandas as pd
from pandas import DataFrame
from pandas.api.typing import DataFrameGroupBy

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
    # dataframe = dataframe.iloc[::-1]
    skills_by_phase_plots = []
    for model in dataframe["model"].unique():
        df = dataframe[dataframe["model"] == model]
        stats: DataFrame = df.groupby("phase", observed=False)[parameter].agg(["mean", "std"]).reset_index().round(2)
        # since the debias_mean_OC pre_storm value is set to 1 throughout, don't display it on the plots (it adds no info)
        if parameter == "debias_mean_OC":
            debias_df = dataframe[dataframe["phase"] != "pre_storm"]
            phase_order = ["total", "onset", "main_recovery", "post_storm"]
            fig = px.strip(
                debias_df[debias_df["model"] == model],
                x="phase",
                y=parameter,
                category_orders={"phase": phase_order}
            )
        else:
            phase_order = ["total", "pre_storm", "onset", "main_recovery", "post_storm"]
            fig = px.strip(
                dataframe[dataframe["model"] == model],
                x="phase",
                y=parameter,
                category_orders={"phase": phase_order}
            )

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
        plot = html.Div(
            className='skills-by-phase-plot',
            children=[
                html.Span(
                    html.B(f"Skills By Phase: {parameter} ({model})"),
                    className='skills-by-phase-title',
                    style={
                        "z-index": "3", 
                        "position": "relative",
                        "top": "50px",
                        "left": "80px"
                    } 
                ),
                dcc.Graph(figure=fig)
            ]
        )
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


def create_plots(
        filtered_df: DataFrame,
        parameter: str,
        first_model: str,
        tpid_base_url: str,
    ) -> tuple[go.Figure, list[dict], list, list, list, list]:
    """
    | This function creates the plots and tables for the analysis dashboard and benchmark page on the Thermosphere web app.
    | The functionalities of this function are the following:
    
    * Computing the mean and standard deviation of `filtered_df`
    * Creating and styling the mean and std labels for the main plot using dash html components
    * Creating the pivot table from `filtered_df`
    * Fetching the data for the tpid menu

    Note: This function does not actually create any plots (dispite the name) that actual plot creation takes place in other functions
    in stripplot.py which this function calls.


    :param filtered_df: A Dataframe containing all data to be plotted after data has been filtered out per the users selection

    :param parameter: A string containing the paramater that will be analyzed. Can be one of the following:

                      * mean_OC
                      * debias_mean_OC
                      * stddev_OC
                      * R

    :param first_model: A string containing the name of the model that will appear at the top of the main plot. This is only
                        used for styling the mean and std labels rendered to the left of the main plot. 
                        This parameter is needed because a different model is on top on the dashboard page and the benchmark page.

    :param tpid_base_url: A string containing the base url used in the hyperlinks in the tpid menu on the analysis dashboard and
                          benchmark pages.

    :param model_order: A list of model names. This is used to ensure the main plot and main data table order the models consistently.

    :return main_plot: The main stripplot which plots all models for the 'total' phase
    :return table_data: The pivot table data obtained from `filtered_df`
    :return skills_by_phase_plots: A list of figures containing the skills by phase plots for the parameter
    :return formatted_main_plot_stats: A list of dash html components which are the mean and std labels for the main plot
    :return tpid_list: A list of the hyperlinks to the storm home page for each unique storm in `filtered_df`
    :return basic_storm_data: Basic stats on the storms being displayed:
                              
                              * Total Storm Count
                              * Multiple Peak Count
                              * Single Peak Count
    """
    filtered_df = filtered_df.sort_values(by="model")
    filtered_df = filtered_df.iloc[::-1]

    # create the elements for the main plot mean and std display
    main_plot_stats: DataFrame = filtered_df.groupby("model", observed=False)[parameter].agg(["mean", "std"]).reset_index().round(2)
    # main_plot_stats = main_plot_stats.iloc[::-1]

    # main plot only uses total phase data
    main_plot = create_main_stripplot(filtered_df[filtered_df["phase"] == "total"], main_plot_stats, parameter)

    # make stats labels dash components
    formatted_main_plot_stats = []
    for _, row in main_plot_stats.iterrows():
        if  row["model"] == first_model:
            stats_label = html.Div(
                children=["Mean: " + str(row["mean"]), html.Br(), "StD: " + str(row["std"])],
                style={"width": "100px"}
            )
            formatted_main_plot_stats.append(stats_label)
            continue
        stats_label = html.Div(
            children=["Mean: " + str(row["mean"]), html.Br(), "StD: " + str(row["std"])],
            style={"margin-top": "12px", "width": "100px"}
        )
        formatted_main_plot_stats.append(stats_label)

    # create skills plots stats
    # skills_plots_stats: pd.DataFrame = filtered_df.groupby("phase", observed=False)[parameter].agg(["mean", "std"]).reset_index().round(2) 
    skills_by_phase_plots = create_phase_stripplots(filtered_df, parameter)
    
    # data preparation for the pivot table
    skills_by_phase: DataFrameGroupBy = filtered_df.groupby(["model", "phase"], observed=False)[parameter]
    skills_by_phase: DataFrame = (
        skills_by_phase.mean()
        .reset_index()
        .pivot(index="model", columns="phase", values=parameter)
        .round(2)
    )
    skills_by_phase.reset_index(inplace=True)
    skills_by_phase = skills_by_phase.sort_values(by="model")
    table_data = skills_by_phase.to_dict("records")

    # compute percentages

    if parameter == "stddev_OC":
        print(table_data)
        for model_data in table_data:
            for key in model_data:
                if key == 'model':
                    continue
                model_data[key] = round(100 * (exp(model_data[key]) - 1), 2)
        print(table_data)

    # get tpid data
    tpid_list, basic_storm_data = fetch_tpid_data(filtered_df, tpid_base_url)

    return (
        main_plot, 
        table_data, 
        skills_by_phase_plots,
        formatted_main_plot_stats,
        tpid_list,
        basic_storm_data
    )
