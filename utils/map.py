import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from pandas import DataFrame
import streamlit as st

@st.cache_data(show_spinner="Consultando dados...", max_entries=500)
def mapa(regiao: list[str], data: DataFrame, projecoes: list[str], visualizacaoPeriodo: str):
    """
    Description
    -----------
    Mapa versátil com as marcações de tremores e as
    respectivas magnitudes.

    Parameters
    ----------
    regiao: string
    data: DataFrame
    projecoes: string


    Returns
    -------
    Objetos plotly com o mapa interativo.
    """

    mapa = px.scatter_geo(data_frame=data, lat="Latitude", lon="Longitude", color="Magnitude", size=data.Magnitude**10, size_max=35,
                          projection=projecoes_mapa[projecoes], color_continuous_scale=['#04290d', 'yellow', 'red'],
                          animation_frame=(None if visualizacaoPeriodo == 'Não' else 'Ano'), scope=regioes[regiao], width=900, height=600,
                          custom_data=["Latitude", "Longitude", "Magnitude"])  

    mapa.update_geos(showcountries=True)

    if regiao == 'world':
        # Ajustando rotação do globo
        mapa.layout.geo.projection = {'rotation': {'lon': 200}, 'type': projecoes}

    # Personalizando o tooltip
    mapa.update_traces(
        hovertemplate='<br>'.join([
            'Latitude: %{customdata[0]}',
            'Longitude: %{customdata[1]}',
            'Magnitude: %{customdata[2]}'
        ])
    )

    return mapa


regioes = {
    'Mundo': 'world',
    'África': 'africa',
    'América do Norte': 'north america',
    'América do Sul': 'south america',
    'Ásia': 'asia',
    'Europa': 'europe',
}

projecoes_mapa = {
    'Terra Natural': 'natural earth',
    'Mercator': 'mercator',
    'Equiretangular': 'equirectangular',
    'Ortográfica': 'orthographic',
    'Kavrayskiy7': 'kavrayskiy7',
    'Miller': 'miller',
    'Robinson': 'robinson',
    'Eckert4': 'eckert4',
    'Área Igual Azimutal': 'azimuthal equal area',
    'Equidistante Azimutal': 'azimuthal equidistant',
    'Área Igual Cônica': 'conic equal area',
    'Conforme Cônica': 'conic conformal',
    'Equidistante Cônica': 'conic equidistant',
    'Gnômica': 'gnomonic',
    'Estereográfica': 'stereographic',
    'Mollweide': 'mollweide',
    'Hammer': 'hammer',
    'Mercator Transversa': 'transverse mercator',
    'Albers EUA': 'albers usa',
    'Winkel Tripel': 'winkel tripel',
    'Aitoff': 'aitoff',
    'Sinusoidal': 'sinusoidal'
}
