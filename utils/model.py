import joblib
import numpy as np
import streamlit as st

@st.cache_resource(show_spinner='Fazendo previsão...', max_entries=500)
def previsao(longitude: float, profundidade: float):
    """
    Description
    -----------
    Carrega o modelo RandomForestRegressor() treinado previamente
    para prever a magnitude de acordo com a Longitude e Profundidade
    do epicentro referente ao tremor escolhido pelo usuário.

    Treinamento realizado com dados de magnitude mínima 2 referente
    ao período de 2015 a 2023.

    Parameters
    ----------
    longitude: float
    latitude: float

    Returns
    -------
    Previsão do modelo.
    """

    model = joblib.load('random-forest-model')
    previsao = model.predict(np.array([longitude, profundidade]).reshape(-1, 2))
    return previsao
