import os
import shutil
import json

def CleanCarpet():
    folder = 'CORPUS-CARPETAS'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)



# LIMPIAR CARPETA
shutil.rmtree("CORPUS-CARPETAS")

os.mkdir("CORPUS-CARPETAS")


# LISTAR DIRECTORIOS DE NUESTRO CORPUS
url_JSONs = os.listdir('CORPUS')


for i in url_JSONs:
    url = 'CORPUS-CARPETAS/' + str(i).replace(".json","")
    os.mkdir(url)

    url_preprocesado = "./CORPUS-PREPROCESADO/" + i
    with open(url_preprocesado, encoding="utf-8") as file:
        data = json.load(file)

    # RECORREMOS EL JSON Y RECUPERAMOS
    cont = 0
    for aux in data['trend']:
        cont += 1
        tweet = ""
        for word in aux["tweet"]:
            tweet = tweet + " " + word

        name = "T-" + str(cont)
        ruta = "./CORPUS-CARPETAS/" + str(i).replace(".json", "") + "/" + name + ".txt"

        file = open(ruta, "w", encoding="utf8")

        file.write(tweet)
