import dash_bootstrap_components as dbc
from dash import html

description_page = html.Div(
    [
        html.Div(
            [
                html.Div(html.H5("Table of Contents")),
                html.Ul(
                    [
                        html.Li(html.A("Introduction", href="#introduction", className="TOC-link")),
                        html.Li(html.A("Challenges", href="#challenges", className="TOC-link")),
                        html.Li(html.A("Campaign Objective", href="#objectives", className="TOC-link")),
                        html.Li(html.A("Methodology", href="#methodology", className="TOC-link")),
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
                        html.H1("Introduction"),
                        html.P(
                            """
                            Thermospheric density is the dominant source of uncertainty in the atmospheric drag. The diagram in Figure 1
                            shows how the data and model are involved in drag calculation. 
                            """
                        ),
                        html.Div(
                            [
                                html.H4("Key Considerations"),
                                html.Ul([
                                    html.Li("Thermosphere models estimate neutral density, composition, and temperature based on the solar and geomagnetic drivers."),
                                    html.Li(
                                        """
                                        Physics-based models with the lower boundary located around the mesopause also need to specify the lower 
                                        boundary condition representing the variability 
                                        from the lower atmosphere.
                                        """
                                    ),
                                    html.Li("Biases from thermospheric models are amplified due to the satellite shape and aerodynamic  model when calculating the drag force."),
                                    html.Li(
                                        """ 
                                        This, in turn, introduces several error sources originating from the modeled thermospheric states in 
                                        orbit computation.
                                        """
                                    )
                                ]),
                            ],
                            className="accent-gray"
                        ),
                        html.P(
                            """
                            To make advances in orbit computation and determination, accurate 
                            specification and forecasting of thermosphere are required. Modelled neutral density must be validated against 
                            high-quality and high-spatial resolution neutral density datasets to identify strengths and weaknesses, establish 
                            error budgets, and improve the models after ingestion.
                            """
                        ),
                        html.Div([
                            dbc.Button(
                                "Figure 1",
                                id="fig-1-btn",
                                className="mb-3",
                                color="secondary",
                                n_clicks=0
                            ),
                            dbc.Collapse(
                                html.Div(
                                    [html.Img(className="description-fig", src="assets/Thermosphere_fig_1.png", 
                                            alt="Figure 1: Diagram showing the data and models of a drag calculation."),
                                    html.P(html.I("Firgure 1. Diagram showing the data and models of a drag calculation."))],
                                    className="img-container"
                                ),
                                id="fig-1-collapse",
                                is_open=False
                            )
                        ])
                    ],
                    id="introduction"
                ),
                html.Div(
                    [
                        html.H1("Challenges"),
                        html.P("However, there are still several challenges remaining in the validation of neutral density."),
                        html.Div(
                            [
                                html.Ol([
                                    html.Li([
                                        html.B("Limited Scope: "),
                                        """
                                        Validation studies often invloved only one or two events and a subset of models. this approach may not 
                                        be robust or comprehansive.
                                        """
                                    ], style={"margin-bottom": "10px"}),
                                    html.Li([
                                        html.B("Version Management: "),
                                        """
                                        Staying updated with the growing number of models and their various versions remains chellenging, 
                                        especially with open source models.
                                        """
                                    ], style={"margin-bottom": "10px"}),
                                    html.Li([
                                        html.B("Lack of an Online Platform: "),
                                        """
                                        Unified validation effort requires an online platform to keep track of the progress of model development.
                                        """
                                    ])
                                ]),
                            ],
                            id="challenges-list"
                        ),
                        html.P(
                            """
                            To addres these challenges, an assessment of thermosphere models under storm conditions was initiated within the COSPR 
                            ISWAT framework, leveraging the international collborative network. This allows the community to systematically track
                            the progress of thermosphere models over time.
                            """
                        )
                    ],
                    id="challenges"
                ),
                html.Div(
                    [
                        html.H1("Campaign Objectives"),
                        html.P(
                            """
                            This validation campaign focuses on validating 1-D neutral density output from various model runs/solutions with
                            observation data from GOCE, CHAMP, GRACE, SWARM, and/or GRACE_FO for different time periods. The thermophsere models
                            are executed in-house using CCMC Runs-on-Request system and accessed. The model performance during the selected 
                            geomagnetically storm times from 2001 to 2023 are assessed for this study.
                            """
                        )
                    ],
                    id="objectives"
                ),
                html.Div(
                    [
                        html.H1("Methodology"),
                        html.P(
                            """
                            An updated metric for thermospheric model assessment under geomagnetic storm conditions were proposed and implemented 
                            in the validation project (Sutton, 2018; Bruinsma et al., 2021; Bruinsma & Laurens, 2024). The metrics for 
                            comprehensive thermospheric model-data comparison are applied to establish the thermospheric model scorecard. 
                            """
                        ),
                        html.P(
                            """
                            Figure 2 (top) illustrates the four phases of a single-peak (SP) storm. Phase 1, the pre-storm interval, is used to 
                            de-bias the models relative to observations. A scaling factor is determined by computing the observed-to-computed (O/C) 
                            density ratio in the pre-storm phase, then applied to the model densities in all four phases. This de-biasing procedure 
                            is used to minimize the effect of non-storm related model errors on the assessment. 
                            """
                        ),
                        html.P(
                            """
                            Density data for the SP storms are selected from 30 hours before to 48 hours after the time when ap reaches 80, which 
                            defines t₀ and marks the end of Phase 2 (storm onset). Phase 3 encompasses the main and recovery phase, while Phase 4 
                            represents the post-storm phase.
                            """
                        ),
                        html.P(
                            """
                            Figure 2 (bottom) illustrates the phases for double or multiple-peaked (MP) storms, exemplified by the 10–16 July 2004 
                            event. For the MP storms, t₀ is defined as the time when ap reaches 80, similar to SP storms. In Figure 2 (bottom), 
                            Phase 3 for MP storms is extended due to a second occurrence of ap = 80 at t = 1.4. The duration of Phase 3 varies, 
                            ending when ap falls below 80 again (at t ≈ 3.0 in this example), plus an additional 36 hours. Phase 4 then extends 
                            for 12 hours beyond the end of Phase 3. Table 1 summarizes the phases and their duration for SP and MP storms computed 
                            as list below with respect to t0.
                            """
                        ),
                        html.Div([
                            dbc.Button(
                                "Figure 2",
                                id="fig-2-btn",
                                className="mb-3",
                                color="secondary",
                                n_clicks=0
                            ),
                            dbc.Collapse(
                                html.Div(
                                    [html.Img(className="description-fig", src="assets/Thermosphere_fig_2.png", alt="Figure 2."),
                                    html.P(html.I("""Figure 2. The four phases of the assessment interavl for single-peak (top) and multiple-peak (bottom) storms, with t0
                          centered on the time of the first peak in ap with a minimum of 80. The X-axis represents the day relative to t0.
                          Adapted from Bruinsma and Laurens (2024)."""))],
                                    className="img-container"
                                ),
                                id="fig-2-collapse",
                                is_open=False
                            )
                        ]),
                        html.Div([
                            dbc.Button(
                                "Phase Table",
                                id="phase-table-btn",
                                className="mb-3",
                                color="secondary",
                                n_clicks=0
                            ),
                            dbc.Collapse(
                                html.Div([
                                    html.Table([
                                        html.Tr([
                                            html.Th("Phase"),
                                            html.Th("Single-Peak (SP) Storm"),
                                            html.Th("Multiple-Peaked (MP) Storm")
                                        ]),
                                        html.Tr([
                                            html.Td("Phase 1"),
                                            html.Td("t0 - 30 h to t0 - 18 h"),
                                            html.Td("t0 - 30 h to t0 - 18 h"),
                                        ]),
                                        html.Tr([
                                            html.Td("Phase 2"),
                                            html.Td("t0 - 18 h to t0"),
                                            html.Td("t0 - 18 h to t0")
                                        ]),
                                        html.Tr([
                                            html.Td("Phase 3"),
                                            html.Td("t0  to t0 + 36 h"),
                                            html.Td("t0 to t0 + variable duration + 36 h")
                                        ]),
                                        html.Tr([
                                            html.Td("Phase 4"),
                                            html.Td("t0 + 36 h to t0 + 48 h"),
                                            html.Td("End of Phase 3 + 12 h")
                                        ])
                                    ]), 
                                    html.Br(),
                                    html.P(html.I(
                                        """Table 1. The phases and their durations for single-peak (SP) and multiple-peaked (MP) storms, 
                                        computed relative to t0, as listed below. Adapted from Bruinsma and Laurens (2024)."""
                                    ))
                                ]),
                                id="phase-table-collapse",
                                is_open=False
                            )
                        ]),
                        html.P(
                            """
                            After debiasing, the observed-to-computed (O/C) density ratio is re-computed for the main and recovery phases of each 
                            storm to express model’s skill to reproduce observations during the geomagnetically storm times. Density ratios of one 
                            indicate perfect duplication of the observations, i.e., an unbiased model that reproduces all features; deviation from 
                            unity points to under (larger than one) or overestimation (smaller than one). A model bias, i.e., the mean of the 
                            density ratios differs from unity, is most damaging to orbit extrapolation because it causes position errors that 
                            increase with time.
                            """
                        ),
                        html.P(
                            """
                            The standard deviation (Std. Dev.) of the density ratios, computed as percentage of the observation, represents a 
                            combination of the ability of the model to reproduce observed density variations, and the geophysical noise 
                            (e.g., waves, the short duration effect of large flares) and instrumental noise in the observations.
                            """
                        ),
                        html.Div([
                            dbc.Button(
                                "Mean/Std Computations",
                                id="comp-btn",
                                className="mb-3",
                                color="secondary",
                                n_clicks=0
                            ),
                            dbc.Collapse(
                                [
                                    html.P(
                                        """
                                        The mean and Std. Dev. of the O/C density ratios, due to their distribution, are computed in log space (Sutton, 2018; 
                                        Bruinsma et al., 2021):
                                        """
                                    ),
                                    html.Ul([
                                        html.Li([
                                            "Average Observed-to-Compute Density (O/C) (= mean scaling factor of the model)",
                                            html.Ul(html.Li(html.Img(src="assets/Thermosphere_equation_1.png", alt="Mean_OC computation")))
                                        ]),
                                        html.Li([
                                            "Average standard deviation (Std. Dev.) of Observed-to-Compute Density (O/C)",
                                            html.Ul(html.Li(html.Img(src="assets/Thermosphere_equation_2.png", alt="StdDev_OC computation")))
                                        ])
                                    ]),
                                    html.P("where N is the total number of observations.")
                                ],
                                id="comp-collapse",
                                is_open=False
                            )
                        ]),
                    ],
                    id="methodology"
                ),
                html.Div(
                    [
                        html.H1("References"),
                        html.P([
                            """
                            Sutton EK. 2018. A new method of physics-based data assimilation for the quiet and disturbed thermosphere. 
                            Space Weather 16: 736–753.
                            """,
                            html.A("https://doi.org/10.1002/2017SW00178.", href="https://doi.org/10.1002/2017SW00178", target="_blank")
                        ]),
                        html.P([
                            """
                            Bruinsma S, Boniface C, Sutton EK & Fedrizzi M 2021. Thermosphere modeling capabilities assessment: geomagnetic storms. 
                            J. Space Weather Space Clim. 11, 12.
                            """,
                            html.A("https://doi.org/10.1051/swsc/2021002.", href="https://doi.org/10.1051/swsc/2021002", target="_blank")
                        ]),
                        html.P([
                            """
                            Bruinsma S & Laurens S. 2024. Thermosphere model assessment for geomagnetic storms from 2001 to 2023. J. Space Weather 
                            Space Clim. 14, 28. 
                            """,
                            html.A("https://doi.org/10.1051/swsc/2024027.", href="https://doi.org/10.1051/swsc/2024027", target="_blank")
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