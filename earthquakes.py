###############################################################################################################################################################################################################
#                                                                                               Bibliotecas
###############################################################################################################################################################################################################
import datetime
import time
import streamlit as st

import pandas as pd
import urllib.request
import json
import plotly.express as px
import plotly.graph_objects as go

###############################################################################################################################################################################################################
#                                                                                                           Funções
###############################################################################################################################################################################################################

#Funcao barra progresso
def Progresso():
    texto = st.empty()
    texto.markdown(f"<h2 style='text-align: center; color: black;'>Carregando...  </h2>",
                unsafe_allow_html=True)
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1)    
    texto.empty()
    return my_bar

# Funcao plotar mapa 
def Mapa(regiao):
    mapa = px.scatter_geo(data_frame=df, lat="Latitude", lon="Longitude", color="Magnitude", size=df.Magnitude**10, size_max=60,
                        projection=projecoes, color_continuous_scale=['#04290d', 'yellow', 'red'],
                        animation_frame=(None if visualizacaoPeriodo == 'Não' else 'Year'), scope=regiao, width=900, height=600)
    # Fazendo com que as fronteiras aparecam
    mapa.update_geos(showcountries=True)

    if regiao == 'world':
        # Ajustando rotacao do globo
        mapa.layout.geo.projection = {'rotation': {'lon': 200}, 'type': projecoes} 

    return mapa

###############################################################################################################################################################################################################
#                                                                                       Inicio da página Streamlit - Input dos dados
###############################################################################################################################################################################################################
st.set_page_config(layout="wide", initial_sidebar_state='expanded')
st.sidebar.title('Filtros de pesquisa')
projeto = st.sidebar.selectbox('Projeto', ('Documentação', 'Mapas'))

if projeto == 'Documentação':
    #Dividindo a pagina em tres colunas
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("")

    #Utilizando apenas a coluna do meio pois é centralizada
    with col2:
        st.markdown("<h2 style='text-align: center; color: black;'>Observatório sismológico</h2>",
            unsafe_allow_html=True)
        st.image("https://www.coladaweb.com/wp-content/uploads/2014/12/20210809-placas-tectonicas.png")
        st.markdown("""<p align='justify'; color: black;'>
                Esse projeto utiliza ferramentas de mineração, coleta, visualização dos dados, criação de modelos preditivos e implementação. Os dados utilizados nos mapas a seguir são oriundos de uma API disponibilizada pelo Serviço Geológico dos Estados Unidos (USGS). A etapa de coleta dos dados foi realizado por meio da linguagem de programação Python, da qual se arquitetou o tratamento dos dados para a extração das variáveis pertinentes. Da mesma forma, a etapa de visualização dos dados e implementação se desenvolveram por meio da linguagem Python.</p>""",
                unsafe_allow_html=True)
        st.image("https://legacy.etap.org/demo/Earth_Science/es3/epicenter.jpg")

    with col3:
        st.write("")
    

if projeto == 'Mapas':
    st.markdown("<h2 style='text-align: center; color: black;'>Observatório sismológico</h2>",
                unsafe_allow_html=True)
    startTime = st.sidebar.date_input(
        "Data inicial (ano/mês/dia):", datetime.date(2011, 1, 1))

    endTime = st.sidebar.date_input(
        "Data final (ano/mês/dia):", datetime.date(2014, 1, 1))

    magMinima = 4
    magnitude_desejada = st.sidebar.slider('Magnitude mínima:', magMinima, 10, magMinima)

    paginaContinentes = st.sidebar.selectbox('Selecione a região de pesquisa', [
                                            'world', 'africa', 'north america', 'south america', 'asia', 'europe'])

    visualizacaoTremor = st.sidebar.selectbox(
        'Tipo de tremor:', ('Terremoto', 'Explosão', 'Explosão Nuclear', 'Explosão de rochas', 'Explosão de pedreira'))

    visualizacaoPeriodo = st.sidebar.selectbox('Visualização por ano:', ('Não', 'Sim'))

    projecoes = st.sidebar.selectbox(
        'Tipo de projeção:',
        ('natural earth', 'mercator', 'equirectangular', 'orthographic', 'kavrayskiy7', 'miller', 'robinson', 'eckert4', 'azimuthal equal area', 'azimuthal equidistant', 'conic equal area',
        'conic conformal', 'conic equidistant', 'gnomonic', 'stereographic', 'mollweide', 'hammer', 'transverse mercator', 'albers usa', 'winkel tripel', 'aitoff', 'sinusoidal'))

###############################################################################################################################################################################################################
#                                                                                       Manipulação dos dados
###############################################################################################################################################################################################################
    # Acessando a API de maneira dinâmica utilizando os inputs do usuário
    @st.cache(show_spinner = False)
    def Dados(startTime, endTime, magnitude_desejada):
        url = f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={startTime}&endtime={endTime}&minmagnitude={magnitude_desejada}&limit=20000'
        response = urllib.request.urlopen(url).read()
        data = json.loads(response.decode('utf-8'))
        return data
    
    data = Dados(startTime, endTime, magnitude_desejada)
    Progresso().empty()
###############################################################################################################################################################################################################
    # Extraindo variáveis do JSON
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

    timestamp = []

    for time in data['features']:
        timestamp.append(time['properties']['time'])

    # Criando data frame com as variáveis em lista
    dicionario_geral = {'Magnitude': magnitude, 'Timestamp': timestamp,
                        'Tipo': tipoTerremoto, 'Alerta': alerta,
                        'Latitude': latitude, 'Longitude': longitude}       
    df = pd.DataFrame.from_dict(dicionario_geral)

    # Ajustando variáveis de data/tempo
    df.Timestamp = pd.to_datetime(df.Timestamp, unit='ms')
    df['Year'] = pd.to_datetime(df.Timestamp).dt.year
    df = df.sort_values(by=['Year'], ascending=True)

    # Renomeando observações

    # Variável Tipo
    mapping_tipo = {"Tipo": {'earthquake': 'Terremoto', 'explosion': 'Explosão', 'nuclear explosion':
                            'Explosão Nuclear', 'rock burst': 'Explosão de rochas', 'quarry blast': 'Explosão de pedreira'}}
    df = df.replace(mapping_tipo)

    df = df[df.Tipo == visualizacaoTremor]

###############################################################################################################################################################################################################
#                                                                                      Demonstração dos gráficos após os inputs
###############################################################################################################################################################################################################
    dataInicio = startTime.strftime("%d/%m/%Y")
    dataFim = endTime.strftime("%d/%m/%Y")

    #Título gráfico
    st.markdown("<h2 style='text-align: center; color: black;'>Visualização interativa dos tremores causados</h2>",
                unsafe_allow_html=True)

    #Data utilizada
    st.markdown(f"<h4 style='text-align: center; color: black; font-size:16px'>{dataInicio} a {dataFim}</h4>",
                    unsafe_allow_html=True)

    #Volume dos dados
    st.markdown(f"<h4 style='text-align: center; color: black; font-size:16px'>Volume de dados pesquisados ({df.shape[0]})</h4>",
                    unsafe_allow_html=True)
    #Mapa
    st.plotly_chart(Mapa(paginaContinentes), use_container_width=True)

    #Observacoes
    st.markdown(f"<p style='text-align: center; color: black; font-size:16px'> <strong>Obs:</strong> Quanto maior a quantidade de dados, mais tempo irá demorar a pesquisa  </p>",
                    unsafe_allow_html=True)