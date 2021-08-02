
import os
import shutil
import json

def CleanCarpet(folder):

    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

CleanCarpet("TRENDS-CSV")

import pandas as pd


# LISTAR DIRECTORIOS DE NUESTRO CORPUS
url_JSONs = os.listdir('CORPUS')

dicc = {}

for i in url_JSONs:

    name_trend = str(i).replace(".json","")

    url_preprocesado = "./CORPUS-PREPROCESADO/" + i
    with open(url_preprocesado, encoding="utf-8") as file:
        data = json.load(file)

    # RECORREMOS EL JSON DEL TREND Y UNIMOS LOS ARREGLOS DE PALABRAS PREPROCESADAS
    cont = 0
    tweets = []
    for aux in data['trend']:
        tweets = tweets + aux['tweet']

    tweets = list(set(tweets))
    #print(name_trend)
    #print(tweets)

    dicc[name_trend] = tweets

# GUARDAR DATA EN UN CSV
df = pd.DataFrame([[key, dicc[key]] for key in dicc.keys()], columns=['Name', 'WordsByTrend'])
df.to_csv('TRENDS-CSV/TRENDS-CSV.csv')