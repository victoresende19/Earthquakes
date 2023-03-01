import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from pandas import DataFrame

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
                        animation_frame=(None if visualizacaoPeriodo == 'Não' else 'Year'), scope=regiao, width=900, height=600)
    # Fazendo com que as fronteiras aparecam
    mapa.update_geos(showcountries=True)

    if regiao == 'world':
        # Ajustando rotacao do globo
        mapa.layout.geo.projection = {
            'rotation': {'lon': 200}, 'type': projecoes}

    return mapa
