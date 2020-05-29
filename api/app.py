from flask import Flask
from flask import jsonify, json
from flask import request
from flask_cors import CORS, cross_origin
import numpy as numpy
import cv2
from resources import *
from PIL import Image
import io
import base64 
import re
import pandas as pd
import threading
import time

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

modelo = ''

def stringToImage(base64_string):
    imgdata = base64.b64decode(base64_string)
    img = Image.open(io.BytesIO(imgdata))
    return np.array(img)

def INICIO():
    '''
    Función que permite que se cargue el modelo
    '''
    global modelo
    modelo=CargarModelo()
    print('Se cargó el modelo')

@app.before_first_request
def activate_job():
    thread = threading.Thread(target=INICIO)
    thread.start()

@app.route('/', methods=['GET'])
def index():
    return 'Welcome'

@app.route('/prueba', methods=['GET'])
def prueba():
    return jsonify({'respuesta':'prueba'})

@app.route('/imagen', methods=['GET','POST'])
def imagen():
    '''Obtiene como parámetro una imagen como un string base 64,
        se obtiene la imagen, esta se procesa y entra al modelo 
        para la clasificación
    '''
    if request.method=='POST':
        imagen = request.form['imagen']
        global modelo

        # Lectura de la imagen
        img = stringToImage(imagen.split(',')[1])
        img = process_image(img)

        # Pasamos la imagen al modelo
        probabilidades, clases = Predict(img,modelo)

        # Se obtiene como resultado un dataframe
        df = Process_results(probabilidades, clases)

        print('resultado obtenido')
        print(df)

        # Tomamos las clases y las probabilidades
        clases = df.index.values
        probabilidades = df['probabilidad'].values

        clases = list(map(int, clases))
        probabilidades = list(map(float, probabilidades))

        response = {'clases': clases, 'probabilidades': probabilidades}
        return jsonify(response)



@app.route('/resultado',methods=['GET','POST'])
def carga():
    '''Obtiene como parámetro una imagen como un archivo,
        se obtiene la imagen, esta se procesa y entra al modelo 
        para la clasificación
    '''
    if request.method=='POST':
        img = request.files['imagen']
        img = cv2.imdecode(numpy.fromstring(img.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
        global modelo

        img = process_image(img)
        # Pasamos la imagen al modelo
        probabilidades, clases = Predict(img,modelo)

        # Se obtiene como resultado un dataframe
        df = Process_results(probabilidades, clases)

        print('res obtenido')
        print(df)

        # Tomamos las clases y las probabilidades
        clases = df.index.values
        probabilidades = df['probabilidad'].values

        clases = list(map(int, clases))
        probabilidades = list(map(float, probabilidades))

        response = {'clases': clases, 'probabilidades': probabilidades}
        return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)