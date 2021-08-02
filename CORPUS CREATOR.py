import twint
import json
import shutil, os
import pandas as pd

#
def TrendCorpusCreator(trend):

    url = "./CORPUS/" + trend.upper() + ".json"

    c = twint.Config()
    c.Limit = 10
    c.Lang = "es"
    c.Search = trend
    c.Near = "Perú"
    c.Since = "2021-08-01"
    c.Store_json = True
    c.Output = url
    c.Popular_tweets = True
    twint.run.Search(c)

def CleanCarpet():
    folder = 'CORPUS'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

# LIMPIAR CARPETA
CleanCarpet()

# RECUPERAMOS TRENS
v = pd.read_csv("TRENDS/TRENDS.csv")
trends = []
for i in range (v.shape[0]):
    trends.append(v.iloc[i,1])

# CREAMOS EL CORPUS DE CADA TREND
for i in trends:
    TrendCorpusCreator(str(i))






