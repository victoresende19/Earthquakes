import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from pandas import DataFrame
import streamlit as st

@st.cache_data(show_spinner="Consultando dados...", max_entries=500)
def mapa(data: DataFrame, visualizacaoPeriodo: str,  projecoes: list[str] = None, regiao: list[str] = None):
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

    # mapa = px.scatter_geo(data_frame=data, lat="Latitude", lon="Longitude", color="Magnitude", size=data.Magnitude**10, size_max=35,
    #                       projection=projecoes_mapa[projecoes], color_continuous_scale=['#04290d', 'yellow', 'red'],
    #                       animation_frame=(None if visualizacaoPeriodo == 'Não' else 'Ano'), scope=regioes[regiao], width=900, height=600,
    #                       custom_data=["Latitude", "Longitude", "Magnitude"]) 
    # if regiao == 'world':
    #     # Ajustando rotação do globo
    #     mapa.layout.geo.projection = {'rotation': {'lon': 200}, 'type': projecoes}


    mapa = px.scatter_mapbox(data_frame=data,
                             lat="Latitude",
                             lon="Longitude",
                             color="Magnitude",
                             color_continuous_scale=['#04290d', 'yellow', 'red'],
                             size=data.Magnitude**10,
                             size_max=35,
                             zoom=1.8,
                             height=900,
                             width=800,
                             mapbox_style="open-street-map",
                             animation_frame=(None if visualizacaoPeriodo == 'Não' else 'Ano'),
                             custom_data=["Timestamp", "Latitude", "Longitude", "Magnitude", "Ano"],
                             center=dict(lon=150))
    mapa.update_layout(coloraxis_colorbar=dict(orientation='h', y=1, xanchor='center', yanchor='bottom', tickfont=dict(color='black'), title_font=dict(color='black')))

    # Personalizando o tooltip
    mapa.update_traces(
        hovertemplate='<br>'.join([
            'Data (m/d/a) e hora: %{customdata[0]}',
            'Latitude: %{customdata[1]}',
            'Longitude: %{customdata[2]}',
            'Magnitude: %{customdata[3]}'
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
