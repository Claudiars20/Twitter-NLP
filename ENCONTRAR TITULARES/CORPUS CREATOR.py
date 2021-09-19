import twint
import json
import shutil, os
import pandas as pd
import re

from datetime import datetime
import pytz

################################################### SCRAPING TWITTER ###################################################

def Fecha():
    zona = 'America/Lima'
    timeZ_zona = pytz.timezone(zona)
    dt_zona = datetime.now(timeZ_zona)
    fecha_actual=dt_zona.strftime('%Y-%m-%d')
    return fecha_actual


def TrendCorpusCreator(name, account):

    url = "./CORPUS/" + name + ".json"
    c = twint.Config()
    c.Since = Fecha()

    c.Username = account
    c.Store_json = True
    c.Output = url
    twint.run.Search(c)

#################################################### ALMACENAMIENTO #####################################################



def CleanCarpet(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def Account_Dicctionary():
    df = pd.read_csv("CUENTAS DE TWITTER/CUENTAS.csv")
    dicc = {}
    for i in range(df.shape[0]):
        a = [df.iloc[i, 1], df.iloc[i, 2]]
        dicc[df.iloc[i, 0]] = a
    return dicc

# LIMPIAR CARPETA
CleanCarpet("CORPUS")


# RECUPERAMOS CUENTAS DE TWITTER EN UN DICCIONARIO
dicc = Account_Dicctionary()

# CREAMOS EL CORPUS DE CADA CUENTA
for key, value in dicc.items():

    account = re.sub(r'@', '', value[0])
    TrendCorpusCreator(key, account)

    print("\n================================" + key + "================================\n")








