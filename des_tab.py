import dash_bootstrap_components as dbc
from dash import html
import dash_core_components as dcc

description_page2 = html.Div(
    [
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
                        html.H1("About"),
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
                        This project presents an interactive platform for exploring the validation results of ionospheric models currently housed at the CCMC. The lower latitude equatorial ionosphere is particularly sensitive to geomagnetic storms, and accurate modeling of its TEC is critical for satellite-based communication, navigation, and space weather forecasting. Model data was chosen from this region, ±40 degrees latitude, as it modeling ionospheric storm anomalies in this region provides a significant challenge. The models validated consist of empirical, data assimilation, and physics-based models. Observational data taken from the ground-based GNSS Total Electron Content (TEC) and FORMOSAT-7/COSMIC-2 satellites data during storms in 2013 and 2021 was used to evaluate and compare the performance of 16 ionospheric models. 
                            """
                        ),
                        
                        html.P(
                            """
                        To do this, four metrics are used: Accuracy, bias, association, and precision. Accuracy uses Root Mean Square Error to quantify the difference and quality of the model-data comparison:
                            """
                        ),
                        html.Img(className="description-fig", src="assets/RMSE.png", style={'width': '200px', 'height': 'auto'}, alt="Figure 2."),
                        html.P(
                            """
                        Bias uses mean error to indicate systematic underestimation or overestimation of model values:
                            """
                        ),
                        html.Img(className="description-fig", src="assets/ME.png", style={'width': '100px', 'height': 'auto'}, alt="Figure 2."),
                        html.P(
                            """       
                        Association is denoted by the Pearson linear correlation coefficient (R):

                            """
                        ),
                        html.Img(className="description-fig", src="assets/Pearson.png", style={'width': '200px', 'height': 'auto'}, alt="Figure 2."),

                        html.P(
                            """
                        This measures the strength of the linear relationship between the model and observation. Precision is given by the difference in standard deviations between the model and observations:
                            """
                        ),
                        html.Img(className="description-fig", src="assets/STD.png", style={'width': '200px', 'height': 'auto'}, alt="Figure 2."),
                        html.P(
                            """
                        From these metrics, the skill score can be calculated against a reference model. Any reference model can be chosen, but in this case IRI 2016 was used. A skill score of one means the new model matches the best metric value, 0 means it performed the same as the reference model, and negative means it performed worse. The skill score can then be normalized: 
                            """
                        ),
                        html.Img(className="description-fig", src="assets/nSS.png", style={'width': '200px', 'height': 'auto'}, alt="Figure 2."),
                        html.P(
                            """
                        This Normalized Skill Score has a maximum of four and a minimum of zero.
                            """
                        ),
                        html.P(
                            """
                        To assess the models’ ability to capture ionospheric storm anomaly, three other metrics are used. These metrics are based on the relative TEC change (TC) between quiet and storm time:
                            """
                        ),
                        html.Img(className="description-fig", src="assets/TC.png", style={'width': '250px', 'height': 'auto'}, alt="Figure 2."),
                        html.P(
                            """
                        From this, ratios of TC can be used to capture storm induced TC changes during the main and recovery phases. The first ratio avoids outliers by including only a certain percentile, the 80th to 20th for TEC and 95th to 5th for foF2 and hmF2. The ratio between the model and observation is then:
                            """
                        ),
                        html.Img(className="description-fig", src="assets/Rat8020.png", style={'width': '400px', 'height': 'auto'}, alt="Figure 2."),
                        html.P(
                            """
                        The second metric is similar, but includes the lower percentile in the ratio:
                            """
                        ),
                        html.Img(className="description-fig", src="assets/Rat80.png", style={'width': '250px', 'height': 'auto'}, alt="Figure 2."),
                        html.P(
                            """
                        Finally, the correlation coefficient between the model and observation TEC change is used to assess the model’s capability in capturing the special distribution of ionospheric anomaly.
                            """                        
                        ),                                                
                    ],
                    id="introduction"
                ),


                html.Div(
                    [
                        html.H1("List of Models Used"),
                        html.H3("Empirical Models:"),
                        html.P([
                            html.Strong("IRI-2016"),
                            """
                             (International Reference Ionosphere) is a project sponsored by the committee on Space Research and International Union of Radio Science. Data is gathered from Ionosondes, ISIS topside sounders, Alouette topside sounders, incoherent scatter radars, and in-situ measurements from satellites and rockets. (Bilitza et al., 2017)
                            """
                    ]),
                        html.P([
                            html.Strong("IRI-2020"),
                            """
                             builds on the 2016 version by including more satellite measurements and equatorial vertical ion drift models. (Bilitza et al., 2022)
                            """
                    ]),
                        html.P([
                            html.Strong("JPL GIM"),
                            """
                             (NASA Jet Propulsion Laboratory Global Ionospheric Map) creates TEC maps using ground based GNSS TEC measurements and climatological models, with a Kalman filter for smoothing in time. 
                            """
                    ]),
                        html.H3("Data Assimilation Models:"),
                        html.P([
                            html.Strong("GloTEC"),
                            """
                             (National Oceanic and Atmospheric Administration Space Weather Prediction Center Global TEC) is an empirically based data assimilation model used to estimate three-dimensional ionospheric electron density. This version uses a Gauss-Markov Kalman filter and IRI-2016 as ionospheric models, which are assimilated with ground based GNSS TEC. 
                            """
                    ]),
                        html.P([
                            html.Strong("WAM-IPE"),
                            """
                             (Whole Atmosphere Model-Ionosphere Plasmasphere Electrodynamics) physics based whole atmosphere data assimilation model that uses solar, geomagnetic, and lower atmospheric forcing to specify ionosphere and thermosphere conditions. (Fang et al., 2022)
                            """
                    ]),
                        html.P([
                            html.Strong("GIS-NCKU"),
                            """
                             (Global Ionospheric Specification-National Cheng Kung University) is a data assimilation model that uses a Gauss-Markov Kalman filter on the IRI model to fit ground based and space-based slant TEC observations. (Lin et al., 2015)
                            """
                    ]),
                        html.H3("Physics Based Models:"),
                        html.P([
                            html.Strong("SAMI3"),
                            """
                             has three versions. The first is SAMI3 v3.22, which uses neutral compositions, temperatures, neutral winds, and high latitude electric fields from empirical models NRLMSIS2.0, Horizontal Wind Model 14, and Weimer model. The second is SAMI3-Rice Convection Model (RCM), which simulates the ionosphere-plasmasphere ring current response to geomagnetic storms. The Third version is SAMI3-TIEGCM, which is largely the same as SAMI3 v3.22 but the neutral compositions, temperatures, and neutral winds are determined by TIEGCM instead of NRLMSIS2.0 and Horizontal Wind Model 14. (Huba et al., 2020)
                            """
                    ]),
                        html.P([
                            html.Strong("CTIPe"),
                            """
                             (Coupled Thermosphere Ionosphere Plasmasphere Electrodynamics) model nonlinear, coupled thermosphere-ionosphere-plasmasphere electrodynamic model that consists of four components: a global thermosphere, a high-latitude ionosphere, a mid- and low-latitude ionosphere/plasmasphere, and an electrodynamical calculation of the global dynamo electric field.  (Codrescu et al., 2012)
                            """
                    ]),
                        html.P([
                            html.Strong("GITM"),
                            """
                             (Global Ionosphere Thermosphere Model) is a three-dimensional spherical code that models the Earth’s thermosphere and ionosphere. Solar wind data and IRI are used to set the initial state. (Ridley et al., 2006)
                            """
                    ]),
                        html.P([
                            html.Strong("TIEGCM v2.0"),
                            """
                             v2.0 comprehensive, first principles, three-dimensional, non-linear representation of the coupled thermosphere and ionosphere system that includes a self-consistent solution of the low-latitude electric field. TIEGCM parameterizes energetic particle precipitation in the high latitude and polar region. The polar region energy inputs associated with electric potential and auroral particle precipitation are prescribed either by empirical Weimer or Heelis. (Richmond et al., 1992)
                            """
                    ]),
                        html.P([
                            html.Strong("WACCM-X"),
                            """
                             is a specific configuration of the NCAR Community Earth System Model that extends the atmospheric component into the thermosphere from 500 to 700 km. It calculates three dimensional ionospheric structures, incorporating all the features from the NCAR Whole Atmosphere Community. 
                            """
                    ]),
                        html.P([
                            html.Strong("PBMOD"),
                            """
                              is a system of Physics Based MODels that described the three-dimensional time-dependent evolution of low-latitude ionosphere on different spatial scales. (Retterer et al., 2005)
                              """
                    ]),
                    ],
                    id="model"
                ),
                html.Div(
                    [
                        html.H1("References"),
                        html.P([
                            """
                            Chou, M.-Y., Yue, J., Wang, J., Huba, J. D., El Alaoui, M., Kuznetsova, M. M., et al. (2023). Validation of ionospheric modeled TEC in the equatorial ionosphere during the 2013 March and 2021 November geomagnetic storms.
                            Space Weather, 21, e2023SW003480. 
                            """,
                            html.A("https://doi.org/10.1029/2023SW003480.", href="https://doi.org/10.1029/2023SW003480", target="_blank")
                        ]),
                        html.P([
                            """
                            Bilitza, D., D. Altadill, V. Truhlik, V. Shubin, I. Galkin, B. Reinisch, and X. Huang (2017), International Reference Ionosphere 2016: From ionospheric climate to real-time weather predictions.
                            Space Weather, 15, 418–429.
                            """,
                            html.A("doi:10.1002/2016SW001593.", href="10.1002/2016SW001593", target="_blank")
                        ]),
                        html.P([
                            """
                            Bilitza, D., Pezzopane, M., Truhlik, V., Altadill, D., Reinisch, B. W., & Pignalberi, A. (2022). The International Reference Ionosphere model: A review and description of an ionospheric benchmark. 
                            Reviews of Geophysics, 60, e2022RG000792. 
                            """,
                            html.A("https://doi.org/10.1029/2022RG000792 .", href="https://doi.org/10.1029/2022RG000792", target="_blank")
                        ]),
                        html.P([
                            """
                            Hurrell, J. W., Holland, M. M., Gent, P. R., Ghan, S., Kay, J. E., Kushner, P. J., et al. (2013). The community Earth system model: A framework for collaborative research. 
                            Bulletin of the American Meteorological Society, 94(9), 1339–1360. 
                            """,
                            html.A("https://doi.org/10.1175/BAMS-D-12-00121.1.", href="https://doi.org/10.1175/BAMS-D-12-00121.1", target="_blank")
                        ]),
                        html.P([
                            """
                            Hurrell, J. W., Holland, M. M., Gent, P. R., Ghan, S., Kay, J. E., Kushner, P. J., et al. (2013). The community Earth system model: A framework for collaborative research. 
                            Bulletin of the American Meteorological Society, 94(9), 1339–1360. 
                            """,
                            html.A("https://doi.org/10.1175/BAMS-D-12-00121.1.", href="https://doi.org/10.1175/BAMS-D-12-00121.1", target="_blank")
                        ]),
                        html.P([
                            """
                            Fang, T.-W., Kubaryk, A., Goldstein, D., Li, Z., Fuller-Rowell, T., Millward, G., et al. (2022). Space weather environment during the SpaceX Starlink satellite loss in February 2022. 
                            Space Weather, 20(11), e2022SW003193. 
                            """,
                            html.A("https://doi.org/10.1029/2022SW003193.", href="https://doi.org/10.1029/2022SW003193", target="_blank")
                        ]),
                        html.P([
                            """
                            Huba, J. D., & Liu, H.-L. (2020). Global modeling of equatorial spread F with SAMI3/WACCM-X. 
                            Geophysical Research Letters, 47(14), e2020GL088258. 
                            """,
                            html.A("https://doi.org/10.1029/2020GL088258.", href="https://doi.org/10.1029/2020GL088258", target="_blank")
                        ]),
                        html.P([
                            """
                            Richmond, A. D., Ridley, E. C., & Roble, R. G. (1992). A thermosphere/ionosphere general circulation model with coupled electrodynamics. 
                            Geophysical Research Letters, 19(6), 601–604.
                            """,
                            html.A("https://doi.org/10.1029/92gl00401.", href="https://doi.org/10.1029/92gl00401", target="_blank")
                        ]),
                        html.P([
                            """
                            Codrescu, M. V., Negrea, C., Fedrizzi, M., Fuller-Rowell, T. J., Dobin, A., Jakowsky, N., et al. (2012). A real-time run of the coupled thermosphere ionosphere plasmasphere electrodynamics (CTIPe) model. 
                            Space Weather, 10(2), S02001. 
                            """,
                            html.A("https://doi.org/10.1029/2011SW000736.", href="https://doi.org/10.1029/2011SW000736", target="_blank")
                        ]),
                        html.P([
                            """
                            Ridley, A. J., Deng, Y., & Tóth, G. (2006). The global ionosphere-thermosphere model. 
                            Journal of Atmospheric and Solar-Terrestrial Physics, 68(8), 839–864. 
                            """,
                            html.A("https://doi.org/10.1016/j.jastp.2006.01.008.", href="https://doi.org/10.1016/j.jastp.2006.01.008", target="_blank")
                        ]),
                        html.P([
                            """
                            Hurrell, J. W., Holland, M. M., Gent, P. R., Ghan, S., Kay, J. E., Kushner, P. J., et al. (2013). The community Earth system model: A framework for collaborative research. 
                            Bulletin of the American Meteorological Society, 94(9), 1339–1360. 
                            """,
                            html.A("https://doi.org/10.1175/BAMS-D-12-00121.1.", href="https://doi.org/10.1175/BAMS-D-12-00121.1", target="_blank")
                        ]),
                        html.P([
                            """
                            Retterer, J. M. (2005). Physics-based forecasts of equatorial radio scintillation for the communication and navigation outage forecasting system (C/NOFS). 
                            Space Weather, 3(12), S12C03. 
                            """,
                            html.A("https://doi.org/10.1029/2005SW000146.", href="https://doi.org/10.1029/2005SW000146", target="_blank")
                        ]),
                        html.P([
                            """
                            Lin, C. Y., Matsuo, T., Liu, J. Y., Lin, C. H., Tsai, H. F., and Araujo-Pradere, E. A.: Ionospheric assimilation of radio occultation and ground-based GPS data using non-stationary background model error covariance. 
                            Atmos. Meas. Tech., 8, 171–182.
                            """,
                            html.A("https://doi.org/10.5194/amt-8-171-2015.", href="https://doi.org/10.5194/amt-8-171-2015", target="_blank")
                        ])
                    ],
                    id="references"
                )
            ],
            id="content"
        )    
    ],
    id="description-page"
)