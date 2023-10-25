from utils.model import previsao
from utils.map import mapa, regioes, projecoes_mapa
from utils.etl import coleta_dados, manipula_dados, tipo_eventos
import pytz
import datetime
import numpy as np
import streamlit as st

st.set_page_config(layout="wide", page_icon='🌎', page_title='SismoMap')
st.markdown("<h1 style='text-align: center; font-size:52px'>SismoMap</h1>",unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:16px'>Observatório sismológico</p>",unsafe_allow_html=True)
mapa_sismos, predict, doc = st.tabs(["Mapa", "Predição magnitude", "Documentação"])

with mapa_sismos:
    st.markdown("<h5 style='text-align: left;'>Caso deseje, aplique os filtros:</h5>",unsafe_allow_html=True)

    with st.form(key='my_form_map'):
        with st.expander("Filtros"):
            col1, col2 = st.columns(2)

            with col1:
                startTime = st.date_input("Data inicial (ano/mês/dia):", datetime.datetime.now(pytz.timezone('America/Sao_Paulo')))
                visualizacaoPeriodo = st.selectbox('Visualização por ano:', ('Não', 'Sim'))

            magMinima = 4
            magnitudeUsuario = st.slider('Magnitude mínima:', magMinima, 10, 5)

            with col2:
                endTime = st.date_input("Data final (ano/mês/dia):", datetime.date(2022, 1, 1), datetime.date(1960, 1, 1))
                visualizacaoTremor = st.selectbox('Tipo de tremor:', list(tipo_eventos.keys()))

        data = coleta_dados(endTime, startTime, magnitudeUsuario, visualizacaoTremor)
        terremotos = manipula_dados(data)
        submit_button = st.form_submit_button(label='Aplicar filtros')

    st.markdown(f"<h4 style='text-align: center; font-size:16px'>Terremotos ocorridos na data de {startTime.strftime('%d/%m/%Y')} a {endTime.strftime('%d/%m/%Y')}</h4>", unsafe_allow_html=True)

    if len(terremotos):
        st.plotly_chart(mapa(data=terremotos, visualizacaoPeriodo=visualizacaoPeriodo), use_container_width=True)
    else:
        st.warning('Não existem dados para os filtros aplicados')

    st.markdown(f"<h4 style='text-align: center; font-size:16px'>Quantidade de terremotos: {terremotos.shape[0]}</h4>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: left; font-size:16px; color:red'><strong>Observação (1):</strong> Apesar do range de dados escolhido, a aplicação considera apenas os 20.000 primeiros dados referente a data de início.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: left; font-size:16px; color:red'> <strong>Observação (2):</strong> A quantidade de dados pesquisados pode afetar no tempo de execução da visualização.</p>", unsafe_allow_html=True)


with predict:
    startTime = datetime.date(2021, 1, 1)
    endTime = datetime.date(2023, 1, 1)

    # st.markdown("<h1 style='text-align: center; color: black;'>Previsão magnitude de terremotos</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: justify; color: black;'>Como exposto por Geller (1997), terremotos são desastres praticamente impossíveis de se prever dada sua natureza incerta. Entretanto, Mondol (2021) apresenta um estudo sobre variáveis e métodos para previsão da magnitude de um terremoto. Nesse último, o algoritmo de floresta aleatória obteve resultados interessantes quando alimentado por dados sobre profundidade dos terremotos.  </p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: justify; color: black;'>Portanto, ao verificar a correlação e a literatura, decidiu-se que as variáveis de longitude e profundidade do epicentro (em km) são as que possuem melhor resultado na predição de um tremor. Dessa forma, o modelo utilizado para tal chama-se <strong>floresta aleatória</strong>, um método não-linear do qual utiliza um agregado de árvores de decisão para assim prever a magnitude do terremoto. Abaixo estão disponibilizados os filtros citado para fazer a previsão da magnitude do terremoto.</p>", unsafe_allow_html=True)
    st.write('')
    st.markdown("<h5 style='text-align: left;'>Caso deseje, aplique os filtros:</h5>", unsafe_allow_html=True)
    with st.form(key='my_form_predict'):
        col1, col2, col3 = st.columns(3)

        with col1:
            latitude = st.slider('Latitude: ', min_value=-90.0, max_value=180.0, value=90.0)

        with col2:
            longitude = st.slider('Longitude: ', min_value=-180.0, max_value=180.0, value=142.0)

        with col3:
            profundidade = st.slider('Profundidade: ', min_value=5.0, max_value=500.0, value=15.0)
            
        submit_button = st.form_submit_button(label='Aplicar filtros')

    st.markdown("<p style='text-align: left; color: red;'><strong>Observação (1)</strong>: A previsão é realizada com base em uma amostra representativa dos dados.</p>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: justify; color: black;'>Caso o terremoto ocorresse em uma latitude de {latitude}, longitude de {longitude}, e o epicentro estiver a uma profundidade de {profundidade} km, a magnitude estimada desse tremor seria: </h4>", unsafe_allow_html=True)
    previsao = previsao(latitude, longitude, profundidade)
    st.markdown(f"<h3 style='text-align: center; color: brown;'>{round(previsao[0], 2)} graus na escala Ritcher </h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: justify; color: black;'>A métrica utilizada para a avaliação da floresta aleatória foi o R², ou coeficiente de determinação, do qual demonstra quão explicativo o modelo é, variando entre 0 a 1. Como consta na documentação do projeto, o R² referente ao conjunto de dados utilizado como treinamento chegou a 0.72. Além disso, a métrica MAPE foi de 0.11, o que significa dizer que a precisão do modelo é cerca de 89% nas respectivas previsões.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: justify; color: black;'><br><br><strong>Referências</strong> </p>",unsafe_allow_html=True)
    st.markdown("<p style='text-align: justify; color: black;'><a href='http://essay.utwente.nl/87313/'>[1] Manaswi Mondol. Analysis and prediction of earthquakes using different machine learning techniques. B.S. thesis, University of Twente, 2021.</a> </p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: justify; color: black;'><a href='https://www.scec.org/publication/404'>[2] Robert J Geller, David D Jackson, Yan Y Kagan, and Francesco Mulargia. Earthquakes cannot be predicted. Science, 275(5306):1616–1616, 1997</a> </p>", unsafe_allow_html=True)


with doc:
    # st.markdown("<h1 style='text-align: center;'>Observatório sismológico</h1>", unsafe_allow_html=True)
    st.image("https://i.ibb.co/4tnS9bb/imagem-terremoto-lisboa.png", caption='Ilustração da cidade de Lisboa após o terremoto em 1755')

    doc1, doc2, doc3 = st.columns(3)
    with doc1:
        st.markdown("""<p align='justify';'> Os fenômenos naturais que se originam por meio de tremores terrestre ocorrem desde o início do planeta. Desde então a humanidade sofria com as consequências de tais fenômenos, dos quais são capazes de causar mortes, mudar paisagens e diversos outros fatores. Entretanto, os terremotos começaram a ser analisados cientificamente apenas após o terremoto que devastou Lisboa, em 1755. Considerado um dos terremotos mais fortes que atingiu a Europa, e segundo os sismólogos modernos, o tremor foi capaz de atingir uma magnitude de 9 na escala Richter, do qual gerou um tsunami e por fim tirou a vida de certa de 100 mil pessoas. Uma das consequências desse forte terremoto foi o interesse da ciência sobre a sismologia, ciência da qual era pouco explorada até a época. </p>""", unsafe_allow_html=True)

    with doc2:
        st.markdown("""<p align='justify';'> A sismologia visa o estudo dos sismos (ou terremotos) e, genericamente, dos diversos movimentos que ocorrem na superfície do globo terrestre. Esta ciência busca conhecer e determinar em que circunstâncias ocorrem os sismos naturais assim como suas causas, de modo a prevê-los em tempo e espaço. Portanto, por meio dessa ciência, é possível analisar dados gerados de diversos observatórios sismológicos e sensores sismógrafos a fim de entender os tremores terrestres, as causas e impactos diretos na sociedade, havendo até a possibilidade de prevê-los em alguns casos dependendo dos dados gerados. Dessa forma, o observatório tenta auxiliar na visualização e predição da magnitude dos sismos atráves de modelos estatísticos e robustos métodos computacionais.</p>""", unsafe_allow_html=True)

    with doc3:
        st.markdown("""<p align='justify';'>A referência mundial em relação ao monitoramento global de tremores terrestre acontece por meio do Serviço Geológico dos Estados Unidos (USGS). Dessa forma, no site é disponibilizado uma API pública para a consulta dos dados, do qual pode ser acessada por diversas formas. Portanto, o observatório sismológico faz a consulta dos dados de acordo com os filtros aplicado. Vale ressaltar que existe um limite de 20.000 dados por requisição, caso os filtros excedam esse limite, são coletados apenas os primeiros 20.000 sismos referente as datas escolhidas. Para a melhor visualização e coleta dos dados referentes aos terremotos, foi fixado o limite de terremotos com magnitude mínima igual a 4 graus na escala Ritcher, não sendo possível visualizar sismos menores.</p>""", unsafe_allow_html=True)
        st.markdown("""<p align='justify'; font-size:10px '><br><br><br>Documentação oficial e código-fonte do observatório sismológico:  <a href='https://github.com/victoresende19/earthquakes'>Observatório sismológico repositório</a> </p>""", unsafe_allow_html=True)
        st.markdown("""<p align='justify'; font-size:10px '>Victor Resende &trade;<br>Brazil - 2022 </p>""",unsafe_allow_html=True)
