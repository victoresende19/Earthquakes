###############################################################################################################################################################################################################
#                                                                                       Bibliotecas
###############################################################################################################################################################################################################
import datetime
import streamlit as st

import pandas as pd
import urllib.request
import json
import plotly.express as px
from plotly.subplots import make_subplots

###############################################################################################################################################################################################################
#                                                                                       Inicio da página Streamlit - Input dos dados
###############################################################################################################################################################################################################
st.set_page_config(layout="wide", initial_sidebar_state='expanded')

st.markdown("<h2 style='text-align: center; color: black;'>Visualização de Terremotos </h2>",
            unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: black;'>Preencha os campos para criar uma visualização dinâmica </h4>",
            unsafe_allow_html=True)
startTime = st.date_input("Data de inicio:", datetime.date(1975, 1, 1))
endTime = st.date_input("Data final:", datetime.date(1990, 1, 1))
magnitude_desejada = st.slider('Magnitude desejada', 0, 10, 5)
option = st.selectbox(
    'Escolha o tipo de projeção',
    ('orthographic', 'mercator', 'equirectangular', 'natural earth', 'kavrayskiy7', 'miller', 'robinson', 'eckert4', 'azimuthal equal area', 'azimuthal equidistant', 'conic equal area',
     'conic conformal', 'conic equidistant', 'gnomonic', 'stereographic', 'mollweide', 'hammer', 'transverse mercator', 'albers usa', 'winkel tripel', 'aitoff', 'sinusoidal'))


###############################################################################################################################################################################################################
#                                                                                       Manipulação dos dados
###############################################################################################################################################################################################################

# Acessando a API de maneira dinâmica utilizando os inputs do usuário
url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={0}&endtime={1}&minmagnitude={2}&limit=20000'.format(
    startTime, endTime, magnitude_desejada)
response = urllib.request.urlopen(url).read()
data = json.loads(response.decode('utf-8'))

###############################################################################################################################################################################################################
# Extraindo variáveis do JSON
magnitude = []

for mag in data['features']:
    magnitude.append(mag['properties']['mag'])

latitude = []

for lat in data['features']:
    latitude.append(lat['geometry']['coordinates'][1])

longitude = []

for lon in data['features']:
    longitude.append(lon['geometry']['coordinates'][0])

timestamp = []

for time in data['features']:
    timestamp.append(time['properties']['time'])

###############################################################################################################################################################################################################
# Criando data frame com as variáveis em lista
dicionario_geral = {'Magnitude': magnitude, 'Latitude': latitude,
                    'Longitude': longitude, 'Timestamp': timestamp}
df = pd.DataFrame.from_dict(dicionario_geral)

###############################################################################################################################################################################################################
# Ajustando variáveis de data/tempo
df.Timestamp = pd.to_datetime(df.Timestamp, unit='ms')
df['Year'] = pd.to_datetime(df.Timestamp).dt.year
df = df.sort_values(by=['Year'], ascending=True)


###############################################################################################################################################################################################################
# Gráficos
# Mapa Mundi com projecao ortografica
figMapaMundi = px.scatter_geo(data_frame=df, lat="Latitude", lon="Longitude", color="Magnitude", size=df.Magnitude**5,
                              projection=option, color_continuous_scale=[
                                  '#04290d', 'yellow', 'red'],
                              animation_frame="Year", width=900, height=600)

# Mapa da Asia com projecao natural da terra
figAsia = px.scatter_geo(data_frame=df, lat="Latitude", lon="Longitude", color="Magnitude", size=df.Magnitude**3,
                         projection=option, color_continuous_scale=[
                             '#04290d', 'yellow', 'red'],
                         animation_frame="Year", scope='asia', width=900, height=600)

figAfrica = px.scatter_geo(data_frame=df, lat="Latitude", lon="Longitude", color="Magnitude", size=df.Magnitude**3,
                           projection=option, color_continuous_scale=[
                               '#04290d', 'yellow', 'red'],
                           animation_frame="Year", scope='africa', width=900, height=600)

figAmericaNorte = px.scatter_geo(data_frame=df, lat="Latitude", lon="Longitude", color="Magnitude", size=df.Magnitude**3,
                                 projection=option, color_continuous_scale=[
                                     '#04290d', 'yellow', 'red'],
                                 animation_frame="Year", scope='north america', width=900, height=600)

figAmericaSul = px.scatter_geo(data_frame=df, lat="Latitude", lon="Longitude", color="Magnitude", size=df.Magnitude**3,
                               projection=option, color_continuous_scale=[
                                   '#04290d', 'yellow', 'red'],
                               animation_frame="Year", scope='south america', width=900, height=600)

figEuropa = px.scatter_geo(data_frame=df, lat="Latitude", lon="Longitude", color="Magnitude", size=df.Magnitude**3,
                           projection=option, color_continuous_scale=[
                               '#04290d', 'yellow', 'red'],
                           animation_frame="Year", scope='europe', width=900, height=600)


print(['orthographic', 'mercator', 'equirectangular', 'natural earth', 'kavrayskiy7', 'miller', 'robinson', 'eckert4', 'azimuthal equal area', 'azimuthal equidistant', 'conic equal area',
      'conic conformal', 'conic equidistant', 'gnomonic', 'stereographic', 'mollweide', 'hammer', 'transverse mercator', 'albers usa', 'winkel tripel', 'aitoff', 'sinusoidal'])

###############################################################################################################################################################################################################
#                                                                                      Demonstração dos gráficos após os inputs
###############################################################################################################################################################################################################
st.sidebar.title('Menu de pesquisa por área')
africa = 'África'
americaNorte = 'América do Norte'
americaSul = 'América do Sul'
asia = 'Ásia'
europa = 'Europa'
mundial = 'Mapa Mundi'


paginaContinentes = st.sidebar.selectbox('Selecione o continente de pesquisa', [
                                         mundial, africa, americaNorte, americaSul, asia, europa])

if paginaContinentes == mundial:
    st.markdown("<h3 style='text-align: center; color: black;'>Visualização de terremotos mundiais <br> {0} a {1} </br> </h3>".format(startTime.strftime("%d/%m/%Y"), endTime.strftime("%d/%m/%Y")),
                unsafe_allow_html=True)

    st.plotly_chart(figMapaMundi, use_container_width=True)

if paginaContinentes == africa:
    st.markdown("<h3 style='text-align: center; color: black;'>Visualização de terremotos na Africa <br> {0} a {1} </br> </h3>".format(startTime.strftime("%d/%m/%Y"), endTime.strftime("%d/%m/%Y")),
                unsafe_allow_html=True)

    st.plotly_chart(figAfrica, use_container_width=True)

if paginaContinentes == americaNorte:
    st.markdown("<h3 style='text-align: center; color: black;'>Visualização de terremotos na América do Norte <br> {0} a {1} </br> </h3>".format(startTime.strftime("%d/%m/%Y"), endTime.strftime("%d/%m/%Y")),
                unsafe_allow_html=True)

    st.plotly_chart(figAmericaNorte, use_container_width=True)

if paginaContinentes == americaSul:
    st.markdown("<h3 style='text-align: center; color: black;'>Visualização de terremotos na América do Sul <br> {0} a {1} </br> </h3>".format(startTime.strftime("%d/%m/%Y"), endTime.strftime("%d/%m/%Y")),
                unsafe_allow_html=True)

    st.plotly_chart(figAmericaSul, use_container_width=True)

if paginaContinentes == asia:
    st.markdown("<h3 style='text-align: center; color: black;'>Visualização de terremotos na Ásia <br> {0} a {1} </br> </h3>".format(startTime.strftime("%d/%m/%Y"), endTime.strftime("%d/%m/%Y")),
                unsafe_allow_html=True)

    st.plotly_chart(figAsia, use_container_width=True)

if paginaContinentes == europa:
    st.markdown("<h3 style='text-align: center; color: black;'>Visualização de terremotos na Europa <br> {0} a {1} </br> </h3>".format(startTime.strftime("%d/%m/%Y"), endTime.strftime("%d/%m/%Y")),
                unsafe_allow_html=True)

    st.plotly_chart(figEuropa, use_container_width=True)
