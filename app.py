import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

# Carregue a logo da Uber
image = Image.open('uber-nova-logo-.jpg')

# Define a largura da página como widescreen
st.set_page_config(layout="wide")

# Cria duas colunas
col1, col2 = st.columns([2, 1])

# Título na primeira coluna
col1.title('Viagens de Uber em Nova York')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    def lowercase(x): return str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


data_load_state = st.text('Carregando dados...')
data = load_data(10000)
data_load_state.text("Pronto!")

if st.checkbox('Mostrar dados brutos'):
    st.subheader('Dados brutos')
    st.write(data)

# Logo da Uber na segunda coluna
col2.image(image, use_column_width=True)

# Exibe o primeiro gráfico na primeira coluna
st.subheader('Número de viagens por hora')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist_values, use_container_width=True)

hour_to_filter = st.slider('Hora', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

# Exibe o segundo gráfico na segunda coluna
st.subheader('Mapa de todas as viagens em %s:00' % hour_to_filter)
st.map(filtered_data, use_container_width=True)
