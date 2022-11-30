import streamlit as st
from sys import setprofile
import pandas as pd
import plotly as py
import plotly.figure_factory as ff
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import time
import requests
import streamlit as st
import seaborn as sns 
import streamlit.components.v1 as components
import pickle


# Configuramos la app y todos los dataframes
st.set_page_config(page_title='Automóviles eléctricos', page_icon='🚘', layout='wide',  initial_sidebar_state="collapsed")
data = pd.read_csv ('evdataset.csv')
data['Range Cold Weather'] = (data['City - Cold Weather']+data['Highway - Cold Weather']+data['Combined - Cold Weather'])/3
data['Range Hot Weather'] = (data['City - Mild Weather']+data['Highway - Mild Weather']+data['Combined - Mild Weather'])/3
df = pd.read_csv ('df.csv')
df2 = df
X, y = df2.loc[:, ~df.columns.isin(['Range Cold Weather'])], df.loc[:, 'Range Cold Weather']
X = X.drop(columns=['Range Hot Weather'])
st.markdown("<h1 style='text-align: center; color: darkblue;'>Automóviles eléctricos</h1>", unsafe_allow_html=True)
st.markdown(
   f” ” ”
   <style>
   p {
   background-image: url(‘https://www.juansola.com/1396-large_default/cartulina-50x65-verde-claro-180-gr.jpg’);
   }
   </style>
   ”””,
   unsafe_allow_html=True)

#----------------CONFIRGURACIÓN PAG...................
sns.set()
st.set_option('deprecation.showPyplotGlobalUse', False)
col1, col2 = st.columns(2)
with col1:
    st.image ('https://www.ecitycharge.com/wp-content/uploads/2021/05/car-ecity-miny.gif',width=350)
    st.caption ('Gif obtenido de: https://www.ecitycharge.com/wp-content/uploads/2021/05/car-ecity-miny.gif')
with col2:
    st.markdown("<h3 style='text-align: center; color: black;'>Contexto</h1>", unsafe_allow_html=True)
    st.write('El mundo de los vehículos está en cambio constante, este cambio se está dando para optimizar todos los aspectos que pueden ofrecer tanto al cliente como al planeta. De esta forma los clientes cada vez tendrán más ventajas con las nuevas tecnologías y a su vez el planeta no se verá tan perjudicado por los combustibles fósiles.')
    st.write('En este caso, vamos a analizar esta nueva tendencia de los vehículos eléctricos, contamos con un dataset de 194 vehículos donde se muestran sus características. A continuación podremos ver cuáles son las empresas que más fabrican este tipo de automóviles y que carácterísticas tienen.')
    st.write('También hemos realizado un modelo predictivo en el que podremos saber la autonomía (tanto en un clima frío como en uno cálido) de cualquier vehículo introduciendo los parámetros que nos interesen.')

#Uso de regresiones lineales

frio = pickle.load(open('Frio.pkl', 'rb'))
caliente = pickle.load(open('Caliente.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl','rb'))
sca = pickle.load(open('hot.pkl','rb'))



#first defined how much columns we need
col1, col2,  = st.columns(2)

Make = st.sidebar.selectbox(label = 'Marca', options = ([ 'Genesis', 'Mercedes', 'Porsche', 'BMW', 'Volkswagen', 'CUPRA','Skoda', 'MG', 'Volvo', 'Fiat', 'Smart', 'Hyundai', 'Peugeot','Citroen', 'Audi', 'Polestar', 'Toyota', 'Kia', 'DS', 'Ford','Honda', 'JAC', 'Nissan', 'Renault', 'Opel', 'Hongqi', 'Lexus','Dacia', 'Mazda', 'Seres', 'Tesla', 'Jaguar', 'Mini', 'Subaru']))
Aceleracion = st.sidebar.slider(label = "Aceleración (0-100 km/h) en segundos", min_value =1.5, max_value = 25.0 , value = 1.5, step = 0.1)
Velocidad = st.sidebar.slider(label = 'Velocidad máxima (km/h)', min_value =120, max_value = 270 , value = 120, step = 5)
Autonomia = st.sidebar.slider(label = 'Autonomía según fabricante (kms)', min_value =100, max_value = 700 , value = 100, step = 10)
Autmaxv = st.sidebar.slider(label = 'Potencia eléctrica (KW)', min_value =30, max_value = 560 , value = 30, step = 10)
Potencia = st.sidebar.slider(label = 'Potencia del motor (HP)', min_value =125, max_value = 1100 , value = 125, step = 15)
Traccion = st.sidebar.selectbox(label = 'Tracción', options = ['Delantera', 'Trasera', '4X4'])
carga = st.sidebar.slider(label = 'Capacidad de carga (KW)', min_value =23, max_value = 120 , value = 23, step = 1)
potcarga = st.sidebar.slider(label = 'Potencia de carga (KW)', min_value = 6.0, max_value = 24.0 , value = 6.0, step = 0.5)
aut1 = st.sidebar.slider(label = 'Autonomía tras una hora de carga (kms)', min_value = 20.0, max_value = 120.0 , value = 20.0, step = 0.5)
aut1r = st.sidebar.slider(label = 'Autonomía tras una hora de carga rápida (kms)', min_value = 150, max_value = 1120 , value = 150, step = 20)
Lenght = st.sidebar.slider(label = 'Longitud (cms)', min_value = 3500, max_value = 5391 , value = 3500, step = 10)
Width = st.sidebar.slider(label = 'Anchura (cms)', min_value = 1600, max_value = 2020 , value = 1600, step = 10)
Height = st.sidebar.slider(label = 'Altura (cms)', min_value = 1350, max_value = 1930 , value = 1350, step = 10)
Wheelbase = st.sidebar.slider(label = 'Distancia entre ejes (cms)', min_value = 2300, max_value = 3450 , value = 2300, step = 10)
GVWr = st.sidebar.slider(label = 'Peso bruto (kgs)', min_value = 1100, max_value = 3500 , value = 1100, step = 10)
Maxcargo = st.sidebar.slider(label = 'Carga máxima (kgs)', min_value = 245, max_value = 1121 , value = 245, step = 5)
volcargo = st.sidebar.slider(label = 'Volumen de carga (cms2)', min_value = 170, max_value = 1410 , value = 170, step = 10)
Seats = st.sidebar.selectbox(label = 'Nº asientos', options = ['2', '3','4','5','6','7','8','9','10'])

#Diccionarios para volver a formato texto
Dicc = { 'Genesis':1, 'Mercedes': 2, 'Porsche': 3, 'BMW': 4, 'Volkswagen': 5,'CUPRA': 6, 'Skoda': 7, 'MG': 8, 'Volvo': 9, 'Fiat':10, 'Smart':11, 'Hyundai':12, 'Peugeot':13, 'Citroen':14, 'Audi':15, 'Polestar':16, 'Toyota':17, 'Kia':18, 'DS':19, 'Ford':20, 'Honda':21, 'JAC':22, 'Nissan':23, 'Renault':24, 'Opel':25, 'Hongqi':26, 'Lexus':27, 'Dacia':28, 'Mazda':29, 'Seres':30, 'Tesla':31, 'Jaguar':32, 'Mini':33, 'Subaru':34}
Make = Dicc[Make]

Dicc1 = {'Delantera':1,'Trasera':2,'4X4':3}
Traccion = Dicc1[Traccion]


# -------------METEMOS LAS TABLAS QUE COMPONEN LAS CELDAS----------------
tabs = st.tabs(['Datos','Marcas','Tipo de tracción','Tipo de clima','Predicción clima frío','Predicción clima cálido'])
tab_plots= tabs[0]
with tab_plots:
    st.write('En nuestro Dataset inicial contamos con 27 columnas y ningún dato nulo.')
    st.markdown("<h3 style='text-align: center; color: black;'>Analizamos las variables</h1>", unsafe_allow_html=True)
    dfnuevo = pd.read_csv('dfnuevo.csv')
    dfnuevo
    st.write('*Consideramos clima frío con una temperatura de -10ºc y clima cálido con una temperatura de 23ºc.')
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Dataset inicial')
        pers = pd.read_csv('pers.csv')
        pers
    with col2:
        st.subheader('Dataset final')
        pers1 = pd.read_csv('pers1.csv')
        pers1
    st.markdown("<h3 style='text-align: center; color: black;'>Correlación</h1>", unsafe_allow_html=True)
    st.image("cor.png",width=1000)
tab_plots= tabs[1]
with tab_plots:
    st.write('Contamos con 34 marcas de vehículos diferentes.')
    st.markdown("<h3 style='text-align: center; color: black;'>Analizamos las marcas</h1>", unsafe_allow_html=True)
    st.image("ma.png",width=1000)
    st.subheader('Media de autonomía según la marca')
    p = open("me.html")
    components.html(p.read(),height=500,width=1000) 
tab_plots= tabs[2]
with tab_plots:
    st.write('Como hemos visto anteriormente, existen tres tipos de tracción, la delantera, la tasera y la tracción a las cuatro ruedas.')
    st.markdown("<h3 style='text-align: center; color: black;'>Tracción</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.write('Porcentaje de vehículos según su tracción')
        p = open("trac.html")
        components.html(p.read(),height=400,width=400) 
    with col2:
        st.write('Cantidad de vehículos por marca y tracción')
        st.image("matt.png",width=800)
    st.markdown("<h3 style='text-align: center; color: black;'>Tracción y autonomía</h1>", unsafe_allow_html=True)
    p = open("auton.html")
    components.html(p.read(),height=400,width=1520) 
tab_plots= tabs[3]
with tab_plots:
    st.write('A continuación vamos a analizar la diferencia entre los climas fríos y los cálidos en cuanto a la autonomía.')
    col1, col2 = st.columns(2)
    with col1:
        st.image("frio.png",width=550)
    with col2:
        st.image('caliente.png',width=550)
    col1, col2, col3 = st.columns(3)
    with col2:
        st.image('difr.png',width=550)
tab_plots= tabs[4]
with tab_plots:
    st.markdown("<h3 style='text-align: center; color: black;'>¿Cuántos kms de autonomía tendrá el vehículo en un clima frío?</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Predicción')
        st.write('Abra el panel desplegable de la izquierda y seleccione las características de un vehículo.')
        features = {'Make': Make, 'Acceleration_0_-_100_km/h': Aceleracion, 'Top_Speed': Velocidad, 'Electric_Range': Autonomia, 'Total_Power': Autmaxv, 'Total_Torque': Potencia, 'Drive': Traccion, 'Battery_Capacity': carga, 'Charge_Power': potcarga, 'Charge_Speed': aut1, 'Fastcharge_Speed': aut1r, 'Length': Lenght, 'Width': Width, 'Height': Height, 'Wheelbase':Wheelbase, 'Gross_Vehicle_Weight_(GVWR)': GVWr, 'Max._Payload': Maxcargo, 'Cargo_Volume': volcargo, 'Seats': Seats}
        dflis = pd.DataFrame(features, index = [0])
        features_df  = pd.DataFrame([features])
        if st.button('Autonomía en clima frío'):     
            st.write("Tu coche tendrá una autonomía de  {:.2f} kms.".format(float(frio.predict(scaler.transform(dflis))) ))

    with col2:
        st.image ('https://media.tenor.com/GZigPBjX2ysAAAAC/old-town-road-car.gif')
        st.caption ('Gif obtenido de: https://media.tenor.com/GZigPBjX2ysAAAAC/old-town-road-car.gif') 
tab_plots= tabs[5]
with tab_plots:
    st.markdown("<h3 style='text-align: center; color: black;'>¿Cuántos kms de autonomía tendrá el vehículo en un clima cálido?</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Predicción')
        st.write('Abra el panel desplegable de la izquierda y seleccione las características de un vehículo.')

        features = {'Make': Make, 'Acceleration_0_-_100_km/h': Aceleracion, 'Top_Speed': Velocidad, 'Electric_Range': Autonomia, 'Total_Power': Autmaxv, 'Total_Torque': Potencia, 'Drive': Traccion, 'Battery_Capacity': carga, 'Charge_Power': potcarga, 'Charge_Speed': aut1, 'Fastcharge_Speed': aut1r, 'Length': Lenght, 'Width': Width, 'Height': Height, 'Wheelbase':Wheelbase, 'Gross_Vehicle_Weight_(GVWR)': GVWr, 'Max._Payload': Maxcargo, 'Cargo_Volume': volcargo, 'Seats': Seats}
        df = pd.DataFrame(features, index = [0])      
        features_df  = pd.DataFrame([features])
        if st.button('Autonomía en clima cálido'):    
            st.write("Tu coche tendrá una autonomía de  {:.2f} kms.".format(float(caliente.predict(sca.transform(dflis))) ))
    with col2:
        st.image ('https://media.tenor.com/tIWFMoqxTL4AAAAC/hennessy-venom.gif')
        st.caption ('Gif obtenido de: https://media.tenor.com/tIWFMoqxTL4AAAAC/hennessy-venom.gif')
