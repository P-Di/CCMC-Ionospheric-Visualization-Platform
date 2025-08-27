import dash_bootstrap_components as dbc
from dash import html
import dash_core_components as dcc

description_page2 = html.Div(style={'marginTop': '30px'},
    children=[
        html.Div(
            [
                html.Div(html.H5("Table of Contents")),
                html.Ul(
                    [
                        html.Li(html.A("Introduction", href="#about", className="TOC-link")),
                        html.Li(html.A("Model Description", href="#model", className="TOC-link")),

                        html.Li(html.A("References", href="#references", className="TOC-link"))
                    ],
                    style={"list-style-type": "none"}
                )
            ],
            className="TOC"
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div([

                            html.Br(),
                            html.Br()
                        ]),
                    ],
                    id="about"
                ),
                html.Div(
                    [
                        html.H1("Introduction: Ionospheric Model Validation"),
                        html.P(
                            """
                        NASA Goddard Space Flight Center Community Coordinated Modeling Center (CCMC) is a multi-agency partnership dedicated to supporting the development, evaluation and dissemination of advanced space science and space weather models. CCMC provides the broader space weather and aeronomy community with access to a suite of state-of-the-art models developed by research institutions and operational agencies around the world. These models are made available through runs-on-request and instant run to facilitate research and improve understanding of space weather impacts on technological systems. 
                            """
                        ),
                        
                        html.P(
                            """
                        A key part of model development at CCMC is the systematic and quantitative evaluation of space weather models. The model validation process is essential not only to verify model accuracy but also to identify missing physical processes, ultimately enhancing model capability for real-time space weather forecasting. CCMC acts as an unbiased evaluator to provide a mechanism by which research and/or operational models can be validated, tested, and improved for eventual use in space weather forecasting. 
                            """
                        ),
                        html.P([
                        "Recently, CCMC has initiated the historic storm event model validation campaign, which assess the performance of ionospheric models during geomagnetic storms across solar cycles 23 to 25 (",
                        html.A("https://kauai.ccmc.gsfc.nasa.gov/CMR/TimeInterval/viewAllTI", href="https://kauai.ccmc.gsfc.nasa.gov/CMR/TimeInterval/viewAllTI", target="_blank"),
                        "To support community engagement and open science, CCMC has developed the ",
                        html.Strong("Ionosphere- Thermosphere Model Assessment and validation Platform (ITMAP). ITMAP"),
                        " is an interactive tool designed to visualize the ionospheric model validation results for the historic storm events, enabling users to explore the model validation outcomes. The current ITMAP ionospheric validation projects focus on key ionospheric parameters including critical for navigation and communication systems:"
                        ]),
                        html.P(
                        html.Strong("•	Total Electron Content (TEC)"),
                        ),
                        html.P(
                        html.Strong("•	Critical frequency of the F2 layer (foF2)"),
                        ),
                        html.P(
                        html.Strong("•	Peak height of the F2 layer (hmF2)"),
                        ),
                        html.P([
                        
                        "These parameters are vital to understanding ionospheric behavior and its influence on satellite-based systems, including GPS and high-frequency radio communications. To evaluate ionospheric model performance during geomagnetic storm conditions, the storm phases, quiet phase, main phase and recovery phase, are defined based on the Dst and Kp indices as shown in Figure 1. These geomagnetic indices serve as proxies for storm intensity and timing, allowing for a consistent segmentation of the storm period. Model outputs are then validated against observations separately for each phase to assess how well the models capture ionospheric responses throughout the storm’s evolution.",
                        html.Strong(" Note that due to the complexity of geomagnetic storm dynamics, only storm events characterized by a single Dst index trough are selected for validation. This criterion ensures a clearer definition of storm phases and avoids ambiguity in the timing of the main and recovery phases."),
                        ]),
                        html.Div([
                        html.Img(className="description-fig", src="assets/DST_KP.png", style={'width': '600px', 'height': 'auto', 'display': 'block', 'margin': '0 auto'}, alt="Figure 2."),
                
                        html.P("Figure 1. Dst and Kp for the 2021 November storm events.", style={'textAlign': 'center', 'marginTop': '10px'}),
                        ]),
                        html.H1("Model Validation Projects"),
                        html.H3("•	TEC validation using the ground-based GNSS TEC"),
                        
                        html.Img(className="description-fig", src="assets/GNSSTEC.png", style={'width': '600px', 'height': 'auto', 'display': 'block', 'margin': '0 auto'}, alt="Figure 2."),
                
                        html.P("Figure 2. Ground-based GNSS TEC ", style={'textAlign': 'center', 'marginTop': '10px'}),
                        
                        html.P(
                            """       
                        Global ground-based GNSS networks consist of thousands of continuously operating stations maintained by various organizations for applications including geodesy, navigation, tectonics, ionospheric research, and precise positioning. These dense GNSS networks offer continuous, high-resolution two-dimensional TEC observations (Figure 2). Ionospheric models hosted by CCMC and other institutions are validated by leveraging the dense GNSS networks, providing a comprehensive model validation on a global scale and deeper insights into model performance.

                            """
                        ),
                        html.P([
                        
                        "In this project, we validate ionospheric models using ",
                        html.Strong("ground-based GNSS TEC observations "),
                         "from two major sources: the ",
                        html.Strong("Massachusetts Institute of Technology Haystack Observatory (Madrigal TEC) and Nagoya University (Nagoya TEC)"),
                        " The Madrigal TEC has a spatial and temporal resolutions of 1° × 1° × 5 min, while Nagoya TEC provides data at 0.5° × 0.5° × 10 min resolution. Due to the discrepancy of spatial resolution and cadence between the model outputs and TEC observations, the model-derived TEC maps are interpolated into 1° × 1° × 1 hr. Only the grid points where TEC observations are available on an hourly basis are used in the validation. Note that this project specifically focuses on the equatorial ionization anomaly (EIA) region; only the TEC observations within ±40° magnetic latitudes are used for validation. ",
                        ]),
                        html.H3("•	foF2 and hmF2 validation using the GNSS Radio Occultation observations"),
                        html.P([
                        
                        "In this project,  ",
                        html.Strong("electron density profiles from the FORMOSAT-7/COSMIC-2 (F7/C2) "),
                         " radio occultation (RO) mission are used to validate ionospheric models. The inclusion of F7/C2 satellite observations helps  ",
                        html.Strong("overcome the spatial limitations "),
                        " of ground-based GNSS and ionosonde networks, particularly over oceanic and data-sparse regions. This enables a ",
                        html.Strong("more comprehensive assessment "),
                        " of model performance on a global scale. Rather than directly comparing the RO-derived foF2 and hmF2 with model outputs, we employ an Observing System Simulation Experiment (OSSE) approach, as illustrated in Figure3, to enhance the robustness of the validation.",
                        ]),
                        html.Div([
                        html.Img(className="description-fig", src="assets/FLOW.png", style={'width': '600px', 'height': 'auto', 'display': 'block', 'margin': '0 auto'}, alt="Figure 2."),
                
                        html.P("Figure 3. Flowchart of F7/C2 OSSE.", style={'textAlign': 'center', 'marginTop': '10px'}),
                        ]),

                        html.P(
                            """
                        The OSSE process consists of the following steps:
                            """
                        ),
                        dcc.Markdown("1.	The realistic line-of-sight geometries between F7/C2 and GNSS satellites are inserted into the ionospheric models to derive the synthetic RO TEC $(TEC_{AC})$. ", mathjax=True),
                        dcc.Markdown("2.	Calculate the calibrated TEC (occultation side TEC subtracts non-occultation side TEC,  calTEC = $(TEC_{AC} – TEC_{BC})$", mathjax=True),
                        dcc.Markdown("3.	The Abel inversion is applied to convert the calTEC into synthetic RO electron density profile "),
                        dcc.Markdown("4.	Derive the NmF2 and hmF2 from the synthetic electron density profile"),    
                        dcc.Markdown("5.	Convert NmF2 to foF2 using the relation: $NmF2 = (1/80.6)·(foF2)^2$", mathjax=True),           
                        dcc.Markdown("6.	Finally, the model-derived RO foF2 and hmF2 are compared with F7/C2 observations"),                          
                        html.P("This OSSE method allows us to simulate the F7/C2 observational process within the models, reducing the impact of potential systematic errors in the observed RO electron density profiles. It provides a more consistent and fair comparison between model outputs and satellite observations."),
                        html.H1("Metrics and Skill Score"),
                        html.H3("•	Model-data comparison metrics"),
                        html.P([
                        
                        "To assess and quantify the ionospheric model performance, four categories of metrics, including",
                        html.Strong(" accuracy, bias, association, "),
                         "and ",
                        html.Strong("precision "),
                        ", are utilized to address specific aspects of the model-data relationship (Liemohn et al., 2021).",
                        html.Strong(" Accuracy "),
                        "metric uses Root Mean Square Error to quantify the difference and quality of the model-data comparison:",
                        ]),
                        dcc.Markdown("$RMSE = \\sqrt{\\frac{1}{N}\\sum_{i=1}^N(M_i-O_i)^2}$", mathjax=True),
                        html.P("Where M and O denote the model and observational values."),
                        html.P([
                        html.Strong("Bias "),
                         "uses mean error to indicate systematic underestimation or overestimation of model values:",
                        ]),
                        dcc.Markdown("$ME = \\overline{M} - \\overline{O}$",mathjax=True),
                        html.P("A negative ME indicates a systematic underestimation of the model values, while a positive ME indicates a systematic overestimation of the model values."),
                        html.P([
                        html.Strong("Association "),
                         "is denoted by the Pearson linear correlation coefficient (R):",
                        ]),
                        dcc.Markdown("$R = \\frac{\\sum_{i}^{N} (O_i - \\overline{O})(M_i - \\overline{M})}{\\sqrt{\\sum_{i}^{N} (O_i - \\overline{O})^2 \\; \\sum_{i}^{N} (M_i - \\overline{M})^2}}$", mathjax=True),
                        html.P("This measures the strength of the linear relationship between the model and observation. "),
                        html.P("A negative ME indicates a systematic underestimation of the model values, while a positive ME indicates a systematic overestimation of the model values."),
                        html.P([html.Strong("Precision "),
                         "is given by the difference in standard deviations between the model and observations:",
                        ]),
                        dcc.Markdown("$P_{σ, diff} = σ_{M}-σ_{O}$", mathjax=True),
                        dcc.Markdown("$P_{σ, diff}$ with value above or below zero indicates that the model over or under predict the spread of the data.", mathjax=True),

                        html.P([
                        "The ",
                        html.Strong("skill score "),
                         "(SS) can be calculated based on the metric scores above.",
                        ]),
                        dcc.Markdown("It is defined as: $SS=\\frac{Metric\_new-Metric\_ref}{Metric\_perfect-Metric\_ref}$", mathjax=True),
                        
                        html.P([
                        html.Strong("Metric_ref: "),
                         "metric values of a reference model, which can be any model. Here IRI-2016 is set as a reference model. "
                        ]),
                        html.P([
                        html.Strong("Metric_new: "),
                         "metric values of a new model.",
                        ]),
                        html.P([
                        html.Strong("Metric_perfect: "),
                         "the best metric value for data-model comparison.",
                        ]),
                        html.P("The SS is, therefore, equal to one if the new model is perfect. If SS=0, this indicates that the performance of the new model is the same as the reference model.  A negative SS denotes a worse skill than the reference model."),
                        dcc.Markdown("The skill score can then be normalized $nSS = \\frac{SS-SS_{min}}{SS_{max}-SS_{min}}$ for calculating the total normalized skill scores (∑nSS). ", mathjax=True),
                        dcc.Markdown("$SS_{max}$ and $SS_{min}$ denote the maximum and minimum SS among the models. The maximum and minimum of total nSS are equal to four (four metrics) and zero.", mathjax=True),
                        dcc.Markdown("Figure 4 shows an example of normalized skill score (nSS) for each model to compare the performance of ionospheric models against IRI-2016 during the quiet phase of a geomagnetic storm. The nSS are calculated across four categories of metrics (RMSE, $P_{σ, diff}, R, ME). In the nSS_RMSE category, GloTEC achieves the highest score (nSS=1), indicating it has the best performance in terms of accuracy.  In contrast, CTIPe has an nSS of 0, representing the lowest performance model in this category.", mathjax=True),
                        html.Img(className="description-fig", src="assets/nSSGRAPH.png", style={'width': '600px', 'height': 'auto', 'display': 'block', 'margin': '0 auto'}, alt="Figure 2."),
                        dcc.Markdown("Figure 4. The normalized skill score of RMSE, $P_{σ, diff}$, R, and ME for each model during the quiet phase of the 2013 geomagnetic storm.", mathjax=True, style={'textAlign': 'center', 'marginTop': '10px'}),
                        html.Img(className="description-fig", src="assets/tnSSGRAPH.png", style={'width': '600px', 'height': 'auto', 'display': 'block', 'margin': '0 auto'}, alt="Figure 2."),
                        html.P("Figure 5. The summation of normalized skill score for each model.", style={'textAlign': 'center', 'marginTop': '10px'}),

                        html.P("Figure 5 shows total normalized skill scores ∑nSS for each model, which is the summation of normalized skill scores from the accuracy, precision, association, and bias categories. Note that the normalized skill scores are calculated independently during the three phases. The total normalized skill scores reveal the performance of ionospheric models based on all used fit performance metrics."),
                        html.H3("•	Ionospheric storm anomaly metrics"),
                        html.P([
                            "While the previously discussed metrics primarily assess the absolute differences between model outputs and observations, they do not adequately evaluate a model’s ability to capture storm-induced ionospheric anomalies. To address this, we introduce a metric based on the ",
                            html.Strong("relative TEC change (TC) between quiet and storm periods: "),
                        ]),
                        dcc.Markdown(
                                                '''
                                                $$
                                                TC = \\frac{TEC_{storm} - TEC_{quiet}}{TEC_{quiet}}
                                                $$
                                                ''',
                                                mathjax=True
                                            ),
                        dcc.Markdown("$TEC_{quiet}$ is the period before the storm, and $TEC_{storm}$ is the period during the main and recovery phases of the storm. The quantities of TC reveal the ionospheric responses to the geomagnetic storms.", mathjax=True),
                     
                        html.P([
                            "To quantify model performance in capturing these storm-driven TEC enhancements and depletions, we adopt two metrics based on prior work (e.g., Shim et al., 2012; 2018). The first metric evaluates the model's ability to reproduce the distribution of storm-time TEC changes and is defined as the is ",
                            html.Strong("the ratio of TC difference between the 80th and 20th percentiles:")
                            ]),
                        dcc.Markdown(
                                                '''
                                                $$
                                                (ratio(80th - 20th) = \\frac{(TC_{M})_{80\\text{th}} - (TC_{M})_{20\\text{th}}}{(TC_{O})_{80\\text{th}} - (TC_{O})_{20\\text{th}}})
                                                $$
                                                ''',
                                                mathjax=True
                                            ),
                        html.P("Where:"),
                        dcc.Markdown("•	$(TC_{M})_{80\\text{th}}\\text{ and }  (TC_{O})_{80\\text{th}}$ are the 80th percentile TC values from the model and observation, respectively.", mathjax=True),
                        dcc.Markdown("•	$(TC_{M})_{20\\text{th}}\\text{ and }(TC_{O})_{20\\text{th}}$ are the corresponding 20th percentile TC values.", mathjax=True),
                        html.P("Using the 80th and 20th percentiles helps reduce the influence of outliers in observational data. A ratio close to 1 suggests the model accurately captures the TEC changes observed during geomagnetic storms."),
                        dcc.Markdown(
                                                'Figure 6 shows an example of the ratio of TC difference between the 80th and 20th percentiles (line plot) and the TC difference from the 80th to 20th percentiles $((TC)_{80\\text{th}}-(TC)_{20\\text{th}}$ during the main (blue line) and recovery (orange line) phases of the storm. If the ratio is 1, this indicates that model shows similar TEC change compared to observations.',
                                                mathjax=True
                                            ),
                        html.Img(className="description-fig", src="assets/chr.png", style={'width': '600px', 'height': 'auto', 'display': 'block', 'margin': '0 auto'}, alt="Figure 2."),
                        
                        dcc.Markdown(
                                                'Figure 6. The line plot and histogram denote the ratio of the TC difference from the 80th to 20th percentiles between models and observation $(ratio(80th - 20th) = \\frac{(TC_{M})_{80\\text{th}} - (TC_{M})_{20\\text{th}}}{(TC_{O})_{80\\text{th}} - (TC_{O})_{20\\text{th}}})$ and the TC difference from the 80th to 20th percentiles $((TC)_{80\\text{th}}-(TC)_{20\\text{th}}$.',
                                                mathjax=True, style={'textAlign': 'center', 'marginTop': '10px'}
                                            ),
                        html.P([
                            "The second metric is the ratio of model and observation TC at the 80th percentile, referred to as ",
                            html.Strong("Yield. "),
                            "It is defined as:"
                        ]),
                        dcc.Markdown(
                                                '''
                                                $$
                                                \\operatorname{ratio}(80\\text{th percentile}) = \\frac{(TC_{M})_{80\\text{th}}}{(TC_{O})_{80\\text{th}}}
                                                $$
                                                ''',
                                                mathjax=True
                                            ),
                        html.P("This metric is designed to assess the model's ability to reproduce enhanced TEC levels typically observed during geomagnetic storms. Since storm-time ionospheric responses often result in significant TEC increases, a ratio close to 1 indicates that the model effectively captures these high-end TEC enhancements. Figure 7 shows an example of the ratio at 80th percentile (line plot) and the TC at 80th percentile (histogram) during the main (blue) and recovery (orange) phases of the storm."),
                        html.Img(className="description-fig", src="assets/chr.png", style={'width': '600px', 'height': 'auto', 'display': 'block', 'margin': '0 auto'}, alt="Figure 2."),
                        html.P("Figure 7. The line plot and histogram denote the ratio of TC at the 80th percentile and TC at the 80th percentile for each model.", style={'textAlign': 'center', 'marginTop': '10px'}),
                        html.P([
                            "Finally, the ",
                            html.Strong("correlation coefficient "),
                            "between the observed and modeled relative ",
                            html.Strong("relative TEC changes (TC) "),
                            "is also computed to assess how well the models capture the ",
                            html.Strong("temporal variability and spatial patterns "),
                            "of storm-time ionospheric responses (Figure 8)."
                        ]),
                        html.Img(className="description-fig", src="assets/CC.png", style={'width': '600px', 'height': 'auto', 'display': 'block', 'margin': '0 auto'}, alt="Figure 2."),
                        html.P("Figure 8. The correlation coefficients of TC between model and observations during the main and recovery phases.", style={'textAlign': 'center', 'marginTop': '10px'}),                        

                   ],
                    id="introduction"
                ),


                html.Div(
                    [
                        html.H1("List of Models Used"),
                        html.H3("•	Empirical Models:"),
                        html.P([
                            html.Strong("IRI-2016 "),
                            "(International Reference Ionosphere) is a project sponsored by the committee on Space Research and International Union of Radio Science. Data is gathered from Ionosondes, ISIS topside sounders, Alouette topside sounders, incoherent scatter radars, and in-situ measurements from satellites and rockets. (Bilitza et al., 2017)"
                        ]),
                        html.P([
                            html.Strong("IRI-2020 "),
                            "builds on the 2016 version by including more satellite measurements and equatorial vertical ion drift models. (Bilitza et al., 2022)"
                        ]),
                        html.P([
                            html.Strong("JPL GIM "),
                            "(NASA Jet Propulsion Laboratory Global Ionospheric Map) creates TEC maps using ground based GNSS TEC measurements and climatological models, with a Kalman filter for smoothing in time. (No reference yet)"
                        ]),
                        html.H1("•	Data Assimilation Models:"),
                        html.P([
                            html.Strong("GloTEC "),
                            "(National Oceanic and Atmospheric Administration Space Weather Prediction Center Global TEC) is an empirically based data assimilation model used to estimate three-dimensional ionospheric electron density. This version uses a Gauss-Markov Kalman filter and IRI-2016 as ionospheric models, which are assimilated with ground based GNSS TEC. "
                        ]),
                        html.P([
                            html.Strong("WAM-IPE "),
                            "(Whole Atmosphere Model-Ionosphere Plasmasphere Electrodynamics) physics based whole atmosphere data assimilation model that uses solar, geomagnetic, and lower atmospheric forcing to specify ionosphere and thermosphere conditions. (Fang et al., 2022)"
                        ]),
                        html.P([
                            html.Strong("GIS-NCKU "),
                            "(Global Ionospheric Specification-National Cheng Kung University) is a data assimilation model that uses a Gauss-Markov Kalman filter on the IRI model to fit ground based and space-based slant TEC observations. (Lin et al., 2015)"
                        ]),
                        html.H1("•	Physics Based Models:"),
                        html.P([
                            html.Strong("SAMI3 "),
                            "has three versions. The first is SAMI3 v3.22, which uses neutral compositions, temperatures, neutral winds, and high latitude electric fields from empirical models NRLMSIS2.0, Horizontal Wind Model 14, and Weimer model. The second is SAMI3-Rice Convection Model (RCM), which simulates the ionosphere-plasmasphere ring current response to geomagnetic storms. The RCM provides high-latitude field-aligned currents, which can generate penetration electric fields to the low- to mid-latitude ionosphere. The Third version is SAMI3-TIEGCM, which is largely the same as SAMI3 v3.22 but the neutral compositions, temperatures, and neutral winds are determined by TIEGCM instead of NRLMSIS2.0 and Horizontal Wind Model 14. (Huba et al., 2020)"
                        ]),
                        html.P([
                            html.Strong("CTIPe "),
                            "(Coupled Thermosphere Ionosphere Plasmasphere Electrodynamics) model nonlinear, coupled thermosphere-ionosphere-plasmasphere electrodynamic model that consists of four components: a global thermosphere, a high-latitude ionosphere, a mid- and low-latitude ionosphere/plasmasphere, and an electrodynamical calculation of the global dynamo electric field.  (Codrescu et al., 2012)"
                        ]),
                        html.P([
                            html.Strong("GITM "),
                            "(Global Ionosphere Thermosphere Model) is a three-dimensional spherical code that models the Earth’s thermosphere and ionosphere. Solar wind data and IRI are used to set the initial state. (Ridley et al., 2006)"
                        ]),
                        html.P([
                            html.Strong("TIEGCM "),
                            "v2.0 comprehensive, first principles, three-dimensional, non-linear representation of the coupled thermosphere and ionosphere system that includes a self-consistent solution of the low-latitude electric field. TIEGCM parameterizes energetic particle precipitation in the high latitude and polar region. The polar region energy inputs associated with electric potential and auroral particle precipitation are prescribed either by empirical Weimer or Heelis. (Richmond et al., 1992)"
                        ]),
                        html.P([
                            html.Strong("WACCM-X "),
                            " is a specific configuration of the NCAR Community Earth System Model that extends the atmospheric component into the thermosphere from 500 to 700 km. It calculates three dimensional ionospheric structures, incorporating all the features from the NCAR Whole Atmosphere Community. "
                        ]),
                        html.P([
                            html.Strong("PBMOD "),
                            " is a system of Physics Based MODels that described the three-dimensional time-dependent evolution of low-latitude ionosphere on different spatial scales. (Retterer et al., 2005)"
                        ]),
                    ],
                    id="model"
                ),
                html.Div(
                    [
                        html.H1("References"),
                        html.P([
                            """
                            Chou, M.-Y., Yue, J., Wang, J., Huba, J. D., El Alaoui, M., Kuznetsova, M. M., et al. (2023). Validation of ionospheric modeled TEC in the equatorial ionosphere during the 2013 March and 2021 November geomagnetic storms. Space Weather, 21, e2023SW003480.  
                            """,
                            html.A("https://doi.org/10.1029/2023SW003480.", href="https://doi.org/10.1029/2023SW003480", target="_blank")
                        ]),
                        html.P([
                            """
                            Bilitza, D., D. Altadill, V. Truhlik, V. Shubin, I. Galkin, B. Reinisch, and X. Huang (2017), International Reference Ionosphere 2016: From ionospheric climate to real-time weather predictions. Space Weather, 15, 418–429. 
                            """,
                            html.A("https://doi.org/10.1002/2016SW001593 ..", href="https://doi.org/10.1002/2016SW001593 .", target="_blank")
                        ]),
                        html.P([
                            """
                            Bilitza, D., Pezzopane, M., Truhlik, V., Altadill, D., Reinisch, B. W., & Pignalberi, A. (2022). The International Reference Ionosphere model: A review and description of an ionospheric benchmark. Reviews of Geophysics, 60, e2022RG000792.  
                            """,
                            html.A("https://doi.org/10.1029/2022RG000792.", href="https://doi.org/10.1029/2022RG000792", target="_blank")
                        ]),
                        html.P([
                            """
                            Hurrell, J. W., Holland, M. M., Gent, P. R., Ghan, S., Kay, J. E., Kushner, P. J., et al. (2013). The community Earth system model: A framework for collaborative research. Bulletin of the American Meteorological Society, 94(9), 1339–1360. 
                            """,
                            html.A("https://doi.org/10.1175/BAMS-D-12-00121.1.", href="https://doi.org/10.1175/BAMS-D-12-00121.1", target="_blank")
                        ]),
                        
                        html.P([
                            """
                            Hurrell, J. W., Holland, M. M., Gent, P. R., Ghan, S., Kay, J. E., Kushner, P. J., et al. (2013). The community Earth system model: A framework for collaborative research. Bulletin of the American Meteorological Society, 94(9), 1339–1360. 
                            """,
                            html.A("https://doi.org/10.1175/BAMS-D-12-00121.1.", href="https://doi.org/10.1175/BAMS-D-12-00121.1", target="_blank")
                        ]),
                        html.P([
                            """
                            Fang, T.-W., Kubaryk, A., Goldstein, D., Li, Z., Fuller-Rowell, T., Millward, G., et al. (2022). Space weather environment during the SpaceX Starlink satellite loss in February 2022. Space Weather, 20(11), e2022SW003193.
                            """,
                            html.A("https://doi.org/10.1029/2022SW003193.", href="https://doi.org/10.1029/2022SW003193", target="_blank")
                        ]),
                        html.P([
                            """
                            Huba, J. D., & Liu, H.-L. (2020). Global modeling of equatorial spread F with SAMI3/WACCM-X. Geophysical Research Letters, 47(14), e2020GL088258. 
                            """,
                            html.A("https://doi.org/10.1029/2020GL088258.", href="https://doi.org/10.1029/2020GL088258", target="_blank")
                        ]),
                        html.P([
                            """
                            Richmond, A. D., Ridley, E. C., & Roble, R. G. (1992). A thermosphere/ionosphere general circulation model with coupled electrodynamics. Geophysical Research Letters, 19(6), 601–604.
                            """,
                            html.A("https://doi.org/10.1029/92gl00401.", href="https://doi.org/10.1029/92gl00401", target="_blank")
                        ]),
                        html.P([
                            """
                            Codrescu, M. V., Negrea, C., Fedrizzi, M., Fuller-Rowell, T. J., Dobin, A., Jakowsky, N., et al. (2012). A real-time run of the coupled thermosphere ionosphere plasmasphere electrodynamics (CTIPe) model. Space Weather, 10(2), S02001. 
                            """,
                            html.A("https://doi.org/10.1029/2011SW000736.", href="https://doi.org/10.1029/2011SW000736", target="_blank")
                        ]),
                        html.P([
                            """
                            Ridley, A. J., Deng, Y., & Tóth, G. (2006). The global ionosphere-thermosphere model. Journal of Atmospheric and Solar-Terrestrial Physics, 68(8), 839–864.
                            """,
                            html.A("https://doi.org/10.1016/j.jastp.2006.01.008.", href="https://doi.org/10.1016/j.jastp.2006.01.008", target="_blank")
                        ]),
                        html.P([
                            """
                            Hurrell, J. W., Holland, M. M., Gent, P. R., Ghan, S., Kay, J. E., Kushner, P. J., et al. (2013). The community Earth system model: A framework for collaborative research. Bulletin of the American Meteorological Society, 94(9), 1339–1360.
                            """,
                            html.A("https://doi.org/10.1175/BAMS-D-12-00121.1.", href="https://doi.org/10.1175/BAMS-D-12-00121.1", target="_blank")
                        ]),
                        html.P([
                            """
                            Retterer, J. M. (2005). Physics-based forecasts of equatorial radio scintillation for the communication and navigation outage forecasting system (C/NOFS). Space Weather, 3(12), S12C03.
                            """,
                            html.A("https://doi.org/10.1029/2005SW000146.", href="https://doi.org/10.1029/2005SW000146", target="_blank")
                        ]),
                        html.P([
                            """
                            Lin, C. Y., Matsuo, T., Liu, J. Y., Lin, C. H., Tsai, H. F., and Araujo-Pradere, E. A.: Ionospheric assimilation of radio occultation and ground-based GPS data using non-stationary background model error covariance, Atmos. Meas. Tech., 8, 171–182, 
                            """,
                            html.A("https://doi.org/10.5194/amt-8-171-2015.", href="https://doi.org/10.5194/amt-8-171-2015", target="_blank")
                        ]),
                        html.P([
                            """
                            Liemohn, M. W., Shane, A. D., Azari, A. R., Petersen, A. K., Swiger, B. M., & Mukhopadhyay, A. (2021). RMSE is not enough: Guidelines to robust data-model comparisons for magnetospheric physics. Journal of Atmospheric and Solar-Terrestrial Physics, 218, 105624. 
                            """,
                            html.A("https://doi.org/10.1016/j.jastp.2021.105624.", href="https://doi.org/10.1016/j.jastp.2021.105624", target="_blank")
                        ]),
            
                    ],
                    id="references"
                )
            ],
            id="content"
        )   
 
    ],
    id="description-page"
)