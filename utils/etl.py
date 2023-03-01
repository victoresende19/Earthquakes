import urllib.request
import json
import pandas as pd
from datetime import datetime
import streamlit as st

@st.cache_data(show_spinner="Consultando dados...", max_entries=500)
def coleta_dados(startTime: datetime, endTime: datetime, magnitude_desejada: int):
    """
    Description
    -----------
    Consulta dos dados na API USGS.
    
    Parameters
    ----------
    startTime: DateTime
        Data de entrada.

    endTime: DateTime
        Data de saída.

    magnitude_desejada: int
        Magnitude mínima.

    Returns
    -------
    Dados de terremotos em formato JSON no intervalo solicitado.
    """

    url = f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={startTime}&endtime={endTime}&minmagnitude={magnitude_desejada}&limit=20000'
    response = urllib.request.urlopen(url).read()
    data = json.loads(response.decode('utf-8'))
    return data

# Manipulando os dados


@st.cache_data(show_spinner="Manipulando os dados...", max_entries=500)
def manipula_dados(data: dict):
    """
    Description
    -----------
    Manipulação dos dados coletados (criando o dataframe).

    Parameters
    ----------
    data: dict

    Returns
    -------
    Dados de terremotos em formato dataframe.
    """

    magnitude = []
    for mag in data['features']:
        magnitude.append(mag['properties']['mag'])

    tipoTerremoto = []
    for tipo in data['features']:
        tipoTerremoto.append(tipo['properties']['type'])

    alerta = []
    for alert in data['features']:
        alerta.append(alert['properties']['alert'])

    latitude = []
    for lat in data['features']:
        latitude.append(lat['geometry']['coordinates'][1])

    longitude = []
    for lon in data['features']:
        longitude.append(lon['geometry']['coordinates'][0])

    profundidade = []
    for prof in data['features']:
        profundidade.append(prof['geometry']['coordinates'][2])

    timestamp = []
    for time in data['features']:
        timestamp.append(time['properties']['time'])

    significancia = []
    for sig in data['features']:
        significancia.append(sig['properties']['sig'])

    local = []
    for loc in data['features']:
        local.append(loc['properties']['place'])

    # Criando data frame com as variáveis em lista
    dicionario_geral = {'Local': local, 'Magnitude': magnitude, 'Tipo': tipoTerremoto,
                        'Significancia': significancia, 'Profundidade': profundidade,
                        'Latitude': latitude, 'Longitude': longitude, 'Timestamp': timestamp}
    terremotos = pd.DataFrame.from_dict(dicionario_geral)

    # Ajustando variáveis de terremotos/tempo
    terremotos.Timestamp = pd.to_datetime(terremotos.Timestamp, unit='ms')
    terremotos['Ano'] = pd.to_datetime(terremotos.Timestamp).dt.year
    terremotos = terremotos.sort_values(by=['Timestamp'], ascending=False)

    return terremotos
