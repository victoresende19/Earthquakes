###############################################################################################################################################################################################################
#                                                                                               Bibliotecas
###############################################################################################################################################################################################################
import datetime
import streamlit as st

import pandas as pd
import urllib.request
import json
import plotly.express as px
import plotly.graph_objects as go

###############################################################################################################################################################################################################
#                                                                                       Inicio da página Streamlit - Input dos dados
###############################################################################################################################################################################################################
st.set_page_config(layout="wide", initial_sidebar_state='expanded')

st.markdown("<h2 style='text-align: center; color: black;'>Visualização dinâmica de tremores</h2>",
            unsafe_allow_html=True)
st.sidebar.title('Filtros de pesquisa')

magMinima = 2

# st.sidebar.markdown("<h4 style='text-align: center; color: black;'>Preencha os campos para criar uma visualização dinâmica </h4>",
# unsafe_allow_html=True)
startTime = st.sidebar.date_input(
    "Data de inicio (Ano/ Mês / Dia):", datetime.date(2011, 1, 1))
endTime = st.sidebar.date_input(
    "Data final (Ano/ Mês / Dia):", datetime.date(2014, 1, 1))
magnitude_desejada = st.sidebar.slider('Magnitude mínima:', magMinima, 10, 5)
visualizacaoTremor = st.sidebar.selectbox(
    'Tipo de tremor:', ('Terremoto', 'Explosão', 'Explosão Nuclear', 'Explosão de rochas', 'Explosão de pedreira'))
tsunamiFilter = st.sidebar.selectbox('Verificar tsunami:', ('Não', 'Sim'))
visualizacaoPeriodo = st.sidebar.selectbox(
    'Visualização por ano:', ('Não', 'Sim'))
option = st.sidebar.selectbox(
    'Tipo de projeção:',
    ('natural earth', 'mercator', 'equirectangular', 'orthographic', 'kavrayskiy7', 'miller', 'robinson', 'eckert4', 'azimuthal equal area', 'azimuthal equidistant', 'conic equal area',
     'conic conformal', 'conic equidistant', 'gnomonic', 'stereographic', 'mollweide', 'hammer', 'transverse mercator', 'albers usa', 'winkel tripel', 'aitoff', 'sinusoidal'))


###############################################################################################################################################################################################################
#                                                                                       Manipulação dos dados
###############################################################################################################################################################################################################
# Acessando a API de maneira dinâmica utilizando os inputs do usuário
url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={0}&endtime={1}&minmagnitude={magMinima}&limit=20000'.format(
    startTime, endTime, magnitude_desejada)
response = urllib.request.urlopen(url).read()
data = json.loads(response.decode('utf-8'))

###############################################################################################################################################################################################################
# Extraindo variáveis do JSON
magnitude = []

for mag in data['features']:
    magnitude.append(mag['properties']['mag'])

tsunami = []

for tsu in data['features']:
    tsunami.append(tsu['properties']['tsunami'])

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

timestamp = []

for time in data['features']:
    timestamp.append(time['properties']['time'])

###############################################################################################################################################################################################################
# Criando data frame com as variáveis em lista
dicionario_geral = {'Magnitude': magnitude, 'Tsunami': tsunami,
                    'Tipo': tipoTerremoto, 'Alerta': alerta,
                    'Latitude': latitude, 'Longitude': longitude,
                    'Timestamp': timestamp}
df = pd.DataFrame.from_dict(dicionario_geral)

###############################################################################################################################################################################################################
# Ajustando variáveis de data/tempo
df.Timestamp = pd.to_datetime(df.Timestamp, unit='ms')
df['Year'] = pd.to_datetime(df.Timestamp).dt.year
df = df.sort_values(by=['Year'], ascending=True)

# Renomeando observações
# Variável Tsunami
mapping_tsunami = {"Tsunami": {0: 'Não', 1: 'Sim'}}
df = df.replace(mapping_tsunami)

# Variável Tipo
mapping_tipo = {"Tipo": {'earthquake': 'Terremoto', 'explosion': 'Explosão', 'nuclear explosion':
                         'Explosão Nuclear', 'rock burst': 'Explosão de rochas', 'quarry blast': 'Explosão de pedreira'}}
df = df.replace(mapping_tipo)

df = df[df.Tipo == visualizacaoTremor]
df = df[df.Tsunami == tsunamiFilter]
###############################################################################################################################################################################################################
# Gráficos
# Mapa Mundi com projecao ortografica
figMapaMundi = px.scatter_geo(data_frame=df, lat="Latitude", lon="Longitude", color="Magnitude", size=df.Magnitude**10, size_max=60,
                              color_continuous_scale=[
                                  '#04290d', 'yellow', 'red'],
                              animation_frame=(None if visualizacaoPeriodo == 'Não' else 'Year'), width=900, height=600)
figMapaMundi.layout.geo.projection = {'rotation': {
    'lon': 200}, 'type': option}  # Ajustando rotacao do globo
# Fazendo com que as fronteiras aparecam
figMapaMundi.update_geos(showcountries=True)

# Mapa da Asia com projecao natural da terra
figAsia = px.scatter_geo(data_frame=df, lat="Latitude", lon="Longitude", color="Magnitude", size=df.Magnitude**10, size_max=60,
                         projection=option, color_continuous_scale=[
                             '#04290d', 'yellow', 'red'],
                         animation_frame=(None if visualizacaoPeriodo == 'Não' else 'Year'), scope='asia', width=900, height=600)

figAfrica = px.scatter_geo(data_frame=df, lat="Latitude", lon="Longitude", color="Magnitude", size=df.Magnitude**10, size_max=60,
                           projection=option, color_continuous_scale=[
                               '#04290d', 'yellow', 'red'],
                           animation_frame=(None if visualizacaoPeriodo == 'Não' else 'Year'), scope='africa', width=900, height=600)

figAmericaNorte = px.scatter_geo(data_frame=df, lat="Latitude", lon="Longitude", color="Magnitude", size=df.Magnitude**10, size_max=60,
                                 projection=option, color_continuous_scale=[
                                     '#04290d', 'yellow', 'red'],
                                 animation_frame=(None if visualizacaoPeriodo == 'Não' else 'Year'), scope='north america', width=900, height=600)

figAmericaSul = px.scatter_geo(data_frame=df, lat="Latitude", lon="Longitude", color="Magnitude", size=df.Magnitude**10, size_max=60,
                               projection=option, color_continuous_scale=[
                                   '#04290d', 'yellow', 'red'],
                               animation_frame=(None if visualizacaoPeriodo == 'Não' else 'Year'), scope='south america', width=900, height=600)

figEuropa = px.scatter_geo(data_frame=df, lat="Latitude", lon="Longitude", color="Magnitude", size=df.Magnitude**10, size_max=60,
                           projection=option, color_continuous_scale=[
                               '#04290d', 'yellow', 'red'],
                           animation_frame=(None if visualizacaoPeriodo == 'Não' else 'Year'), scope='europe', width=900, height=600)

###############################################################################################################################################################################################################
#                                                                                      Demonstração dos gráficos após os inputs
###############################################################################################################################################################################################################
#st.sidebar.title('Menu de pesquisa por área')
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
    # st.write(df)

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
