###############################################################################################################################################################################################################
#                                                                                               Bibliotecas
###############################################################################################################################################################################################################
import streamlit as st

import pandas as pd
import numpy as np

import datetime
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

#Acessando a API
@st.cache(show_spinner = False)
def Dados(startTime, endTime, magnitude_desejada):
    url = f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={startTime}&endtime={endTime}&minmagnitude={magnitude_desejada}&limit=20000'
    response = urllib.request.urlopen(url).read()
    data = json.loads(response.decode('utf-8'))
    return data

def Previsao(df):
    cols =  ['Longitude', 'Profundidade']
    X = df.loc[:, cols].values
    y = df.loc[:, 'Magnitude'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)

    ss = StandardScaler()
    X_stand_train = ss.fit_transform(X_train)
    X_stand_test = ss.transform(X_test)

    regressor = RandomForestRegressor()

    regressor.fit(X_stand_train, y_train)
    y_pred = regressor.predict(X_stand_test)

    return X_stand_train, X_stand_test, y_train, y_test, y_pred, regressor


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

# Funcao barra progresso
def ProgressoML():
    texto = st.empty()
    texto.markdown(f"<h2 style='text-align: center;'>Fazendo a previsão...  </h2>",
                unsafe_allow_html=True)
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1)    
    texto.empty()
    return my_bar

# Funcao barra progresso
def ProgressoDados():
    texto = st.empty()
    texto.markdown(f"<h2 style='text-align: center;'>Carregando os dados...  </h2>",
                unsafe_allow_html=True)
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1)    
    texto.empty()
    return my_bar

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
st.set_page_config(layout="wide", initial_sidebar_state='expanded')
st.sidebar.markdown("<h1 style='text-align: center;'>Filtros de pesquisa</h1>", unsafe_allow_html=True)
projeto = st.sidebar.selectbox('Projeto', ('Documentação', 'Mapas', 'Previsão'))

# Pagina documentacao
if projeto == 'Documentação':
    st.markdown("<h1 style='text-align: center;'>Observatório sismológico</h1>", unsafe_allow_html=True)
    st.image("https://i.ibb.co/gwyKVGQ/002-1-1.png", caption = 'Ilustração da cidade de Lisboa após o terremoto em 1755')

    # Dividindo a pagina em tres colunas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<p align='justify';'>
               Os fenômenos naturais que se originam por meio de tremores terrestre ocorrem desde o início do planeta. Desde então a humanidade sofria com as consequências de tais fenômenos, dos quais são capazes de mudar paisagens, clima, mortes e diversos outros fatores. Entretanto, os terremotos começaram a ser analisados cientificamente apenas após o terremoto que devastou Lisboa, em 1755. Considerado um dos terremotos mais fortes que atingiu a Europa, e segundo os sismólogos modernos, o tremor foi capaz de atingir uma magnitude de 9 na escala Richter, do qual gerou um tsunami e por fim tirou a vida de certa de 100 mil pessoas. Uma das consequências desse forte terremoto foi o interesse da ciência sobre a sismologia, ciência da qual era pouco explorada até a época. </p>""",
                unsafe_allow_html=True)
        st.markdown("""<p align='justify';'>
                A sismologia visa o estudo dos sismos (ou terremotos) e, genericamente, dos diversos movimentos que ocorrem na superfície do globo terrestre. Esta ciência busca conhecer e determinar em que circunstâncias ocorrem os sismos naturais assim como suas causas, de modo a prevê-los em tempo e espaço. Portanto, por meio dessa ciência, é possível analisar dados gerados de diversos observatórios sismológicos e sensores sismógrafos a fim de entender os tremores terrestres, as causas e impactos diretos na sociedade, havendo até a possibilidade de prevê-los em alguns casos dependendo dos dados gerados.</p>""",
                unsafe_allow_html=True)

    with col2:
        st.markdown("""<p align='justify';'>
                Com o passar dos anos e o avanço da tecnologia, houve a criação e implementação de sensores em locais com risco de desastres naturais para a verificação de riscos e coleta dos dados. Dessa forma, uma vasta quantidade de dados é gerada diariamente, principalmente quando há situações de tremores, seja em razão de terremotos, erupções, ou até mesmo de ações humanas como acontece em alguns tipos de explosões. Portanto, a criação de um observatório sobre tremores e a predição da magnitude de determinada vibração terrestre, dado a localidade (Por meio da latitude e longitude), torna-se interessante para o monitoramento de tais fenômenos.</p>""",
                unsafe_allow_html=True)
        st.markdown("""<p align='justify';'>
                A referência mundial em relação ao monitoramento global de tremores terrestre acontece por meio do Serviço Geológico dos Estados Unidos (USGS). Dessa forma, em seu site é disponibilizado uma API pública para a consulta dos dados, do qual pode ser acessada por diversas formas.</p>""",
                unsafe_allow_html=True)
        
    with col3:
        st.markdown("""<p align='justify';'>
                Esse projeto utiliza ferramentas de mineração, coleta, visualização dos dados, criação de modelos preditivos e implementação. Os dados utilizados nos mapas a seguir são oriundos de uma API disponibilizada pelo Serviço Geológico dos Estados Unidos (USGS). A etapa de coleta dos dados foi realizado por meio da linguagem de programação Python, da qual se arquitetou o tratamento dos dados para a extração das variáveis pertinentes. Da mesma forma, a etapa de visualização dos dados e implementação se desenvolveram por meio da linguagem Python.</p>""",
                unsafe_allow_html=True)
        st.markdown("""<p align='justify';'>
                Esse estudo utiliza dados da API pública citada em formato JSON, coletando dados de tremores que tiveram magnitude maior ou igual a 2. Vale ressaltar que a API possui um limite de apenas 20.000 registros por requisição. Consequentemente, será necessário fazer mais de uma consulta para coletar todos os dados do período citado na introdução.</p>""",
                unsafe_allow_html=True)
    
# Pagina mapas
elif projeto == 'Mapas':

    # Filtros
    form = st.sidebar.form(key='my_form')
    startTime = form.date_input("Data inicial (ano/mês/dia):", datetime.date(2021, 1, 1), min_value = datetime.date(1960, 1, 1))
    endTime = form.date_input("Data final (ano/mês/dia):", datetime.date(2022, 6, 10), min_value = datetime.date(1960, 1, 1))
    magMinima = 4
    magnitude_desejada = form.slider('Magnitude mínima:', magMinima, 10, 5)
    paginaContinentes = form.selectbox('Selecione a região de pesquisa', [ 'world', 'africa', 'north america', 'south america', 'asia', 'europe'])
    visualizacaoTremor = form.selectbox('Tipo de tremor:', ('Terremoto', 'Explosão', 'Explosão Nuclear', 'Explosão de rochas', 'Explosão de pedreira'))
    visualizacaoPeriodo = form.selectbox('Visualização por ano:', ('Não', 'Sim'))
    projecoes = form.selectbox('Tipo de projeção:',
        ('natural earth', 'mercator', 'equirectangular', 'orthographic', 'kavrayskiy7', 'miller', 'robinson', 'eckert4', 'azimuthal equal area', 'azimuthal equidistant', 'conic equal area',
        'conic conformal', 'conic equidistant', 'gnomonic', 'stereographic', 'mollweide', 'hammer', 'transverse mercator', 'albers usa', 'winkel tripel', 'aitoff', 'sinusoidal'))  
    submit_button = form.form_submit_button(label='Aplicar filtros')

    # Dados
    data = Dados(startTime, endTime, magnitude_desejada)
    df = ManipulacaoDados(data)

    # Variável Tipo
    mapping_tipo = {"Tipo": {'earthquake': 'Terremoto', 'explosion': 'Explosão', 'nuclear explosion':
                            'Explosão Nuclear', 'rock burst': 'Explosão de rochas', 'quarry blast': 'Explosão de pedreira'}}
    df = df.replace(mapping_tipo)
    df = df[df.Tipo == visualizacaoTremor]

    # Barra de progresso
    ProgressoDados().empty()

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
    st.markdown(f"<h4 style='text-align: center; font-size:16px'>Volume de dados pesquisados ({df.shape[0]})</h4>", unsafe_allow_html=True)

    # Observacoes
    st.markdown(f"<p style='text-align: center; font-size:16px; color:red'><strong>Observação (1):</strong> Caso o range de data escolhido tenha mais de 20.000 dados, esse é o limite que será utilizado no gráfico.</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size:16px; color:red'> <strong>Observação (2):</strong> A quantidade de dados pesquisados pode afetar no tempo de execução da visualização.</p>", unsafe_allow_html=True)

# Pagina previsao
elif projeto == 'Previsão':

    # Barra de progresso
    ProgressoDados().empty()
    st.markdown("<h1 style='text-align: center; color: black;'>Previsão de terremotos</h1>", unsafe_allow_html=True) 
    st.markdown("<h3 style='text-align: center; color: black;'>Longitude e Profundidade</h3>", unsafe_allow_html=True) 
    st.markdown("<p style='text-align: left; color: red;'><strong>Observação</strong>: Os dados serão coletados e o modelo treinado de acordo com os filtros escolhidos</p>", unsafe_allow_html=True)
    
    # Filtros
    col1, col2= st.columns(2)
    with col1:
        # Longitude
        form1 = st.form(key='my_form1')
        Longitude = form1.slider('Longitude: ', min_value = -174, max_value = 174, value = 142)
        submit_button = form1.form_submit_button(label='Aplicar filtros')
    
    with col2:
        # Profundidade
        form2 = st.form(key='my_form2')
        Profundidade = form2.slider('Profundidade: ', min_value = 10, max_value = 400, value = 53)
        submit_button = form2.form_submit_button(label='Aplicar filtros')

    # Dataframe
    ProgressoML().empty() # Barra de progresso
    startTime =  datetime.date(2021, 1, 1)
    endTime =  datetime.date(2022, 6, 10)
    data = Dados(startTime, endTime, magnitude_desejada = 2)
    df = ManipulacaoDados(data)

    # Modelo
    ProgressoML().empty() # Barra de progresso
    X_stand_train, X_stand_test, y_train, y_test, y_pred, regressor = Previsao(df)
    # R2
    score_stand_ran = regressor.score(X_stand_test, y_test)
    # MSE
    mse = mean_squared_error(y_test, y_pred)
    previsao = np.array([Longitude, Profundidade]).reshape(-1, 2)
    st.markdown(f"<h3 style='text-align: left; color: black;'>Previsão da magnitude: {round(regressor.predict(previsao)[0], 2)} graus na escala Ritcher </h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: left; color: black;'><strong>R²</strong>: {round(score_stand_ran, 2)} </p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: left; color: black;'><strong>MSE</strong>: {round(mse, 2)} </p>", unsafe_allow_html=True)