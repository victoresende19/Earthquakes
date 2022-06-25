###############################################################################################################################################################################################################
#                                                                                               Bibliotecas
###############################################################################################################################################################################################################
import streamlit as st

import pandas as pd
import numpy as np

import datetime
import pytz
import time

import urllib.request
import json

import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib
###############################################################################################################################################################################################################
#                                                                                                Funções
###############################################################################################################################################################################################################
def Tema():
    #CURRENT_THEME = "blue"
    IS_DARK_THEME = True
    THEMES = [
        "light",
        "dark",
        "green",
        "blue",
    ]
    return IS_DARK_THEME, THEMES

# Funcao barra progresso
def ProgressoML():
    texto = st.empty()
    texto.markdown(f"<h2 style='text-align: center;'>Fazendo a previsão...  </h2>",
                unsafe_allow_html=True)
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1)    
    texto.empty()
    return my_bar

# Funcao barra progresso
def ProgressoDados():
    texto = st.empty()
    texto.markdown(f"<h2 style='text-align: center;'>Carregando dados...  </h2>",
                unsafe_allow_html=True)
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1)    
    texto.empty()
    return my_bar

#Acessando a API
@st.cache(show_spinner = False)
def Dados(startTime, endTime, magnitude_desejada):
    url = f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={startTime}&endtime={endTime}&minmagnitude={magnitude_desejada}&limit=20000'
    response = urllib.request.urlopen(url).read()
    data = json.loads(response.decode('utf-8'))
    return data

#Manipulando os dados
@st.cache(show_spinner = False)
def ManipulacaoDados(data):
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
    df = pd.DataFrame.from_dict(dicionario_geral)

    # Ajustando variáveis de data/tempo
    df.Timestamp = pd.to_datetime(df.Timestamp, unit='ms')
    df['Year'] = pd.to_datetime(df.Timestamp).dt.year
    df = df.sort_values(by=['Timestamp'], ascending=False)

    return df

def Previsao():
    df = pd.read_csv('earthquake-sample-predict.csv')

    cols =  ['Longitude', 'Profundidade']
    X = df.loc[:, cols].values
    y = df.loc[:, 'Magnitude'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)

    ss = StandardScaler()
    X_stand_train = ss.fit_transform(X_train)
    X_stand_test = ss.transform(X_test)

    ProgressoML().empty()

    regressor = RandomForestRegressor()

    regressor.fit(X_stand_train, y_train)
    y_pred = regressor.predict(X_stand_test)
    return X_stand_train, X_stand_test, y_train, y_test, y_pred, regressor

    # loading model exported
    # model = joblib.load('regressorModel')
    # score = model.score(long, profun)
    # new_array = np.array([long, profun]).reshape(-1, 2)
    # return model.predict(new_array), score

# Funcao metricas
def Metricas(mse, r2):
    col1, col2 = st.columns(2)
    col1.metric("R²", round(r2, 2))
    col2.metric("MSE", round(mse, 2))

# Funcao plotar mapa 
def Mapa(regiao, df):
    if df.shape[0] !=0:
        mapa = px.scatter_geo(data_frame=df, lat="Latitude", lon="Longitude", color="Magnitude", size=df.Magnitude**10, size_max=60,
                            projection=projecoes, color_continuous_scale=['#04290d', 'yellow', 'red'],
                            animation_frame=(None if visualizacaoPeriodo == 'Não' else 'Year'), scope=regiao, width=900, height=600)
        # Fazendo com que as fronteiras aparecam
        mapa.update_geos(showcountries=True)
        if regiao == 'world':
            # Ajustando rotacao do globo
            mapa.layout.geo.projection = {'rotation': {'lon': 200}, 'type': projecoes}
    else:
        mapa = st.warning('Não existem dados para os filtros aplicados')
        mapa = go.Figure()
    return mapa

###############################################################################################################################################################################################################
#                                                                                                Streamlit
###############################################################################################################################################################################################################
Tema()
st.set_page_config(layout="wide", initial_sidebar_state='expanded', page_icon = '🌎', page_title = 'Observatório sismológico')
st.sidebar.markdown("<h1 style='text-align: center;'>Filtros de pesquisa</h1>", unsafe_allow_html=True)
projeto = st.sidebar.selectbox('Projeto', ('Documentação', 'Mapas', 'Previsão'))

# Pagina documentacao
if projeto == 'Documentação':
    st.markdown("<h1 style='text-align: center;'>Observatório sismológico</h1>", unsafe_allow_html=True)
    st.image("https://i.ibb.co/4tnS9bb/imagem-terremoto-lisboa.png", caption = 'Ilustração da cidade de Lisboa após o terremoto em 1755')

    # Dividindo a pagina em tres colunas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<p align='justify';'>
               Os fenômenos naturais que se originam por meio de tremores terrestre ocorrem desde o início do planeta. Desde então a humanidade sofria com as consequências de tais fenômenos, dos quais são capazes de causar mortes, mudar paisagens e diversos outros fatores. Entretanto, os terremotos começaram a ser analisados cientificamente apenas após o terremoto que devastou Lisboa, em 1755. Considerado um dos terremotos mais fortes que atingiu a Europa, e segundo os sismólogos modernos, o tremor foi capaz de atingir uma magnitude de 9 na escala Richter, do qual gerou um tsunami e por fim tirou a vida de certa de 100 mil pessoas. Uma das consequências desse forte terremoto foi o interesse da ciência sobre a sismologia, ciência da qual era pouco explorada até a época. </p>""",
                unsafe_allow_html=True)

    with col2:
        st.markdown("""<p align='justify';'>
            A sismologia visa o estudo dos sismos (ou terremotos) e, genericamente, dos diversos movimentos que ocorrem na superfície do globo terrestre. Esta ciência busca conhecer e determinar em que circunstâncias ocorrem os sismos naturais assim como suas causas, de modo a prevê-los em tempo e espaço. Portanto, por meio dessa ciência, é possível analisar dados gerados de diversos observatórios sismológicos e sensores sismógrafos a fim de entender os tremores terrestres, as causas e impactos diretos na sociedade, havendo até a possibilidade de prevê-los em alguns casos dependendo dos dados gerados. Dessa forma, o observatório tenta auxiliar na visualização e predição da magnitude dos sismos atráves de modelos estatísticos e robustos métodos computacionais.</p>""",
            unsafe_allow_html=True)
        
    with col3:
        st.markdown("""<p align='justify';'>
                A referência mundial em relação ao monitoramento global de tremores terrestre acontece por meio do Serviço Geológico dos Estados Unidos (USGS). Dessa forma, no site é disponibilizado uma API pública para a consulta dos dados, do qual pode ser acessada por diversas formas. Portanto, o observatório sismológico faz a consulta dos dados de acordo com os filtros aplicado. Vale ressaltar que existe um limite de 20.000 dados por requisição, caso os filtros excedam esse limite, são coletados apenas os primeiros 20.000 sismos referente as datas escolhidas. Para a melhor visualização e coleta dos dados referentes aos terremotos, foi fixado o limite de terremotos com magnitude mínima igual a 4 graus na escala Ritcher, não sendo possível visualizar sismos menores.</p>""",
                unsafe_allow_html=True)

    st.markdown("""<p align='justify'; font-size:10px '><br><br><br>Documentação oficial e código-fonte do observatório sismológico:  <a href='https://github.com/victoresende19/earthquakes'>Observatório sismológico repositório</a> </p>""",
    unsafe_allow_html=True)

    st.markdown("""<p align='justify'; font-size:10px '>Victor Resende &trade;<br>Brazil - 2022 </p>""", unsafe_allow_html=True)
    
# Pagina mapas
elif projeto == 'Mapas':

    my_date = datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))

    # Filtros
    form = st.sidebar.form(key='my_form')
    startTime = form.date_input("Data inicial (ano/mês/dia):", datetime.date(2020, 1, 1), min_value = datetime.date(1960, 1, 1))
    endTime = form.date_input("Data final (ano/mês/dia):", datetime.datetime.now(pytz.timezone('America/Sao_Paulo')))
    magMinima = 4
    magnitude_desejada = form.slider('Magnitude mínima:', magMinima, 10, 5)
    paginaContinentes = form.selectbox('Selecione a região de pesquisa', [ 'world', 'africa', 'north america', 'south america', 'asia', 'europe'])
    visualizacaoTremor = form.selectbox('Tipo de tremor:', ('Terremoto', 'Explosão', 'Explosão Nuclear', 'Explosão de rochas', 'Explosão de pedreira'))
    visualizacaoPeriodo = form.selectbox('Visualização por ano:', ('Não', 'Sim'))
    projecoes = form.selectbox('Tipo de projeção:',
        ('natural earth', 'mercator', 'equirectangular', 'orthographic', 'kavrayskiy7', 'miller', 'robinson', 'eckert4', 'azimuthal equal area', 'azimuthal equidistant', 'conic equal area',
        'conic conformal', 'conic equidistant', 'gnomonic', 'stereographic', 'mollweide', 'hammer', 'transverse mercator', 'albers usa', 'winkel tripel', 'aitoff', 'sinusoidal')) 
    submit_button = form.form_submit_button(label='Aplicar filtros')
    
    data = Dados(startTime, endTime, magnitude_desejada)
    df = ManipulacaoDados(data)
    ProgressoDados().empty()

    # Variável Tipo
    mapping_tipo = {"Tipo": {'earthquake': 'Terremoto', 'explosion': 'Explosão', 'nuclear explosion':
                            'Explosão Nuclear', 'rock burst': 'Explosão de rochas', 'quarry blast': 'Explosão de pedreira'}}
    df = df.replace(mapping_tipo)
    df = df[df.Tipo == visualizacaoTremor]


    # Demonstração dos gráficos após os inputs
    dataInicio = startTime.strftime("%d/%m/%Y")
    dataFim = endTime.strftime("%d/%m/%Y")

    # Título da pagina
    st.markdown("<h1 style='text-align: center;'>Observatório sismológico</h1>", unsafe_allow_html=True)

    # Data utilizada
    st.markdown(f"<h4 style='text-align: center; font-size:16px'>{dataInicio} a {dataFim}</h4>", unsafe_allow_html=True)
    
    # Mapa
    st.plotly_chart(Mapa(paginaContinentes, df), use_container_width=True)

    # Volume dos dados
    st.markdown(f"<h4 style='text-align: center; font-size:16px'>Quantidade de terremotos: {df.shape[0]}</h4>", unsafe_allow_html=True)

    # Observacoes
    st.markdown(f"<p style='text-align: left; font-size:16px; color:red'><strong>Observação (1):</strong> Caso o range de data escolhido tenha mais de 20.000 dados, esse é o limite que será utilizado no gráfico.</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: left; font-size:16px; color:red'> <strong>Observação (2):</strong> A quantidade de dados pesquisados pode afetar no tempo de execução da visualização.</p>", unsafe_allow_html=True)

# Pagina previsao
elif projeto == 'Previsão':

    # startTime =  datetime.date(2015, 1, 1).strftime("%d/%m/%Y")
    # endTime =  datetime.date(2022, 6, 10).strftime("%d/%m/%Y")

    st.markdown("<h1 style='text-align: center; color: black;'>Previsão de terremotos</h1>", unsafe_allow_html=True) 
    st.markdown("<p style='text-align: left; color: black;'>Como exposto por Geller (1997),  terremotos são desastres praticamente impossíveis de se prever dada sua natureza incerta. Entretanto, Mondol (2021) apresenta um estudo sobre variáveis e métodos para previsão da magnitude de um terremoto. Nesse último, o algoritmo de floresta aleatória obteve resultados interessantes quando alimentado por dados sobre profundidade dos terremotos.  </p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: left; color: black;'>Portanto, ao verificar a correlação e a literatura, decidiu-se que as variáveis de longitude e profundidade do epicentro (em km) são as que possuem melhor resultado na predição de um tremor. Dessa forma, o modelo utilizado para tal chama-se <strong>floresta aleatória</strong>, um método não-linear do qual utiliza um agregado de árvores de decisão para assim prever a magnitude do terremoto. Abaixo estão disponibilizados os filtros citado para fazer a previsão da magnitude do terremoto.</p>", unsafe_allow_html=True)

    # Filtros
    col1, col2= st.columns(2)
    with col1:
        # Longitude
        form1 = st.form(key='my_form1')
        Longitude = form1.slider('Longitude: ', min_value = -174.0, max_value = 174.0, value = 142.0)
        submit_button = form1.form_submit_button(label='Aplicar filtros')
    
    with col2:
        # Profundidade
        form2 = st.form(key='my_form2')
        Profundidade = form2.slider('Profundidade: ', min_value = 5.0, max_value = 200.0, value = 15.0)
        submit_button = form2.form_submit_button(label='Aplicar filtros')

    st.markdown(f"<p style='text-align: left; color: red;'><strong>Observação (1)</strong>: A previsão é realizada de acordo com os dados do período de 10/06/2010 a 01/01/2015</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: left; color: red;'><strong>Observação (2)</strong>: Ao aplicar os filtros a floresta aleatória é ativada e a magnitude do terremoto predita.</p>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: left; color: black;'>Caso a longitude em que o terremoto ocorra seja {Longitude} e o epicentro tenha profundidade de {Profundidade} km, quão alta a magnitude deste tremor seria?</h4>", unsafe_allow_html=True) 

    # ProgressoDados().empty()
    # data = Dados(startTime, endTime, magnitude_desejada = 2)
    # df = ManipulacaoDados(data)

    # Modelo
    X_stand_train, X_stand_test, y_train, y_test, y_pred, regressor = Previsao()
    previsao = np.array([Longitude, Profundidade]).reshape(-1, 2)

    # R2
    score_stand_ran = regressor.score(X_stand_test, y_test)
    # MSE
    mse = mean_squared_error(y_test, y_pred)

    #st.markdown(f"<h4 style='text-align: left; color: black;'>Previsão da magnitude: {round(previsao[0], 2)} graus na escala Ritcher </h4>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: left; color: black;'>Previsão da magnitude: {round(regressor.predict(previsao)[0], 2)} graus na escala Ritcher </h4>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: left; color: black;'>As métricas utilizadas para a avaliação da floresta aleatória são o R², ou coeficiente de determinação, do qual demonstra quão explicativo o modelo é, variando entre 0 a 1. Já o MSE, ou erro médio quadrático, representa os erros associados de cada observação treinada em relação ao valor predito. </p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: left; color: black;'><strong>R²</strong>: {round(score_stand_ran, 2)} </p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: left; color: black;'><strong>MSE</strong>: {round(mse, 2)} </p>", unsafe_allow_html=True)

    st.markdown(f"<p style='text-align: left; color: black;'><br><br><strong>Referências</strong> </p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: left; color: black;'><a href='http://essay.utwente.nl/87313/'>[1] Manaswi Mondol. Analysis and prediction of earthquakes using different machine learning techniques. B.S. thesis, University of Twente, 2021.</a> </p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: left; color: black;'><a href='https://www.scec.org/publication/404'>[2] Robert J Geller, David D Jackson, Yan Y Kagan, and Francesco Mulargia. Earthquakes cannot be predicted. Science, 275(5306):1616–1616, 1997</a> </p>", unsafe_allow_html=True)