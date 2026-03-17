import numpy as np
import pandas as pd
from functools import lru_cache
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# Custom colorscale approximating cmcrameri "roma_r" with lighter extremes
ROMA_LIKE_LIGHT = [
    [0.0, "#f2f2f2"],
    [0.05, "#dfe8f1"],
    [0.2, "#9fc0dd"],
    [0.4, "#5a8ec1"],
    [0.5, "#486fb0"],
    [0.6, "#b36259"],
    [0.8, "#d99b6b"],
    [0.95, "#f0e2cc"],
    [1.0, "#f2f2f2"],
]

# Custom colorscale approximating cmcrameri "vik" (diverging blue-white-red)
VIK_COLORSCALE = [
    [0.0, "#001260"],
    [0.1, "#1a4d99"],
    [0.2, "#4575b4"],
    [0.3, "#74add1"],
    [0.4, "#abd9e9"],
    [0.5, "#e0f3f8"],
    [0.6, "#fee090"],
    [0.7, "#fdae61"],
    [0.8, "#f46d43"],
    [0.9, "#d73027"],
    [1.0, "#67001f"],
]


# Simple in-process figure cache
FIG_CACHE = {}

# ----------------------------
# Data loaders (cached)
# ----------------------------

@lru_cache(maxsize=1)
def load_tec_rmse_npz():
    """
    Loads TEC and TEC RMSE UT-LAT data from the notebook-produced npz.
    Expected keys:
      - 'RMSE_UTLAT': dict(model -> 2D array [lat x ut])
      - 'TEC_UTLAT': dict(model -> 2D array [lat x ut])
      - 'model_latidx': 1D array of latitudes
    """
    path = "MCHUp/MCHUp2/TEC_rmse_UTLAT_map.npz"
    data = np.load(path, allow_pickle=True)
    RMSE_UTLAT = data["RMSE_UTLAT"].item()
    TEC_UTLAT = data["TEC_UTLAT"].item()
    model_latidx = data["model_latidx"]
    return RMSE_UTLAT, TEC_UTLAT, model_latidx


@lru_cache(maxsize=1)
def load_error_utlat_npz():
    """
    Loads GNSS positioning error UT-LAT data from the notebook-produced npz.
    Expected keys:
      - 'ERROR_3D_UTLAT': dict(model -> 2D array [lat x ut])
      - 'ERROR_2D_UTLAT': dict(model -> 2D array [lat x ut])
      - 'ERROR_U_UTLAT' : dict(model -> 2D array [lat x ut])
      - 'ERROR_E_UTLAT' : dict(model -> 2D array [lat x ut])
      - 'ERROR_N_UTLAT' : dict(model -> 2D array [lat x ut])
    """
    path = "MCHUp/MCHUp2/ERROR_UTLAT_map_75125W_60min_SPP.npz"
    data = np.load(path, allow_pickle=True)
    ERROR_3D = data["ERROR_3D_UTLAT"].item()
    ERROR_2D = data["ERROR_2D_UTLAT"].item()
    ERROR_U = data["ERROR_U_UTLAT"].item()
    ERROR_E = data.get("ERROR_E_UTLAT", {}).item() if "ERROR_E_UTLAT" in data else {}
    ERROR_N = data.get("ERROR_N_UTLAT", {}).item() if "ERROR_N_UTLAT" in data else {}
    # Note: lat idx for errors in updated notebook is np.arange(30,51,1)
    model_latidx = np.arange(30, 51, 1)
    return ERROR_3D, ERROR_2D, ERROR_U, ERROR_E, ERROR_N, model_latidx


@lru_cache(maxsize=1)
def load_tec_gradient_npz():
    """
    Loads TEC gradient UT-LAT data from the notebook-produced npz.
    Expected keys:
      - 'TEC_gradient_UTLAT': dict(model -> 2D array [lat x ut])
      - 'model_latidx': 1D array of latitudes
    """
    path = "MCHUp/MCHUp2/TEC_gradient_UTLAT_map.npz"
    data = np.load(path, allow_pickle=True)
    TEC_gradient_UTLAT = data["TEC_gradient_UTLAT"].item()
    model_latidx = data["model_latidx"]
    return TEC_gradient_UTLAT, model_latidx


@lru_cache(maxsize=1)
def load_metric_scores_csv():
    """
    Loads metric_scores_SPP.csv produced by the updated notebook.
    MultiIndex columns, with top level like:
      '3D RMSE', '3D Mean Error', '3D STD',
      '2D RMSE', '2D Mean Error', '2D STD',
      'U RMSE',  'U Mean Error', 'U STD',
      'TEC RMSE','TEC Mean Error','TEC STD', 'TEC TSS'
    Second level are phases: 'quiet phase', 'main phase', 'recovery phase', 'main+recovery'
    Index are model names.
    """
    path = "MCHUp/MCHUp2/metric_scores_SPP.csv"
    df = pd.read_csv(path, header=[0, 1], index_col=0)
    return df


@lru_cache(maxsize=1)
def load_tec_anomaly_scores_csv():
    """
    Loads TEC_anomaly_scores.csv produced by the updated notebook.
    Contains SSIM and TSS scores for TEC anomaly detection.
    MultiIndex columns with top level: 'SSIM', 'TSS'
    Second level are phases: 'Main phase', 'Recovery phase', 'Main+Recovery'
    Index are model names.
    """
    path = "MCHUp/MCHUp2/TEC_anomaly_scores.csv"
    df = pd.read_csv(path, header=[0, 1], index_col=0)
    return df


# ----------------------------
# Common helpers
# ----------------------------

# Model orders as used in the updated notebook
TEC_MODELS = [
    "MadTEC", "Klobuchar", "IRI2020", "IRTAM", "GloTEC", "GIS", "NEDM",
    "CTIPe", "SAMI3-TIEGCM", "SAMI3-HWM", "SAMI3-WACCMX", "SAMI3-MSIS-WACCMX",
    "TIEGCM-Weimer", "TIEGCM-Heelis", "WAMIPE", "WACCMX-Heelis", "GITM", "GITM-FTA-MSIS"
]

RMSE_MODELS = [
    "Klobuchar", "IRI2020", "IRTAM", "GloTEC", "GIS", "NEDM",
    "CTIPe", "SAMI3-TIEGCM", "SAMI3-HWM", "SAMI3-WACCMX", "SAMI3-MSIS-WACCMX",
    "TIEGCM-Weimer", "TIEGCM-Heelis", "WAMIPE", "WACCMX-Heelis", "GITM", "GITM-FTA-MSIS"
]

ERROR_MODELS = [
    "MadTEC", "Klobuchar", "IRI2020", "IRTAM", "GloTEC", "GIS", "NEDM",
    "CTIPe", "SAMI3-TIEGCM", "SAMI3-HWM", "SAMI3-WACCMX", "SAMI3-MSIS-WACCMX",
    "TIEGCM-Weimer", "TIEGCM-Heelis", "WAMIPE", "WACCMX-Heelis", "GITM", "GITM-FTA-MSIS"
]

PHASES = ["quiet phase", "main phase", "recovery phase"]
PHASES_EXTENDED = ["quiet phase", "main phase", "recovery phase", "main+recovery"]

PHASE_LABELS = {
    "quiet phase": "Quiet",
    "main phase": "Main",
    "recovery phase": "Recovery",
    "main+recovery": "Main + Recovery",
}


def _display_phase_label(phase: str) -> str:
    return PHASE_LABELS.get(phase.strip().lower(), phase.title())


def _phase_dropdown_menu(buttons):
    return dict(
        buttons=buttons,
        direction="down",
        pad={"l": 10, "t": 10, "r": 10, "b": 4},
        showactive=True,
        x=-0.25,
        xanchor="left",
        y=1.15,
        yanchor="top",
        font=dict(size=13),
    )


def _make_grid_title(model: str, date_range_str: str):
    return f"{model} {date_range_str}"


def _ensure_range(zmin, zmax):
    if zmin is None or zmax is None:
        return None, None
    if zmin == zmax:
        return None, None
    return zmin, zmax


def _grid_height(rows: int, min_height: int = 350, per_row: int = 220):
    """
    Compute responsive figure height for UT-LAT grids so smaller selections
    fit well in cards. Slightly taller when only 1 row (1–2 models).
    """
    try:
        r = int(rows)
    except Exception:
        r = 1
    if r == 1:
        return 460
    return max(min_height, per_row * r)

# ----------------------------
# UT-LAT heatmap grids
# ----------------------------

def tec_utlat_figure(date_range_str="2024/05/09-05/12", model_names=None):
    """
    Builds a grid of TEC (TECU) heatmaps vs UT (0..95) and Latitude.
    model_names: optional iterable of model keys to display (use TEC_MODELS names).
    """
    _, TEC_UTLAT, model_latidx = load_tec_rmse_npz()
    ut = np.arange(0, 4 * 24, 1)

    # Resolve which models to show (preserve standard order)
    all_models = TEC_MODELS
    if model_names and len(model_names) > 0:
        display_models = [m for m in all_models if m in set(model_names)]
    else:
        display_models = all_models

    n = len(display_models)
    if n == len(all_models):
        rows, cols = 9, 2  # 18 models in 9 rows x 2 columns
    else:
        cols = 2 if n > 1 else 1
        rows = int(np.ceil(n / cols))

    fig = make_subplots(
        rows=rows,
        cols=cols,
        subplot_titles=[_make_grid_title(m, date_range_str) for m in display_models]
    )

    # Color scale for TEC (TECU) - using VIK colorscale
    coloraxis = dict(
        colorscale=VIK_COLORSCALE,
        reversescale=False,
        cmin=0,
        cmax=120,
        colorbar=dict(title="TECU", ticks="outside", tickvals=[0, 30, 60, 90, 120], outlinecolor="black", outlinewidth=1)
    )

    for idx, model in enumerate(display_models):
        r = idx // cols + 1
        c = idx % cols + 1
        if model not in TEC_UTLAT:
            continue
        z = TEC_UTLAT[model]
        # Filled contours (levels 0..120 by 10), colored via shared coloraxis
        fig.add_trace(
            go.Contour(
                x=ut,
                y=model_latidx,
                z=z,
                coloraxis="coloraxis",
                zmin=0,
                zmax=120,
                contours=dict(start=0, end=120, size=10, coloring="heatmap", showlines=False),
                hovertemplate="UT=%{x}h<br>Lat=%{y}<br>TEC=%{z:.2f} TECU<extra>" + model + "</extra>",
            ),
            row=r, col=c
        )
        # Overlay black contour lines with labels at 20 TECU spacing
        fig.add_trace(
            go.Contour(
                x=ut,
                y=model_latidx,
                z=z,
                showscale=False,
                line=dict(color="black", width=1),
                contours=dict(coloring="none", showlines=True, start=0, end=120, size=20, showlabels=True),
                
                hoverinfo="skip"
            ),
            row=r, col=c
        )

    fig.update_layout(
        title="TEC maps as a function of UT and Latitude",
        title_x=0.5,
        coloraxis=coloraxis,
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=_grid_height(rows),
    )
    fig.update_xaxes(
        title_text="UT (hour)",
        tickmode="array",
        tickvals=np.arange(0, 4 * 24 + 1, 12),
        ticktext=(np.arange(0, 4 * 24 + 1, 12) % 24),
        showline=True, linewidth=2, linecolor="black", mirror=True
    )
    fig.update_yaxes(title_text="Lat", showline=True, linewidth=2, linecolor="black", mirror=True)
    return fig


def tec_rmse_utlat_figure(date_range_str="2024/05/09-05/12", model_names=None):
    """
    Builds a grid of TEC RMSE (TECU) heatmaps vs UT and Latitude,
    for models defined in RMSE_MODELS, using MCHUp/TEC_rmse_UTLAT_map.npz.
    model_names: optional iterable of model keys to display (use RMSE_MODELS names).
    """
    RMSE_UTLAT, _, model_latidx = load_tec_rmse_npz()
    ut = np.arange(0, 4 * 24, 1)

    # Resolve which models to show (preserve standard order)
    all_models = RMSE_MODELS
    if model_names and len(model_names) > 0:
        display_models = [m for m in all_models if m in set(model_names)]
    else:
        display_models = all_models

    n = len(display_models)
    if n == len(all_models):
        rows, cols = 9, 2  # 17 models in 9 rows x 2 columns (last row has 1)
    else:
        cols = 2 if n > 1 else 1
        rows = int(np.ceil(n / cols))

    fig = make_subplots(
        rows=rows,
        cols=cols,
        subplot_titles=[_make_grid_title(m, date_range_str) for m in display_models]
    )

    # Color scheme using VIK colorscale
    coloraxis = dict(
        colorscale=VIK_COLORSCALE,
        reversescale=False,
        colorbar=dict(title="RMSE (TECU)", outlinecolor="black", outlinewidth=1)
    )

    for idx, model in enumerate(display_models):
        r = idx // cols + 1
        c = idx % cols + 1
        if model not in RMSE_UTLAT:
            continue
        z = RMSE_UTLAT[model]
        fig.add_trace(
            go.Heatmap(
                x=ut,
                y=model_latidx,
                z=z,
                coloraxis="coloraxis",
                hovertemplate="UT=%{x}h<br>Lat=%{y}<br>RMSE=%{z:.2f} TECU<extra>" + model + "</extra>",
            ),
            row=r, col=c
        )

        # optional contour overlays (labels become crowded in plotly; using thin lines)
        fig.add_trace(
            go.Contour(
                x=ut, y=model_latidx, z=z, showscale=False, line=dict(color="black", width=1),
                contours=dict(showlines=True, coloring="none"),
                hoverinfo="skip"
            ),
            row=r, col=c
        )

    fig.update_layout(
        title="TEC RMSE as a function of UT and Latitude",
        title_x=0.5,
        coloraxis=coloraxis,
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=_grid_height(rows),
    )
    fig.update_xaxes(
        title_text="UT (hour)",
        tickmode="array",
        tickvals=np.arange(0, 4 * 24 + 1, 12),
        ticktext=(np.arange(0, 4 * 24 + 1, 12) % 24),
        showline=True, linewidth=2, linecolor="black", mirror=True
    )
    fig.update_yaxes(title_text="Lat", showline=True, linewidth=2, linecolor="black", mirror=True)
    return fig


def gnss_error_utlat_figure(kind="3D", date_range_str="2024/05/09-05/12", model_names=None):
    """
    Builds a grid of GNSS positioning error heatmaps vs UT and Latitude.
    kind: '3D', '2D', 'U', 'E', or 'N'
    Uses MCHUp/MCHUp2/ERROR_UTLAT_map_75125W_60min_SPP.npz.
    model_names: optional iterable of model keys to display (use ERROR_MODELS names).
    """
    ERROR_3D, ERROR_2D, ERROR_U, ERROR_E, ERROR_N, model_latidx = load_error_utlat_npz()
    ut = np.arange(0, 4 * 24, 1)

    # choose data and colorbar title
    if kind.upper() == "3D":
        source = ERROR_3D
        cbar_title = "3D Error (m)"
        levels = [0, 5, 10, 15, 20]
    elif kind.upper() == "2D":
        source = ERROR_2D
        cbar_title = "2D Error (m)"
        levels = [0, 5, 10, 15, 20]
    elif kind.upper() == "E":
        source = ERROR_E
        cbar_title = "East Error (m)"
        levels = [-6, -2, 0, 2, 6]
    elif kind.upper() == "N":
        source = ERROR_N
        cbar_title = "North Error (m)"
        levels = [-6, -2, 0, 2, 6]
    else:  # U
        source = ERROR_U
        cbar_title = "Up Error (m)"
        levels = [-6, -2, 0, 2, 6]

    # Resolve which models to show (preserve standard order)
    all_models = ERROR_MODELS
    if model_names and len(model_names) > 0:
        display_models = [m for m in all_models if m in set(model_names)]
    else:
        display_models = all_models

    n = len(display_models)
    if n == len(all_models):
        rows, cols = 9, 2  # 18 models in 9 rows x 2 columns
    else:
        cols = 2 if n > 1 else 1
        rows = int(np.ceil(n / cols))

    fig = make_subplots(
        rows=rows,
        cols=cols,
        subplot_titles=[_make_grid_title(m, date_range_str) for m in display_models]
    )

    # Use VIK colorscale for all error plots
    coloraxis = dict(
        colorscale=VIK_COLORSCALE,
        reversescale=False,
        colorbar=dict(title=cbar_title, outlinecolor="black", outlinewidth=1)
    )

    for idx, model in enumerate(display_models):
        r = idx // cols + 1
        c = idx % cols + 1
        z = source.get(model)
        if z is None:
            continue
        fig.add_trace(
            go.Heatmap(
                x=ut,
                y=model_latidx,
                z=z,
                coloraxis="coloraxis",
                hovertemplate="UT=%{x}h<br>Lat=%{y}<br>Error=%{z:.2f} m<extra>" + model + "</extra>",
            ),
            row=r, col=c
        )

        # contour overlays for quick reading
        fig.add_trace(
            go.Contour(
                x=ut, y=model_latidx, z=z, showscale=False, line=dict(color="black", width=1),
                contours=dict(showlines=True, coloring="none", start=levels[0], end=levels[-1]),
                hoverinfo="skip"
            ),
            row=r, col=c
        )

    fig.update_layout(
        title=f"GNSS {kind.upper()} positioning error as a function of UT and Latitude",
        title_x=0.5,
        coloraxis=coloraxis,
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=_grid_height(rows),
    )
    fig.update_xaxes(
        title_text="UT (hour)",
        tickmode="array",
        tickvals=np.arange(0, 4 * 24 + 1, 12),
        ticktext=(np.arange(0, 4 * 24 + 1, 12) % 24),
        showline=True, linewidth=2, linecolor="black", mirror=True
    )
    fig.update_yaxes(title_text="Lat", showline=True, linewidth=2, linecolor="black", mirror=True)
    return fig


def tec_gradient_utlat_figure(date_range_str="2024/05/09-05/12", model_names=None):
    """
    Builds a grid of TEC gradient heatmaps vs UT and Latitude.
    Shows gradient in dTECU/100km.
    model_names: optional iterable of model keys to display (use TEC_MODELS names).
    """
    TEC_gradient_UTLAT, model_latidx = load_tec_gradient_npz()
    ut = np.arange(0, 4 * 24, 1)

    # Resolve which models to show (preserve standard order)
    all_models = TEC_MODELS
    if model_names and len(model_names) > 0:
        display_models = [m for m in all_models if m in set(model_names)]
    else:
        display_models = all_models

    n = len(display_models)
    if n == len(all_models):
        rows, cols = 9, 2  # 18 models in 9 rows x 2 columns
    else:
        cols = 2 if n > 1 else 1
        rows = int(np.ceil(n / cols))

    fig = make_subplots(
        rows=rows,
        cols=cols,
        subplot_titles=[_make_grid_title(m if m != "MadTEC" else "Madrigal TEC", date_range_str) for m in display_models]
    )

    # Color scheme using VIK colorscale
    coloraxis = dict(
        colorscale=VIK_COLORSCALE,
        reversescale=False,
        cmin=0,
        cmax=6,
        colorbar=dict(title="dTECU/100km", ticks="outside", tickvals=[0, 2, 4, 6], outlinecolor="black", outlinewidth=1)
    )

    for idx, model in enumerate(display_models):
        r = idx // cols + 1
        c = idx % cols + 1
        if model not in TEC_gradient_UTLAT:
            continue
        z = TEC_gradient_UTLAT[model]
        fig.add_trace(
            go.Heatmap(
                x=ut,
                y=model_latidx,
                z=z,
                coloraxis="coloraxis",
                hovertemplate="UT=%{x}h<br>Lat=%{y}<br>Gradient=%{z:.2f} dTECU/100km<extra>" + model + "</extra>",
            ),
            row=r, col=c
        )

    fig.update_layout(
        title="TEC Gradient - 2024/05/09-05/12",
        title_x=0.5,
        coloraxis=coloraxis,
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=_grid_height(rows),
    )
    fig.update_xaxes(
        title_text="UT (hour)",
        tickmode="array",
        tickvals=np.arange(0, 4 * 24 + 1, 12),
        ticktext=(np.arange(0, 4 * 24 + 1, 12) % 24),
        showline=True, linewidth=2, linecolor="black", mirror=True
    )
    fig.update_yaxes(title_text="Lat", showline=True, linewidth=2, linecolor="black", mirror=True)
    return fig


def tec_gradient_rmse_utlat_figure(date_range_str="2024/05/09-05/12", model_names=None):
    """
    Builds a grid of TEC gradient RMSE heatmaps vs UT and Latitude.
    Shows absolute difference from MadTEC gradient.
    model_names: optional iterable of model keys to display (use RMSE_MODELS names).
    """
    TEC_gradient_UTLAT, model_latidx = load_tec_gradient_npz()
    ut = np.arange(0, 4 * 24, 1)

    # Resolve which models to show (exclude MadTEC for RMSE)
    all_models = RMSE_MODELS
    if model_names and len(model_names) > 0:
        display_models = [m for m in all_models if m in set(model_names)]
    else:
        display_models = all_models

    n = len(display_models)
    if n == len(all_models):
        rows, cols = 9, 2  # 17 models in 9 rows x 2 columns (last row has 1)
    else:
        cols = 2 if n > 1 else 1
        rows = int(np.ceil(n / cols))

    fig = make_subplots(
        rows=rows,
        cols=cols,
        subplot_titles=[_make_grid_title(m, date_range_str) for m in display_models]
    )

    # Color scheme using VIK colorscale
    coloraxis = dict(
        colorscale=VIK_COLORSCALE,
        reversescale=False,
        cmin=0,
        cmax=10,
        colorbar=dict(title="TECU/100km", ticks="outside", tickvals=[0, 2, 4, 6, 8, 10], outlinecolor="black", outlinewidth=1)
    )

    ref_gradient = TEC_gradient_UTLAT.get("MadTEC")
    if ref_gradient is None:
        # Return empty figure if reference not available
        fig.update_layout(
            title="TEC Gradient Error - Reference (MadTEC) not found",
            plot_bgcolor="white", paper_bgcolor="white"
        )
        return fig

    for idx, model in enumerate(display_models):
        r = idx // cols + 1
        c = idx % cols + 1
        if model not in TEC_gradient_UTLAT:
            continue
        z = np.abs(TEC_gradient_UTLAT[model] - ref_gradient)
        fig.add_trace(
            go.Heatmap(
                x=ut,
                y=model_latidx,
                z=z,
                coloraxis="coloraxis",
                hovertemplate="UT=%{x}h<br>Lat=%{y}<br>Error=%{z:.2f} TECU/100km<extra>" + model + "</extra>",
            ),
            row=r, col=c
        )

        # Add contour lines
        fig.add_trace(
            go.Contour(
                x=ut, y=model_latidx, z=z, showscale=False, line=dict(color="black", width=1),
                contours=dict(showlines=True, coloring="none", start=1, end=9, size=2, showlabels=True),
                hoverinfo="skip"
            ),
            row=r, col=c
        )

    fig.update_layout(
        title="TEC Gradient Error - 2024/05/09-05/12",
        title_x=0.5,
        coloraxis=coloraxis,
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=_grid_height(rows),
    )
    fig.update_xaxes(
        title_text="UT (hour)",
        tickmode="array",
        tickvals=np.arange(0, 4 * 24 + 1, 12),
        ticktext=(np.arange(0, 4 * 24 + 1, 12) % 24),
        showline=True, linewidth=2, linecolor="black", mirror=True
    )
    fig.update_yaxes(title_text="Lat", showline=True, linewidth=2, linecolor="black", mirror=True)
    return fig


def relative_tec_change_figure(date_range_str="2024/05/10-05/12", model_names=None):
    """
    Builds a grid of relative TEC change heatmaps vs UT and Latitude.
    Shows percentage change relative to quiet day (first 24 hours).
    Only displays 3 days (hours 24-96), excluding the quiet reference day.
    model_names: optional iterable of model keys to display (use TEC_MODELS names).
    """
    _, TEC_UTLAT, _ = load_tec_rmse_npz()
    
    # Use latitude range from notebook: 30-51
    model_latidx = np.arange(30, 51, 1)
    ut = np.arange(0, 3 * 24, 1)  # Only 3 days (24-96 hours)

    # Resolve which models to show
    all_models = TEC_MODELS
    if model_names and len(model_names) > 0:
        display_models = [m for m in all_models if m in set(model_names)]
    else:
        display_models = all_models

    n = len(display_models)
    if n == len(all_models):
        rows, cols = 9, 2  # 18 models in 9 rows x 2 columns
    else:
        cols = 2 if n > 1 else 1
        rows = int(np.ceil(n / cols))

    fig = make_subplots(
        rows=rows,
        cols=cols,
        subplot_titles=[_make_grid_title(m if m != "MadTEC" else "Madrigal TEC", date_range_str) for m in display_models]
    )

    # Storm phase markers (adjusted for 3-day display starting from hour 24)
    main_ph = 26 + 24 - 24  # Adjusted to 3-day window
    quiet_ph = 24 + 17 + 40/60 - 24

    for idx, model in enumerate(display_models):
        r = idx // cols + 1
        c = idx % cols + 1
        if model not in TEC_UTLAT:
            continue
        
        # Get TEC data and extract relevant latitude range
        tec_full = TEC_UTLAT[model]
        # Extract latitude indices 30-51 from the full data
        lat_start_idx = 30 - model_latidx[0] if len(tec_full) > 30 else 0
        lat_end_idx = lat_start_idx + len(model_latidx)
        tec_data = tec_full[lat_start_idx:lat_end_idx, :]
        
        # Calculate reference (first 24 hours, tiled to match full period)
        tec_ref = np.tile(tec_data[:, :24], (1, 4))
        
        # Calculate relative change
        with np.errstate(divide='ignore', invalid='ignore'):
            tec_change = (tec_data - tec_ref) / tec_ref * 100
            tec_change = np.nan_to_num(tec_change, nan=0.0, posinf=0.0, neginf=0.0)
        
        # Extract only days 2-4 (hours 24-96)
        tec_change_display = tec_change[:, 24:96]
        
        # Determine levels based on model (NEDM has different scale)
        if model == "NEDM":
            levels_fill = np.arange(-10, 11, 1)
            levels_contour = np.arange(-10, 11, 2.5)
            coloraxis_key = "coloraxis2"
        else:
            levels_fill = np.arange(-100, 110, 10)
            levels_contour = np.arange(-100, 110, 20)
            coloraxis_key = "coloraxis"
        
        fig.add_trace(
            go.Contour(
                x=ut,
                y=model_latidx,
                z=tec_change_display,
                coloraxis=coloraxis_key,
                contours=dict(start=levels_fill[0], end=levels_fill[-1], size=levels_fill[1]-levels_fill[0], coloring="heatmap", showlines=False),
                hovertemplate="UT=%{x}h<br>Lat=%{y}<br>Change=%{z:.1f}%<extra>" + model + "</extra>",
            ),
            row=r, col=c
        )
        
        # Add contour lines
        fig.add_trace(
            go.Contour(
                x=ut, y=model_latidx, z=tec_change_display, showscale=False,
                line=dict(color="black", width=1),
                contours=dict(showlines=True, coloring="none", start=levels_contour[0], end=levels_contour[-1], size=levels_contour[1]-levels_contour[0], showlabels=True),
                hoverinfo="skip"
            ),
            row=r, col=c
        )
        
        # Add shaded region for main phase
        fig.add_shape(
            type="rect",
            x0=quiet_ph, x1=main_ph,
            y0=model_latidx[0], y1=model_latidx[-1],
            fillcolor="yellow", opacity=0.2,
            layer="below", line_width=0,
            row=r, col=c
        )

    # Color schemes
    coloraxis = dict(
        colorscale=VIK_COLORSCALE,
        reversescale=False,
        cmin=-100,
        cmax=100,
        colorbar=dict(title="%", ticks="outside", tickvals=[-100, -50, 0, 50, 100], outlinecolor="black", outlinewidth=1)
    )
    
    coloraxis2 = dict(
        colorscale=VIK_COLORSCALE,
        reversescale=False,
        cmin=-10,
        cmax=10,
        colorbar=dict(title="%", ticks="outside", tickvals=[-10, -5, 0, 5, 10], outlinecolor="black", outlinewidth=1)
    )

    fig.update_layout(
        title="Relative Vertical TEC Change (vs. Quiet Day 5/9) - 2024/05/10-05/12",
        title_x=0.5,
        coloraxis=coloraxis,
        coloraxis2=coloraxis2,
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=_grid_height(rows),
    )
    fig.update_xaxes(
        title_text="UT (hour)",
        tickmode="array",
        tickvals=np.arange(0, 3 * 24 + 1, 12),
        ticktext=(np.arange(0, 3 * 24 + 1, 12) % 24),
        showline=True, linewidth=2, linecolor="black", mirror=True
    )
    fig.update_yaxes(title_text="Lat", showline=True, linewidth=2, linecolor="black", mirror=True)
    return fig


# ----------------------------
# Metric score scatter plots
# ----------------------------

def metric_scatter_figure(var_label: str, title_prefix: str = "", unit: str = ""):
    """
    Builds a 1x3 horizontal scatter panel for the given metric variable across phases.
    var_label should match top-level column in metric_scores.csv, e.g. 'TEC RMSE' or '3D RMSE'.
    """
    df = load_metric_scores_csv()

    if var_label not in df.columns.levels[0]:
        # Return an informative empty figure
        fig = go.Figure()
        fig.update_layout(
            title=f"Metric '{var_label}' not found in metric_scores.csv",
            plot_bgcolor="white", paper_bgcolor="white"
        )
        return fig

    models = list(df.index)
    fig = make_subplots(
        rows=1,
        cols=3,
        subplot_titles=[f"{title_prefix}{var_label} {ph}" for ph in PHASES],
        horizontal_spacing=0.08,
        shared_yaxes=True
    )

    colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]

    for i, phase in enumerate(PHASES):
        sub = df[(var_label, phase)].dropna()
        # Keep y order as in models when possible
        y_models = [m for m in models if m in sub.index]
        x_vals = sub.loc[y_models].values if len(y_models) > 0 else []

        # main scatter
        fig.add_trace(
            go.Scatter(
                x=x_vals,
                y=y_models,
                mode="markers+text",
                marker=dict(color=colors[i], size=10),
                text=[f"{v:.2f}" for v in x_vals],
                textposition="middle right",
                name=phase,
                showlegend=False,
                hovertemplate="%{y}: %{x:.2f}" + (f" {unit}" if unit else "") + "<extra></extra>",
            ),
            row=1, col=i + 1
        )

        # baseline vertical line for Klobuchar if present
        if "Klobuchar" in sub.index:
            base_x = float(sub.loc["Klobuchar"])
            fig.add_vline(
                x=base_x,
                line_width=2,
                line_dash="dash",
                line_color="red",
                row=1, col=i + 1
            )

        fig.update_xaxes(
            title_text=f"Error{f' ({unit})' if unit else ''}",
            showline=True, linewidth=2, linecolor="black", mirror=True,
            row=1, col=i + 1
        )
        if i == 0:
            fig.update_yaxes(
                title_text="Model",
                showline=True, linewidth=2, linecolor="black", mirror=True,
                tickfont=dict(size=9),
                ticks="outside",
                ticklabelposition="outside",
                ticklabelstandoff=6,
                automargin=True,
                row=1, col=1
            )
        else:
            fig.update_yaxes(
                title_text=None,
                showline=True, linewidth=2, linecolor="black", mirror=True,
                showticklabels=False,
                row=1, col=i + 1
            )

    fig.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=460,
        margin=dict(l=160, r=30, t=70, b=50),
        uniformtext_minsize=9,
        uniformtext_mode="hide"
    )
    return fig


def tec_rmse_metric_scatter():
    return metric_scatter_figure(var_label="TEC RMSE", title_prefix="", unit="TECU")


def ppp3d_metric_scatter():
    # Notebook uses label "SF PPP 3D error" context; in CSV the relevant column is "3D RMSE"
    return metric_scatter_figure(var_label="3D RMSE", title_prefix="SF PPP ", unit="meter")


# ----------------------------
# New metric bar chart functions
# ----------------------------

def tec_rmse_metric_bars():
    """
    Builds horizontal bar chart for TEC RMSE with dropdown to select phase.
    Uses Plotly updatemenus for phase selection.
    Bars are gray by default, blue if better than Klobuchar.
    Excludes MadTEC from display.
    """
    df = load_metric_scores_csv()
    
    if "TEC RMSE" not in df.columns.levels[0]:
        fig = go.Figure()
        fig.update_layout(
            title="TEC RMSE not found in metric_scores_SPP.csv",
            plot_bgcolor="white", paper_bgcolor="white"
        )
        return fig
    
    # Exclude Madrigal/MadTEC reference row (not a model skill score)
    df_filtered = df[~df.index.isin(["MadTEC", "Madrigal TEC"])]
    models = list(df_filtered.index)
    
    gray_color = "#808080"
    blue_color = "#4575b4"
    
    fig = go.Figure()
    
    # Create traces for each phase
    for i, ph in enumerate(PHASES_EXTENDED):
        if ("TEC RMSE", ph) not in df_filtered.columns:
            continue
            
        sub = df_filtered[("TEC RMSE", ph)].dropna()
        y_models = [m for m in models if m in sub.index]
        x_vals = sub.loc[y_models].values if len(y_models) > 0 else []
        
        # Determine bar colors
        klob_val = sub.loc["Klobuchar"] if "Klobuchar" in sub.index else None
        colors = []
        for model, val in zip(y_models, x_vals):
            if klob_val is not None and val < klob_val:
                colors.append(blue_color)
            else:
                colors.append(gray_color)

        # Reverse ordering so top-to-bottom matches the original notebook ordering
        y_models = list(reversed(y_models))
        try:
            x_vals = x_vals[::-1]
        except Exception:
            x_vals = list(reversed(list(x_vals))) if len(x_vals) else []
        colors = list(reversed(colors))
        
        # First phase visible, others hidden
        visible = True if i == 0 else 'legendonly'
        
        fig.add_trace(
            go.Bar(
                x=x_vals,
                y=y_models,
                orientation='h',
                marker=dict(color=colors),
                text=[f"{v:.2f}" for v in x_vals],
                textposition="outside",
                name=ph,
                visible=visible,
                hovertemplate="%{y}: %{x:.2f} TECU<extra></extra>",
            )
        )
    
    # Create dropdown buttons for phase selection
    buttons = []
    for i, ph in enumerate(PHASES_EXTENDED):
        visibility = [j == i for j in range(len(PHASES_EXTENDED))]
        buttons.append(
            dict(
                args=[{"visible": visibility}],
                label=_display_phase_label(ph),
                method="update"
            )
        )
    
    fig.update_layout(
        title=dict(text="TEC RMSE", x=0.5, xanchor="center"),
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=500,
        margin=dict(l=160, r=80, t=70, b=50),
        updatemenus=[
            _phase_dropdown_menu(buttons)
        ]
    )
    
    fig.update_xaxes(
        title_text="Error (TECU)",
        range=[0, 50],
        showline=True, linewidth=2, linecolor="black", mirror=True
    )
    fig.update_yaxes(
        showline=True, linewidth=2, linecolor="black", mirror=True,
        tickfont=dict(size=10),
        automargin=True
    )
    
    return fig


def tec_tss_metric_bars():
    """
    Builds a horizontal bar chart for TEC TSS with dropdown to select phase.
    Bars are gray by default, blue if better than Klobuchar.
    Excludes MadTEC from display.
    """
    df = load_tec_anomaly_scores_csv()
    
    if "TSS" not in df.columns.levels[0]:
        fig = go.Figure()
        fig.update_layout(
            title="TSS not found in TEC_anomaly_scores.csv",
            plot_bgcolor="white", paper_bgcolor="white"
        )
        return fig
    
    # Exclude MadTEC
    df_filtered = df[df.index != "MadTEC"]
    models = list(df_filtered.index)

    # Phases in anomaly scores use different naming
    anomaly_phases = ["Main phase", "Recovery phase", "Main+Recovery"]

    gray_color = "#808080"
    blue_color = "#4575b4"

    fig = go.Figure()
    trace_phases = []

    for i, phase in enumerate(anomaly_phases):
        if ("TSS", phase) not in df_filtered.columns:
            logger.debug("TEC TSS: phase missing in CSV: %s", phase)
            continue

        sub = df_filtered[("TSS", phase)].dropna()
        y_models = [m for m in models if m in sub.index]
        x_vals = sub.loc[y_models].values if len(y_models) > 0 else []

        # Determine bar colors (higher TSS is better)
        klob_val = sub.loc["Klobuchar"] if "Klobuchar" in sub.index else None
        colors = [blue_color if (klob_val is not None and v > klob_val) else gray_color for v in x_vals]

        # Reverse ordering so top-to-bottom matches the original notebook ordering
        y_models = list(reversed(y_models))
        try:
            x_vals = x_vals[::-1]
        except Exception:
            x_vals = list(reversed(list(x_vals))) if len(x_vals) else []
        colors = list(reversed(colors))

        visible = True if len(trace_phases) == 0 else False
        trace_phases.append(_display_phase_label(phase))

        fig.add_trace(
            go.Bar(
                x=x_vals,
                y=y_models,
                orientation="h",
                marker=dict(color=colors),
                text=[f"{v:.2f}" for v in x_vals],
                textposition="outside",
                name=phase,
                visible=visible,
                hovertemplate="%{y}: %{x:.2f}<extra></extra>",
            )
        )

    if len(trace_phases) == 0:
        fig.update_layout(
            title="No TEC TSS phases found in TEC_anomaly_scores.csv",
            plot_bgcolor="white", paper_bgcolor="white",
        )
        return fig

    # Dropdown buttons for phase selection
    buttons = []
    for i, ph in enumerate(trace_phases):
        visibility = [j == i for j in range(len(trace_phases))]
        buttons.append(
            dict(
                args=[{"visible": visibility}],
                label=ph,
                method="update",
            )
        )

    fig.update_layout(
        title=dict(text="TEC TSS", x=0.5, xanchor="center"),
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=500,
        margin=dict(l=160, r=80, t=70, b=50),
        updatemenus=[
            _phase_dropdown_menu(buttons)
        ],
    )

    fig.update_xaxes(
        title_text="TSS",
        range=[0, 1],
        showline=True, linewidth=2, linecolor="black", mirror=True,
    )
    fig.update_yaxes(
        showline=True, linewidth=2, linecolor="black", mirror=True,
        tickfont=dict(size=10),
        automargin=True,
    )

    return fig


def ssim_metric_bars():
    """
    Builds a horizontal bar chart for SSIM with dropdown to select phase.
    All bars are blue.
    Excludes MadTEC from display.
    """
    df = load_tec_anomaly_scores_csv()
    
    if "SSIM" not in df.columns.levels[0]:
        fig = go.Figure()
        fig.update_layout(
            title="SSIM not found in TEC_anomaly_scores.csv",
            plot_bgcolor="white", paper_bgcolor="white"
        )
        return fig
    
    # Exclude MadTEC
    df_filtered = df[df.index != "MadTEC"]
    models = list(df_filtered.index)

    # Phases in anomaly scores use different naming
    anomaly_phases = ["Main phase", "Recovery phase", "Main+Recovery"]

    blue_color = "#4575b4"

    fig = go.Figure()
    trace_phases = []

    for i, phase in enumerate(anomaly_phases):
        if ("SSIM", phase) not in df_filtered.columns:
            logger.debug("SSIM: phase missing in CSV: %s", phase)
            continue

        sub = df_filtered[("SSIM", phase)].dropna()
        y_models = [m for m in models if m in sub.index]
        x_vals = sub.loc[y_models].values if len(y_models) > 0 else []

        # Reverse ordering so top-to-bottom matches the original notebook ordering
        y_models = list(reversed(y_models))
        try:
            x_vals = x_vals[::-1]
        except Exception:
            x_vals = list(reversed(list(x_vals))) if len(x_vals) else []

        visible = True if len(trace_phases) == 0 else False
        trace_phases.append(_display_phase_label(phase))

        fig.add_trace(
            go.Bar(
                x=x_vals,
                y=y_models,
                orientation="h",
                marker=dict(color=blue_color),
                text=[f"{v:.2f}" for v in x_vals],
                textposition="outside",
                name=phase,
                visible=visible,
                hovertemplate="%{y}: %{x:.2f}<extra></extra>",
            )
        )

    if len(trace_phases) == 0:
        fig.update_layout(
            title="No SSIM phases found in TEC_anomaly_scores.csv",
            plot_bgcolor="white", paper_bgcolor="white",
        )
        return fig

    buttons = []
    for i, ph in enumerate(trace_phases):
        visibility = [j == i for j in range(len(trace_phases))]
        buttons.append(
            dict(
                args=[{"visible": visibility}],
                label=ph,
                method="update",
            )
        )

    fig.update_layout(
        title=dict(text="SSIM", x=0.5, xanchor="center"),
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=500,
        margin=dict(l=160, r=80, t=70, b=50),
        updatemenus=[
            _phase_dropdown_menu(buttons)
        ],
    )

    fig.update_xaxes(
        title_text="SSIM",
        range=[-0.2, 1],
        showline=True, linewidth=2, linecolor="black", mirror=True,
    )
    fig.update_yaxes(
        showline=True, linewidth=2, linecolor="black", mirror=True,
        tickfont=dict(size=10),
        automargin=True,
    )

    return fig


def positioning_rmse_metric_bars(error_type="3D"):
    """
    Builds a horizontal bar chart for positioning RMSE with dropdown to select phase.
    error_type: '3D', '2D', or 'U'
    Bars are gray by default, blue if better than Klobuchar.
    """
    df = load_metric_scores_csv()
    
    var_label = f"{error_type.upper()} RMSE"
    if var_label not in df.columns.levels[0]:
        fig = go.Figure()
        fig.update_layout(
            title=f"{var_label} not found in metric_scores_SPP.csv",
            plot_bgcolor="white", paper_bgcolor="white"
        )
        return fig
    
    models = list(df.index)
    
    # Determine x-axis range based on error type
    if error_type.upper() == "3D":
        x_range = [0, 20]
        title_text = "3D RMSE"
    elif error_type.upper() == "2D":
        x_range = [0, 10]
        title_text = "2D RMSE"
    else:  # U
        x_range = [0, 10]
        title_text = "Up RMSE"
    
    gray_color = "#808080"
    blue_color = "#4575b4"

    fig = go.Figure()
    trace_phases = []

    for i, phase in enumerate(PHASES_EXTENDED):
        if (var_label, phase) not in df.columns:
            logger.debug("%s: phase missing in metric_scores_SPP.csv: %s", var_label, phase)
            continue

        sub = df[(var_label, phase)].dropna()
        y_models = [m for m in models if m in sub.index]
        x_vals = sub.loc[y_models].values if len(y_models) > 0 else []

        # Determine bar colors based on Klobuchar comparison (lower RMSE is better)
        klob_val = sub.loc["Klobuchar"] if "Klobuchar" in sub.index else None
        colors = [blue_color if (klob_val is not None and v < klob_val) else gray_color for v in x_vals]

        # Reverse ordering so top-to-bottom matches the original notebook ordering
        y_models = list(reversed(y_models))
        try:
            x_vals = x_vals[::-1]
        except Exception:
            x_vals = list(reversed(list(x_vals))) if len(x_vals) else []
        colors = list(reversed(colors))

        visible = True if len(trace_phases) == 0 else False
        trace_phases.append(_display_phase_label(phase))

        fig.add_trace(
            go.Bar(
                x=x_vals,
                y=y_models,
                orientation="h",
                marker=dict(color=colors),
                text=[f"{v:.2f}" for v in x_vals],
                textposition="outside",
                name=phase,
                visible=visible,
                hovertemplate="%{y}: %{x:.2f} m<extra></extra>",
            )
        )

    if len(trace_phases) == 0:
        fig.update_layout(
            title=f"No phases found for {var_label} in metric_scores_SPP.csv",
            plot_bgcolor="white", paper_bgcolor="white",
        )
        return fig

    # Dropdown buttons for phase selection
    buttons = []
    for i, ph in enumerate(trace_phases):
        visibility = [j == i for j in range(len(trace_phases))]
        title_suffix = " (w)" if ph == "main+recovery" else ""
        buttons.append(
            dict(
                args=[{"visible": visibility}],
                label=ph + title_suffix,
                method="update",
            )
        )

    # Initial title uses first available trace phase
    init_ph = trace_phases[0]
    init_suffix = " (w)" if init_ph == "main+recovery" else ""
    fig.update_layout(
        title=dict(text=title_text, x=0.5, xanchor="center"),
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=500,
        margin=dict(l=160, r=80, t=70, b=50),
        updatemenus=[
            _phase_dropdown_menu(buttons)
        ],
    )

    fig.update_xaxes(
        title_text="Error (meter)",
        range=x_range,
        showline=True, linewidth=2, linecolor="black", mirror=True,
    )
    fig.update_yaxes(
        showline=True, linewidth=2, linecolor="black", mirror=True,
        tickfont=dict(size=10),
        automargin=True,
    )

    return fig


def sppp_dst_kp_plot():
    """
    Build DST/KP figure for Single Frequency GNSS PPP using MCHUp/MCHUp2/kp_dst.txt
    Two stacked subplots with shaded main phase region, matching notebook style.
    """
    import os
    from plotly.subplots import make_subplots
    from datetime import datetime, timedelta

    path = "MCHUp/MCHUp2/kp_dst.txt"
    with open(path, "r") as f:
        text = f.readlines()

    # Parse file (kp at col 3 scaled by 1/10, dst at col 4)
    n = len(text)
    dst_ut = np.arange(24 * 4)
    arr = np.zeros((n, 5), dtype=float)
    for i, line in enumerate(text):
        parts = line.split()
        if len(parts) >= 5:
            arr[i, 0] = int(parts[0])
            arr[i, 1] = int(parts[1])
            arr[i, 2] = int(parts[2])
            arr[i, 3] = int(parts[3]) / 10.0  # kp
            arr[i, 4] = int(parts[4])         # dst

    # Storm phase markers from the notebook
    main_ph = 26 + 24
    quiet_ph = 24 + 17 + 40 / 60

    # Create figure with 2 stacked subplots sharing x-axis
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.12,
        row_heights=[0.4, 0.6],
        subplot_titles=("", "")
    )
    
    # Top subplot: Kp Index (bar chart)
    fig.add_trace(
        go.Bar(
            x=dst_ut,
            y=arr[:len(dst_ut), 3],
            marker_color="steelblue",
            name="Kp",
            showlegend=False
        ),
        row=1, col=1
    )
    
    # Add shaded region for main phase (Kp subplot)
    fig.add_shape(
        type="rect",
        x0=quiet_ph, x1=main_ph,
        y0=0, y1=10,
        fillcolor="gray", opacity=0.3,
        layer="below", line_width=0,
        row=1, col=1
    )
    
    # Bottom subplot: Dst Index (line plot)
    fig.add_trace(
        go.Scatter(
            x=dst_ut,
            y=arr[:len(dst_ut), 4],
            mode="lines",
            line=dict(color="red", width=3),
            name="Dst",
            showlegend=False
        ),
        row=2, col=1
    )
    
    # Add shaded region for main phase (Dst subplot)
    fig.add_shape(
        type="rect",
        x0=quiet_ph, x1=main_ph,
        y0=-500, y1=200,
        fillcolor="gray", opacity=0.3,
        layer="below", line_width=0,
        row=2, col=1
    )
    
    # Add phase labels to Dst subplot
    fig.add_annotation(
        x=quiet_ph - 20, y=100,
        text="Quiet Phase",
        showarrow=False,
        font=dict(size=12, color="black"),
        xref="x2", yref="y2"
    )
    fig.add_annotation(
        x=quiet_ph + 4, y=50,
        text="Main<br>Phase",
        showarrow=False,
        font=dict(size=12, color="black"),
        xref="x2", yref="y2"
    )
    fig.add_annotation(
        x=main_ph + 17, y=100,
        text="Recovery Phase",
        showarrow=False,
        font=dict(size=12, color="black"),
        xref="x2", yref="y2"
    )

    # Update layout
    fig.update_layout(
        title="2024 Gannon Storm",
        title_x=0.5,
        title_font=dict(size=16, color="black"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        height=450
    )

    # Match original notebook styling: light gray grid with both major + minor lines
    major_grid_color = "#bdbdbd"
    minor_grid_color = "#e0e0e0"
    
    # Update Kp y-axis (top subplot)
    fig.update_yaxes(
        title_text="Kp Index",
        range=[0, 10],
        showgrid=True,
        gridcolor=major_grid_color,
        gridwidth=1,
        dtick=2,
        minor=dict(
            tickmode="linear",
            tick0=0,
            dtick=1,
            showgrid=True,
            gridcolor=minor_grid_color,
            gridwidth=0.5,
        ),
        showline=True,
        linewidth=2,
        linecolor="black",
        mirror=True,
        row=1, col=1
    )
    
    # Update Dst y-axis (bottom subplot)
    fig.update_yaxes(
        title_text="Dst Index (nT)",
        range=[-500, 200],
        showgrid=True,
        gridcolor=major_grid_color,
        gridwidth=1,
        dtick=100,
        minor=dict(
            tickmode="linear",
            tick0=-500,
            dtick=50,
            showgrid=True,
            gridcolor=minor_grid_color,
            gridwidth=0.5,
        ),
        showline=True,
        linewidth=2,
        linecolor="black",
        mirror=True,
        row=2, col=1
    )
    
    # Update x-axis (only bottom subplot shows labels)
    start_date = datetime(2024, 5, 9)
    tick_locations = np.arange(0, 4 * 24 + 1, 12)
    xtick_labels = [(start_date + timedelta(hours=int(h))).strftime('%m/%d<br>%H:%M UT') for h in tick_locations]
    
    fig.update_xaxes(
        title_text="",
        tickmode="array",
        tickvals=tick_locations,
        ticktext=xtick_labels,
        range=[-1, 24 * 4 + 1],
        showgrid=True,
        gridcolor=major_grid_color,
        gridwidth=1,
        minor=dict(
            tickmode="linear",
            tick0=0,
            dtick=6,
            showgrid=True,
            gridcolor=minor_grid_color,
            gridwidth=0.5,
        ),
        showline=True,
        linewidth=2,
        linecolor="black",
        mirror=True,
        row=2, col=1
    )
    
    # Hide x-axis labels on top subplot but show grid
    fig.update_xaxes(
        showticklabels=False,
        range=[-1, 24 * 4 + 1],
        showgrid=True,
        gridcolor=major_grid_color,
        gridwidth=1,
        minor=dict(
            tickmode="linear",
            tick0=0,
            dtick=6,
            showgrid=True,
            gridcolor=minor_grid_color,
            gridwidth=0.5,
        ),
        showline=True,
        linewidth=2,
        linecolor="black",
        mirror=True,
        row=1, col=1
    )
    
    return fig

# ----------------------------
# Figure cache wrappers + warmup
# ----------------------------
import threading
 
def _models_key(models):
    if models is None:
        return ()
    # keep order stable while allowing tuple hashing
    return tuple(models)
 
def _cache_get_or_build(key, builder):
    if key in FIG_CACHE:
        return FIG_CACHE[key]
    fig = builder()
    FIG_CACHE[key] = fig
    return fig
 
def get_tec_utlat_figure(model_names=None, date_range_str="2024/05/09-05/12"):
    key = ("tec_utlat", date_range_str, _models_key(model_names))
    return _cache_get_or_build(key, lambda: tec_utlat_figure(date_range_str=date_range_str, model_names=model_names))
 
def get_tec_rmse_utlat_figure(model_names=None, date_range_str="2024/05/09-05/12"):
    key = ("tec_rmse_utlat", date_range_str, _models_key(model_names))
    return _cache_get_or_build(key, lambda: tec_rmse_utlat_figure(date_range_str=date_range_str, model_names=model_names))
 
def get_gnss_error_utlat_figure(kind="3D", model_names=None, date_range_str="2024/05/09-05/12"):
    key = ("gnss_error_utlat", kind.upper(), date_range_str, _models_key(model_names))
    return _cache_get_or_build(key, lambda: gnss_error_utlat_figure(kind=kind, date_range_str=date_range_str, model_names=model_names))
 
def get_tec_rmse_metric_scatter():
    key = ("tec_rmse_metric_scatter",)
    return _cache_get_or_build(key, lambda: tec_rmse_metric_scatter())
 
def get_ppp3d_metric_scatter():
    key = ("ppp3d_metric_scatter",)
    return _cache_get_or_build(key, lambda: ppp3d_metric_scatter())

# New cache wrappers for updated graphs
def get_tec_gradient_utlat_figure(model_names=None, date_range_str="2024/05/09-05/12"):
    key = ("tec_gradient_utlat", date_range_str, _models_key(model_names))
    return _cache_get_or_build(key, lambda: tec_gradient_utlat_figure(date_range_str=date_range_str, model_names=model_names))

def get_tec_gradient_rmse_utlat_figure(model_names=None, date_range_str="2024/05/09-05/12"):
    key = ("tec_gradient_rmse_utlat", date_range_str, _models_key(model_names))
    return _cache_get_or_build(key, lambda: tec_gradient_rmse_utlat_figure(date_range_str=date_range_str, model_names=model_names))

def get_relative_tec_change_figure(model_names=None, date_range_str="2024/05/10-05/12"):
    key = ("relative_tec_change", date_range_str, _models_key(model_names))
    return _cache_get_or_build(key, lambda: relative_tec_change_figure(date_range_str=date_range_str, model_names=model_names))

def get_tec_rmse_metric_bars():
    key = ("tec_rmse_metric_bars",)
    return _cache_get_or_build(key, lambda: tec_rmse_metric_bars())

def get_tec_tss_metric_bars():
    key = ("tec_tss_metric_bars",)
    return _cache_get_or_build(key, lambda: tec_tss_metric_bars())

def get_ssim_metric_bars():
    key = ("ssim_metric_bars",)
    return _cache_get_or_build(key, lambda: ssim_metric_bars())

def get_positioning_rmse_metric_bars(error_type="3D"):
    key = ("positioning_rmse_metric_bars", error_type.upper())
    return _cache_get_or_build(key, lambda: positioning_rmse_metric_bars(error_type=error_type))
 
def warm_caches():
    """
    Precompute a few hot combinations so first loads are fast.
    Non-blocking call recommended via start_warm_cache_thread().
    """
    try:
        # Show-all variants (model_names=None uses full grids)
        get_tec_utlat_figure(model_names=None)
        get_tec_rmse_utlat_figure(model_names=None)
        get_gnss_error_utlat_figure(kind="3D", model_names=None)
        get_gnss_error_utlat_figure(kind="2D", model_names=None)
        get_gnss_error_utlat_figure(kind="U", model_names=None)
        # New graph types
        get_tec_gradient_utlat_figure(model_names=None)
        get_tec_gradient_rmse_utlat_figure(model_names=None)
        get_relative_tec_change_figure(model_names=None)
        # Metric bar charts
        get_tec_rmse_metric_bars()
        get_tec_tss_metric_bars()
        get_ssim_metric_bars()
        get_positioning_rmse_metric_bars(error_type="3D")
        get_positioning_rmse_metric_bars(error_type="2D")
        get_positioning_rmse_metric_bars(error_type="U")
    except Exception:
        # Swallow warmup errors to avoid impacting app startup
        pass
 
def start_warm_cache_thread():
    t = threading.Thread(target=warm_caches, daemon=True)
    t.start()

