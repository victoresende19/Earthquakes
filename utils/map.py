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

    mapa = px.scatter_geo(data_frame=data, lat="Latitude", lon="Longitude", color="Magnitude", size=data.Magnitude**10, size_max=60,
                          projection=projecoes, color_continuous_scale=[
                              '#04290d', 'yellow', 'red'],
                          animation_frame=(None if visualizacaoPeriodo == 'Não' else 'Year'), scope=regiao, width=900, height=600,
                          custom_data=["Latitude", "Longitude", "Magnitude"])  

    mapa.update_geos(showcountries=True)

    if regiao == 'world':
        # Ajustando rotação do globo
        mapa.layout.geo.projection = {
            'rotation': {'lon': 200}, 'type': projecoes}

    # Personalizando o tooltip
    mapa.update_traces(
        hovertemplate='<br>'.join([
            'Latitude: %{customdata[0]}',
            'Longitude: %{customdata[1]}',
            'Magnitude: %{customdata[2]}'
        ])
    )

    return mapa
