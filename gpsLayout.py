import dash
from dash import html
import dash
from dash import dcc # Dash core componenets (dcc) for graphs and interactivity
from dash import html # Allows html manipultion within dash
import dash_bootstrap_components as dbc 
image_paths = ['assets/CCMC.png', 'assets/airflow1.jpg']
dstyles = [{'display': 'flex','overflowY': 'scroll','maxHeight': '43vh', 'overflowX': 'auto'}, 
           {'height':'200px', 'width': '320px'}, {'margin-top': '20px', 'margin-bottom': '2px'}, 
           {'height':'100%', 'width': '100%', 'min-width': '600px', 'min-height': '400px'}, {'overflowY': 'scroll', 'overflowX': 'auto'}, 
           { 'height':'40vh', 'width': '100%', 'min-width': '33vh'}, {'height':'200px', 'min-width': '320px', 'width': '100%'}, 
           {'height':'1200px', 'min-width': '600px', 'width': '100%'},
           {'overflowY': 'scroll', "maxHeight":"40vh", 'border-radius': '20px', "backgroundColor": "white", }, {"border" : "none", "margin": "0", "padding": "0", "display": "none",}]

TITLES = [["Klobuchar", "IRI2020", "IRTAM", "GloTEC", "GIS", "NEDM", "CTIPe", "SAMI3-TIEGCM", "SAMI3-HWM", "SAMI3-WACCMX", "SAMI3-MSIS-WACCMX", "TIEGCM-Weimer", "TIEGCM-Heelis", "WAMIPE", "WACCMX-Heelis", "GITM", "GITM-FTA-MSIS"]]
model_list = []


for i in TITLES:
    sub_op_list = [{'label': 'Show All', 'value' : '15'}]
    for j, k in enumerate(i):
        options_element = {'label': k, 'value': str(j)}
        sub_op_list.append(options_element)
    model_list.append(sub_op_list)
#Create styles for the graphs and rows
gps_skillscore = html.Div(children=[ html.Div([
    #html.H1("MP4 Video Example"),
    html.Video(
        controls=True,
        autoPlay=True,    
        loop=True,
        #width='1080',
        style={
            "width": "100%",
            "zIndex": "-1",
            "padding": "40px",
            "backgroundColor": "black",
            "margin": "0 auto",
            "height": "auto",  # Maintain aspect ratio
            "maxWidth": "100%"  # Prevent it from stretching beyond container
        },
        children=[
            html.Source(src="assets/movie.mp4", type="video/mp4")
        ]
    ),
html.Video(
        controls=True,
        autoPlay=True,    
        loop=True,
        #width='1080',
        style={
            "width": "100%",
            "zIndex": "-1",
            "padding": "40px",
            "backgroundColor": "black",
            "margin": "0 auto",
            "height": "auto",  # Maintain aspect ratio
            "maxWidth": "100%"  # Prevent it from stretching beyond container
        },
        children=[
            html.Source(src="assets/movie2.mp4", type="video/mp4")
        ]
    )
])
    ])

gps_analysis = html.Div(children=[ html.Div([
    #html.H1("MP4 Video Example"),
    html.Video(
        controls=True,
        autoPlay=True,    
        loop=True,
        #width='1080',
        style={
            "width": "100%",
            "zIndex": "-1",
            "padding": "40px",
            "backgroundColor": "black",
            "margin": "0 auto",
            "height": "auto",  # Maintain aspect ratio
            "maxWidth": "100%"  # Prevent it from stretching beyond container
        },
        children=[
            html.Source(src="assets/movie.mp4", type="video/mp4")
        ]
    ),
html.Video(
        controls=True,
        autoPlay=True,    
        loop=True,
        #width='1080',
        style={
            "width": "100%",
            "zIndex": "-1",
            "padding": "40px",
            "backgroundColor": "black",
            "margin": "0 auto",
            "height": "auto",  # Maintain aspect ratio
            "maxWidth": "100%"  # Prevent it from stretching beyond container
        },
        children=[
            html.Source(src="assets/movie2.mp4", type="video/mp4")
        ]
    )
])
    ])

gps_animation = html.Div(id="gps-animation-container", children=[])

gps_layout = html.Div(style={'marginTop': '30px'},
    children=[
        html.Div(
            [
                html.Div(html.H5("Table of Contents")),
                html.Ul(
                    [
                        html.Li(html.A("Introduction", href="#about", className="TOC-link")),
                        html.Li(html.A("Vertical TEC and Ionospheric Pattern Evaluation", href="#vertical-tec", className="TOC-link")),
                        html.Li(html.A("Storm-Induced TEC Anomaly Evaluation", href="#tec-anomaly", className="TOC-link")),
                        html.Li(html.A("Model Performance in Single-Frequency GNSS SPP", href="#gnss-spp", className="TOC-link")),
                        html.Li(html.A("Metrics and Skill Score", href="#metrics", className="TOC-link")),
                        html.Li(html.A("Models Included in This Study", href="#model", className="TOC-link")),
                        html.Li(html.A("References", href="#references", className="TOC-link")),
                    ],
                    style={"list-style-type": "none"}
                )
            ],
            className="gps-toc"
        ),
        html.Div(
            [
                
                html.Div(id="about", style={"scrollMarginTop": "140px"}),

                # ── Introduction ──────────────────────────────────────────────
                html.Div(
                    [
                        html.H1("Introduction: Ionospheric Model Validation"),
                        html.P(
                            "Recently, CCMC has initiated the historic storm event model validation campaign, which "
                            "assesses the performance of ionospheric models during geomagnetic storms across "
                            "solar cycles 23 to 25. As part of this campaign, this study assesses 17 ionospheric "
                            "models during the extreme G5 2024 Mother\u2019s Day geomagnetic storm. The "
                            "geomagnetic storm resulted in a significant TEC enhancement of ~125%, accompanied "
                            "by large density gradients, over the Continental United States (CONUS). These "
                            "conditions provide an important opportunity to evaluate ionospheric models under "
                            "extreme space weather forcing rather than climatological conditions. This study "
                            "validates the models against ground-based GNSS observations, emphasizing (1) "
                            "vertical TEC and ionospheric pattern accuracy, (2) the models\u2019 ability to capture the "
                            "storm-induced TEC anomaly, and (3) their practical effectiveness in single-frequency "
                            "(SF) GNSS single point positioning (SPP)."
                        ),
                        html.P(
                            "To evaluate ionospheric model performance during geomagnetic storm conditions, the "
                            "storm phases, quiet phase, main phase and recovery phase, are defined based on the "
                            "Dst and Kp indices as shown in Figure 1. These geomagnetic indices serve as proxies "
                            "for storm intensity and timing, allowing for a consistent segmentation of the storm "
                            "period. Model outputs are then validated against observations separately for each "
                            "phase to assess how well the models capture ionospheric responses throughout the "
                            "storm\u2019s evolution."
                        ),
                        html.Img(
                            className="description-fig",
                            src="assets/DSTGS.png",
                            style={'maxWidth': '600px', 'width': '100%', 'height': 'auto', 'display': 'block', 'margin': '10px auto'},
                            alt="Figure 1. The Dst and Kp index for the 2024 Mother's Day storm."
                        ),
                        html.P(
                            "Figure 1. The Dst and Kp index for the 2024 Mother\u2019s Day storm.",
                            style={'textAlign': 'center', 'fontStyle': 'italic'}
                        ),
                    ],
                    id="introduction",
                    style={"scrollMarginTop": "140px"}
                ),

                # ── Vertical TEC ──────────────────────────────────────────────
                html.Div(
                    [
                        html.H2("Vertical TEC and Ionospheric Pattern Evaluation"),
                        html.P(
                            "Model-derived vertical TEC is evaluated against GNSS-based TEC observations from "
                            "the Madrigal database over the CONUS region. TEC maps are examined over the "
                            "CONUS during the main phase of the geomagnetic storm. Notably, all versions of "
                            "SAMI3, WACCMX-Heelis and GITM exhibit apparent storm-enhanced density (SED) "
                            "features extending from mid-latitudes toward the polar region."
                        ),
                        html.P(
                            "TEC maps are shown as a function of universal time (UT) and latitude for various "
                            "models from May 9\u201312, 2024. These TEC maps are constructed by binning the TEC "
                            "data into 1 hr \u00d7 1\u00b0 (UT \u00d7 LAT) grids and calculating the average values at each grid "
                            "point."
                        ),
                        html.P(
                            "Quantitative performance evaluation of each model shows the RMSE and TSS over the "
                            "CONUS (75\u2013125W, 30\u201350N). The analysis covers the quiet, main, recovery, and "
                            "combined (main + recovery) phases. RMSE evaluates model accuracy, and TSS "
                            "assesses pattern skill by combining the TEC variability and correlation."
                        ),
                        html.Img(
                            className="description-fig",
                            src="assets/VerTEC.png",
                            style={'maxWidth': '700px', 'width': '100%', 'height': 'auto', 'display': 'block', 'margin': '10px auto'},
                            alt="Figure 2. Madrigal and model TEC maps over the CONUS at 22:00 UT on May 10, 2024."
                        ),
                        html.P(
                            "Figure 2. Madrigal and model TEC maps over the CONUS at 22:00 UT on May 10, "
                            "2024 during the main phase of the geomagnetic storm.",
                            style={'textAlign': 'center', 'fontStyle': 'italic'}
                        ),
                    ],
                    id="vertical-tec",
                    style={"scrollMarginTop": "140px"}
                ),

                # ── Storm-Induced TEC Anomaly ─────────────────────────────────
                html.Div(
                    [
                        html.H2("Storm-Induced TEC Anomaly Evaluation"),
                        html.P(
                            "To assess the models\u2019 capability in responding to the geomagnetic storm, we calculate "
                            "the relative TEC change between the quiet phase "
                            "(May 9, used as a reference) and storm phases:"
                        ),
                        html.Img(
                            className="description-fig",
                            src="assets/deltTEC.png",
                            style={'height': '35px', 'width': 'auto', 'display': 'block', 'margin': '8px auto'},
                            alt="Relative TEC change formula"
                        ),
                        html.P(
                            "Figure 3 shows an example of the "
                            "relative TEC change maps over the CONUS are presented for the Madrigal TEC "
                            "observation and all models at 22:00 UT on May 10, 2024. The Madrigal TEC "
                            "observation exhibits large density gradients over the central US, with a peak TEC "
                            "enhancement of ~125% and a simultaneous decrease of ~50% over Canada. A clear "
                            "SED structure can also be identified, extending from the mid-latitude toward the polar "
                            "region."
                        ),
                        html.P(
                            "The zonal average relative TEC change maps are shown as a function of universal time "
                            "(UT) and latitude from May 10\u201312, 2024. These maps are constructed by binning the "
                            "\u0394TC data into 1 hr \u00d7 1\u00b0 (UT \u00d7 LAT) grids."
                        ),
                        html.P(
                            "Model performance is quantitatively evaluated using pattern-based metrics. The "
                            "Structure Similarity Index Measure (SSIM) is used to evaluate the model\u2019s capability in "
                            "simulating the storm-induced TEC variation (relative TEC change). SSIM evaluates how "
                            "well the model replicates the perceived structure of observations, considering "
                            "differences in luminance, contrast, and overall pattern correlation. The Taylor Skill "
                            "Score (TSS) is also employed, combining correlation coefficient, standard deviation, "
                            "and centered root mean square difference into a single metric suitable for multiple "
                            "model comparisons."
                        ),
                        html.P(
                            "TSS confirms that the overall statistical behavior and large-scale patterns of the change "
                            "field are realistic. SSIM focuses on the morphological and structural fidelity, confirming "
                            "that the local structures are in the right places and look correct. For example, a high "
                            "TSS and low SSIM indicate that a model captures the overall magnitude of TEC "
                            "variations but fails to reproduce the structure, and vice versa."
                        ),
                        html.Img(
                            className="description-fig",
                            src="assets/RelTEC.png",
                            style={'maxWidth': '700px', 'width': '100%', 'height': 'auto', 'display': 'block', 'margin': '10px auto'},
                            alt="Figure 3. Relative TEC change maps over the CONUS at 22:00 UT on May 10, 2024."
                        ),
                        html.P(
                            "Figure 3. Relative TEC change maps over the CONUS at 22:00 UT on May 10, 2024 "
                            "during the main phase of the geomagnetic storm.",
                            style={'textAlign': 'center', 'fontStyle': 'italic'}
                        ),
                    ],
                    id="tec-anomaly",
                    style={"scrollMarginTop": "140px"}
                ),

                # ── GNSS SPP ──────────────────────────────────────────────────
                html.Div(
                    [
                        html.H2("Model Performance in Single-Frequency GNSS Single Point Positioning"),
                        html.P(
                            "To assess the practical utility of the ionospheric models in technological application, we process GNSS "
                            "SPP in kinematic mode using the GNSS Laboratory Tool Suite (gLAB) v6.0.0 (Sanz et al., 2013; Ib\u00e1\u00f1ez et "
                            "al., 2018). We utilize the GNSS code measurement (P) from SOPAC and CORS networks over the U.S. "
                            "during 9\u201312 May 2024. The use of SPP over SF precise point positioning (SF-PPP) avoids the masking of "
                            "ionospheric model errors by float ambiguity parameters or cycle slips during extreme space weather (Yang "
                            "and Morton, 2025)."
                        ),
                        html.P(
                            "The raw GNSS observation equations for the L1 P measurement can be expressed as follows:"
                        ),
                        html.P(
                            [
                                html.I("P = r + c(\u03b4t"),
                                html.Sub("r"),
                                html.I(" \u2212 \u03b4t"),
                                html.Sup("s"),
                                html.I(") + I + T + d"),
                                html.Sub("cd"),
                                html.I(" + \u03b5"),

                            ],
                            style={"textAlign": "center", "margin": "10px 0", "fontSize": "1.1em"}
                        ),
                        html.P(
                            [
                                "where r denotes the geometric distance between GNSS and receiver, \u03b4t",
                                html.Sup("s"),
                                " and \u03b4t",
                                html.Sub("r"),
                                " are the satellite and receiver clock errors, I denotes the ionospheric delay, "
                                "T denotes the troposphere delay, d",
                                html.Sub("cd"),
                                " denotes code hardware delay bias for both receiver and satellite, "
                                "and \u03b5 represents noise and multipath effects."
                            ]
                        ),
                        html.P(
                            "Our processing strategy applies a priori corrections to remove known error sources and isolate "
                            "the ionospheric component. The troposphere delay (T) is corrected using the UNB3 model (Collins and Langley, "
                            "1997). Precise satellite orbit and clock corrections from the International GNSS Service (IGS) are applied, "
                            "along with standard models for antenna phase center offsets, solid Earth tides, and relativistic effects. The "
                            "ionospheric delay (I) is corrected using slant TEC (sTEC) predictions for each evaluated model:"
                        ),
                        html.P(
                            [
                                html.I("I = 40.3 sTEC / f\u00b2"),
                            ],
                            style={"textAlign": "center", "margin": "10px 0", "fontSize": "1.1em"}
                        ),
                        html.P(
                            "where sTEC is the slant TEC along the line-of-sight and f is the signal frequency."
                        ),
                        html.P(
                            [
                                "After applying these corrections, the corrected code (P",
                                html.Sub("m"),
                                ") measurement is simplified to:"
                            ]
                        ),
                        html.P(
                            [
                                html.I("P"),
                                html.Sub(html.I("m")),
                                html.I(" = r + c\u03b4t"),
                                html.Sub("r"),
                                html.I(" + \u03b5"),
                            ],
                            style={"textAlign": "center", "margin": "10px 0", "fontSize": "1.1em"}
                        ),
                        html.P(
                            [
                                "The resulting P",
                                html.Sub("m"),
                                " is further linearized using the first-order Taylor expansion and solved epoch-by-epoch "
                                "using the Least Squares (LS) method. The state vector ",
                                html.I("x\u0302"),
                                " = [\u03b4x, \u03b4y, \u03b4z, c\u03b4t",
                                html.Sub("r"),
                                "]",
                                html.Sup("T"),
                                " is estimated as:"
                            ]
                        ),
                        html.P(
                            [
                                html.I("x\u0302 = (H"),
                                html.Sup("T"),
                                html.I("H)"),
                                html.Sup("\u22121"),
                                html.I("H"),
                                html.Sup("T"),
                                html.I("z"),
                            ],
                            style={"textAlign": "center", "margin": "10px 0", "fontSize": "1.1em"}
                        ),
                        html.P(
                            [
                                "where z is the vector of residuals and H is the Jacobian Matrix. The estimated corrections ",
                                html.I("x\u0302"),
                                " are applied iteratively to update the initial guess of receiver position and "
                                "clock offset until convergence is achieved."
                            ]
                        ),
                        html.Img(
                            className="description-fig",
                            src="assets/GNSSSPP.png",
                            style={'maxWidth': '700px', 'width': '100%', 'height': 'auto', 'display': 'block', 'margin': '10px auto'},
                            alt="Figure 4. GNSS SPP 3D positioning error maps over the CONUS at 22:00 UT on May 10, 2024."
                        ),
                        html.P(
                            "Figure 4. GNSS SPP 3D positioning error maps over the CONUS at 22:00 UT on May "
                            "10, 2024 during the main phase of the geomagnetic storm.",
                            style={'textAlign': 'center', 'fontStyle': 'italic'}
                        ),
                    ],
                    id="gnss-spp",
                    style={"scrollMarginTop": "140px"}
                ),

                # ── Metrics and Skill Score ───────────────────────────────────
                html.Div(
                    [
                        html.H2("Metrics and Skill Score"),
                        html.P(
                            "To ensure a comprehensive evaluation, several statistical metrics are applied to "
                            "quantify the model accuracy and structural fidelity, including the Root Mean Square "
                            "Error (RMSE), weighted RMSE, the Taylor Skill Score (TSS), and the Structure "
                            "Similarity Index Measure (SSIM)."
                        ),

                        html.H3("Root Mean Square Error (RMSE)"),
                        html.P(
                            "RMSE is used as an accuracy metric that quantifies the overall difference and quality of "
                            "the model-data comparison:"
                        ),
                        html.Img(
                            className="description-fig",
                            src="assets/RMSE.png",
                            style={'height': '47px', 'width': 'auto', 'display': 'block', 'margin': '8px auto'},
                            alt="RMSE formula"
                        ),
                        html.P(
                            "where M and O denote the model and observational values, respectively, and N is the "
                            "total number of observations. Lower RMSE indicates higher model accuracy. "
                            "Additionally, weighted RMSE is used to evaluate the model performance across the "
                            "entire storm phases (main + recovery phases). This aims to address the temporal "
                            "disparity between phases (i.e., the recovery phase contains more data points than the "
                            "main phase)."
                        ),

                        html.H3("Taylor Skill Score (TSS)"),
                        html.P(
                            "The TSS is commonly used in meteorology and climate science for model validation "
                            "(Taylor, 2001). It provides a statistical measure to quantify how well a model reproduces "
                            "observed patterns, combining correlation coefficient, standard deviation, and centered "
                            "root mean square difference into a single metric suitable for multiple model "
                            "comparisons. The TSS is defined as:"
                        ),
                        html.Img(
                            className="description-fig",
                            src="assets/TSS.png",
                            style={'height': '50px', 'width': 'auto', 'display': 'block', 'margin': '8px auto'},
                            alt="TSS formula"
                        ),
                        html.P(
                            "where R is the correlation coefficient, \u03c3\u2098 and \u03c3\u2092 are the standard deviations, and R\u2080 is "
                            "the maximum correlation coefficient (R\u2080 = 1). The TSS ranges from 0 to 1. A score of 1 "
                            "indicates a perfect model, while a score close to 0 indicates a poor-performing model."
                        ),

                        html.H3("Structure Similarity Index Measure (SSIM)"),
                        html.P(
                            "The SSIM is a perceptual metric initially used to evaluate the similarity between two "
                            "images (Wang et al., 2004). Here, SSIM is used to evaluate the model\u2019s capability in "
                            "simulating the storm-induced TEC variation (relative TEC change). SSIM evaluates how "
                            "well the model replicates the perceived structure of observations, considering "
                            "differences in luminance, contrast, and overall pattern correlation. The definition of "
                            "SSIM is:"
                        ),
                        html.Img(
                            className="description-fig",
                            src="assets/SSIM.png",
                            style={'height': '25px', 'width': 'auto', 'display': 'block', 'margin': '8px auto'},
                            alt="SSIM formula"
                        ),
                        html.P([
                            "where ",
                            html.I(
                            "l(obs, model) ="),
                            html.Img(src="assets/l.png", style={'height': '40px', 'width': 'auto', 'verticalAlign': 'middle', 'margin': '0 4px'}, alt="l formula"),
                            ", ",
                            html.I("c(obs, model) ="),
                            html.Img(src="assets/c.png", style={'height': '40px', 'width': 'auto', 'verticalAlign': 'middle', 'margin': '0 4px'}, alt="c formula"),
                            ", and ",
                            html.I("s(obs, model) ="),
                            html.Img(src="assets/s.png", style={'height': '40px', 'width': 'auto', 'verticalAlign': 'middle', 'margin': '0 4px'}, alt="s formula"),
                            ". ",
                            html.I(
                            "l(obs, model) "),
                             " is the luminance term that measures similarity in mean amplitudes (\u03bc); ",
                            html.I(
                            "c(obs, model) "),
                            " is the contrast term that measures similarity in standard deviation (\u03c3); ",
                            html.I(
                            "s(obs, model) "),
                            " is the structure term that uses covariance (\u03c3",
                            html.Sub("obs,model"),
                            ") to compare the similarity of spatial structures. "
                            "\u03b1, \u03b2, and \u03b3 are parameters used to adjust the relative importance of the three components, "
                            "which are set to 1. Constants c1, c2 and c3 are used to stabilize the division. "
                            "SSIM ranges from \u22121 to 1, with values closer to 1 indicating higher structural similarity "
                            "and values at or below 0 denoting no structural resemblance."
                        ]),
                    ],
                    id="metrics",
                    style={"scrollMarginTop": "140px"}
                ),

                # ── Models Included ───────────────────────────────────────────
                html.Div(
                    [
                        html.H1("Models Included in This Study"),
                        html.P(
                            "This study evaluates 17 ionospheric models representing broadcast, empirical, data "
                            "assimilation, and physics-based approaches."
                        ),

                        html.H3("Broadcast Model"),
                        html.P([
                            html.Strong("Klobuchar"),
                            " model is the standard broadcast ionospheric correction model used by "
                            "SF GPS users (Klobuchar, 1987). It is an analytical single-layer model that assumes the "
                            "ionosphere as a thin shell at 350 km, with eight parameters broadcast along with the "
                            "GPS navigation message."
                        ]),

                        html.H3("Empirical Models"),
                        html.P([
                            html.Strong("IRI-2020"),
                            " provides a climatological specification of the global ionosphere based on long-"
                            "term observational data (Bilitza et al., 2017; 2022)."
                        ]),
                        html.P([
                            html.Strong("NEDM2020"),
                            " is a 3D ionosphere model developed at the German Aerospace Center "
                            "(Hoque et al., 2022). The altitudinal range for NEDM TEC integration is 65\u201320000 km."
                        ]),

                        html.H3("Data Assimilation Models"),
                        html.P([
                            html.Strong("GloTEC"),
                            " (National Oceanic and Atmospheric Administration Space Weather Prediction "
                            "Center Global TEC) constructs global ionospheric TEC maps by assimilating ground-"
                            "based GNSS TEC and space-based radio occultation TEC observations. GloTEC "
                            "provides high-resolution TEC maps with a spatial resolution of 1\u00b0 \u00d7 1\u00b0 and a temporal "
                            "resolution of 15 minutes. The post-processed GloTEC product incorporates all available "
                            "observational data after 34 hours."
                        ]),
                        html.P([
                            html.Strong("GIS"),
                            " is designed to provide global 3D electron density structures (Lin et al., 2015; 2017; "
                            "2020). GIS assimilates slant TEC from ground-based GNSS receivers and radio "
                            "occultation TEC from FORMOSAT-7/COSMIC-2 using a Gaussian Markov Kalman "
                            "filter."
                        ]),
                        html.P([
                            html.Strong("IRTAM"),
                            " provides a real-time, global specification of the ionosphere, functioning as an "
                            "advanced data-driven version of the IRI model (Galkin et al., 2012)."
                        ]),

                        html.H3("Physics-Based Models"),
                        html.P([
                            html.Strong("SAMI3"),
                            " is a fully 3D physics-based model of the ionosphere developed by the Naval "
                            "Research Laboratory (Huba et al., 2000). Four versions are used: SAMI3-HWM (v3.22), "
                            "SAMI3-WACCMX, SAMI3-TIEGCM, and SAMI3-MSIS-WACCMX. The altitudinal range "
                            "for calculating SAMI3 TEC is 85\u20133000 km."
                        ]),
                        html.P([
                            html.Strong("CTIPe"),
                            " is a nonlinear, coupled thermosphere\u2013ionosphere\u2013plasmasphere electrodynamic "
                            "model (Codrescu et al., 2012). The altitudinal range for TEC integration is approximately "
                            "140\u20132000 km."
                        ]),
                        html.P([
                            html.Strong("GITM"),
                            " is a 3D model of the Earth\u2019s thermosphere and ionosphere (Ridley et al., 2006). "
                            "Two versions are used: GITM (v25.11.13) and GITM-FTA-MSIS."
                        ]),
                        html.P([
                            html.Strong("TIEGCM v2.0"),
                            " is a comprehensive, first-principles, three-dimensional model of the "
                            "coupled thermosphere\u2013ionosphere system (Richmond et al., 1992). The altitudinal "
                            "range for TEC integration is approximately 95\u2013750 km."
                        ]),
                        html.P([
                            html.Strong("WACCM-X"),
                            " is an extension of the NCAR Community Earth System Model into the "
                            "thermosphere. The integration range is approximately 80\u2013850 km."
                        ]),
                        html.P([
                            html.Strong("WAMIPE v1.2.5"),
                            " is operated as a free-running model as implemented in CCMC ROR "
                            "system (90\u20132000 km)."
                        ]),
                    ],
                    id="model",
                    style={"scrollMarginTop": "140px"}
                ),

                # ── References ────────────────────────────────────────────────
                html.Div(
                    [
                        html.H1("References"),
                        html.P(
                            "Bilitza, D., Altadill, D., Truhlik, V., Shubin, V., Galkin, I., Reinisch, B., & Huang, X. "
                            "(2017). International Reference Ionosphere 2016: From ionospheric climate to real-time "
                            "weather predictions. Space Weather, 15, 418\u2013429."
                        ),
                        html.P(
                            "Bilitza, D., Pezzopane, M., Truhlik, V., Altadill, D., Reinisch, B. W., & Pignalberi, A. "
                            "(2022). The International Reference Ionosphere model: A review and description of an "
                            "ionospheric benchmark. Reviews of Geophysics, 60(4), e2022RG000792."
                        ),
                        html.P(
                            "Codrescu, M. V., Fuller-Rowell, T. J., & Foster, J. C. (2012). Coupled thermosphere\u2013"
                            "ionosphere\u2013plasmasphere electrodynamics model. Space Weather."
                        ),
                        html.P(
                            "Galkin, I. A., Reinisch, B. W., Huang, X., & Bilitza, D. (2012). Assimilation of GIRO data "
                            "into a real-time IRI. Radio Science, 47, RS0L07."
                        ),
                        html.P(
                            "Hoque, M. M., Jakowski, N., & Berdermann, J. (2022). An ionosphere broadcast model "
                            "for next generation GNSS. Navigation, 69(3), navi.528."
                        ),
                        html.P(
                            "Huba, J. D., Joyce, G., & Fedder, J. A. (2000). Sami2 is Another Model of the "
                            "Ionosphere (SAMI2): A new low-latitude ionosphere model. Journal of Geophysical "
                            "Research, 105(A10), 23035\u201323053."
                        ),
                        html.P(
                            "Klobuchar, J. A. (1987). Ionospheric time-delay algorithm for single-frequency GPS "
                            "users. IEEE Transactions on Aerospace and Electronic Systems, AES-23(3), 325\u2013331."
                        ),
                        html.P(
                            "Lin, C. Y., Matsuo, T., Liu, J. Y., Lin, C. H., Tsai, H. F., & Araujo-Pradere, E. A. (2015). "
                            "Ionospheric assimilation of radio occultation and ground-based GPS data using non-"
                            "stationary background model error covariance. Atmospheric Measurement Techniques, "
                            "8, 171\u2013182."
                        ),
                        html.P(
                            "Richmond, A. D., Ridley, E. C., & Roble, R. G. (1992). A thermosphere/ionosphere "
                            "general circulation model with coupled electrodynamics. Geophysical Research Letters, "
                            "19(6), 601\u2013604."
                        ),
                        html.P(
                            "Ridley, A. J., Deng, Y., & T\u00f3th, G. (2006). The global ionosphere-thermosphere model. "
                            "Journal of Atmospheric and Solar-Terrestrial Physics, 68(8), 839\u2013864."
                        ),
                        html.P(
                            "Taylor, K. E. (2001). Summarizing multiple aspects of model performance in a single "
                            "diagram. Journal of Geophysical Research, 106(D7), 7183\u20137192."
                        ),
                        html.P(
                            "Wang, Z., Bovik, A. C., Sheikh, H. R., & Simoncelli, E. P. (2004). Image quality "
                            "assessment: From error visibility to structural similarity. IEEE Transactions on Image "
                            "Processing, 13(4), 600\u2013612."
                        ),
                    ],
                    id="references",
                    style={"scrollMarginTop": "140px"}
                ),
            ],
            className="gps-content",
            id="content"
        )
    ],
    id="gps-description-page"
)
