import os, re, json
################################################# CONVERTIR TXT A JSON #################################################

def Convert(topic):

    # RECUPERAMOS LA URL DEL JSON
    url_creator = "./CORPUS-PREPROCESADO-GRAFO/" + topic + ".json"

    # ABRIMOS EL ARCHIVO JSON
    with open(url_creator, encoding="utf-8") as file:
        data = json.load(file)

    oracion_array = []
    # CREAR ARRAY CON ORACIONES PREPROCESADAS
    for aux in data:
        array = aux['tweet_p']

        oracion = ""
        for word in array:
            oracion += word + " "

        oracion = oracion.strip() + "."
        oracion_array.append(oracion)

    # ESCRIBIR EN ARCHIVO TXT
    url = "TXT GRAPH/" + topic + ".txt"
    file = open(url, "w", encoding="utf-8")
    for oracion in oracion_array:
        file.write(oracion+'\n')
    file.close()

Convert("DEPORTE")

Convert("GENERAL")

Convert("POLITICA")
