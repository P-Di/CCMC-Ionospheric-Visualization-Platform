from dash import html

def gen_MSISE00_01_data():
    return html.Div([
        html.H1("MSISE00-01 Metadata", style={"font-size": "20px", "font-weight": "bold"}),
        html.A("MSISE00-01 Home Page", href="https://ccmc.gsfc.nasa.gov/models/NRLMSIS~00/", target="_blank"),
        html.P(
            """
            NRLMSISE-00 is an empirical, global reference atmospheric model of the Earth from ground to space. It models the temperatures and
            densities of the atmosphere's components. A primary use of this model is to aid predictions of satellite orbital decay due to 
            atmospheric drag. This model has also been used by astronomers to calculate the mass of air between telescopes and laser beams in 
            order to assess the impact of laser guide stars on the non-lasing telescopes.
            """
        ),
        html.P(
            """
            The model, developed by Mike Picone, Alan Hedin, and Doug Drob, is based on the earlier models MSIS-86 and MSISE-90, but 
            updated with actual satellite drag data. It also predicts anomalous oxygen.
            """
        ),
        html.P(
            """
            NRL stands for the US Naval Research Laboratory. MSIS stands for mass spectrometer and incoherent scatter radar, the two 
            primary data sources for development of earlier versions of the model. E indicates that the model extends from the ground 
            through exosphere and 00 is the year of release.
            """
        ),
        html.P(
            """
            Over the years since introduction, NRLMSISE-00 has become the standard for international space research.
            """
        ),
        html.H2("Inputs", style={"font-size": "20px", "font-weight": "bold"}),
        html.Ul([
            html.Li("Year and day"),
            html.Li("Time of day"),
            html.Li("Geodetic altitude from 0 to 1,000 km"),
            html.Li("Geodetic latitude longitude"),
            html.Li("Local apparent solar time"),
            html.Li("81 day average of F10.7 solar flux"),
            html.Li("Daily F10.7 solar flux for previous day"),
            html.Li("Daily magnetic index")
        ]),
        html.H2("Outputs", style={"font-size": "20px", "font-weight": "bold"}),
        html.Ul([
            html.Li("Helium number density"),
            html.Li("Oxygen (O) number density"),
            html.Li("Oxygen (O2) number density"),
            html.Li("Nitrogen (N) number density"),
            html.Li("Nitrogen (N2) number density"),
            html.Li("Argon number density"),
            html.Li("Hydrogen number density"),
            html.Li("Total mass density"),
            html.Li("Anomalous oxygen number density"),
            html.Li("Exospheric temperature"),
            html.Li("Temperature at altitude")
        ]),
        html.H2("Domains", style={"font-size": "20px", "font-weight": "bold"}),
        html.P("Thermosphere"),
        html.H2("Space Weather Impacts", style={"font-size": "20px", "font-weight": "bold"}),
        html.P("Atmosphere variability (satellite/debris drag)"),
    ], className="data-source-metadata")