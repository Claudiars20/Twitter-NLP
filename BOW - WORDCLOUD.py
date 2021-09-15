################################################## IMPORTACIONES #######################################################
import json
import os
import openpyxl
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

# LIBRERIA PARA REALIZAR NUBES DE PALABRAS
import stylecloud as sc

############################################## GENERAR BAG OF WORDS ####################################################

def CleanCarpet(folder):

    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

# MATRIZ DE TF_NORMALIZADO, GUARDA EN UN EXCEL  return matriz_tf, tamanio, keys
'''def TF_Normalizado(i,nombre):
    array_words = []

    # RECUPERAMOS LA URL DEL JSON
    url_creator = "./CORPUS-PREPROCESADO/" + i

    # ABRIMOS EL ARCHIVO JSON
    with open(url_creator, encoding="utf-8") as file: data = json.load(file)
    tamanio = len(data)

    # RECORREMOS EL JSON Y RECUPERAMOS EL ARREGLO DE WORDS Y EL IDENTIFICADOR DE LA LEY
    for aux in data: array_words.append(aux['tweet_p'])

    # REALIZAMOS EL FIT DE LAS PALABRAS DEL ARREGLO PREPROCESADO
    model = Tokenizer()
    model.fit_on_texts(array_words)

    keys = list(model.word_index.keys())

    # REALIZAMOS LA MATRIZ DE TF
    rep = model.texts_to_matrix(array_words, mode='count')


    ############################################################################

    # HABILITAMOS LA LIBRERIA QUE NOS PERMITE TRABAJAR CON UN ARCHIVO EXCEL
    wb = openpyxl.Workbook()
    hoja = wb.active

    # AGREGAR MATRIZ PARA TF
    matriz_tf = []

    # GENERAMOS LAS FILAS USANDO LA MATRIZ DE BAG OF WORDS
    filas = []
    for i in range(tamanio):
        aux = list(rep[i])
        del aux[0]

        tamanio_ley = len(array_words[i])

        for j in range(0, len(aux)):
            if aux[j] > 0: aux[j] = round(aux[j] / tamanio_ley, 2)

        # AGREGAR A LA MATRIZ TF
        # print(aux)
        matriz_tf.append(aux)
        fila = [i] + aux
        filas.append(fila)

    # CREAMOS LA FILA CON LOS ENCABEZADOS (ARRAY_WORDS)
    array = [''] + keys
    hoja.append(array)

    # AGREGAMOS LAS FILAS A NUESTRA HOJA DE EXCEL
    for producto in filas:
        # producto es una tupla con los valores de un producto
        hoja.append(producto)



    url_save = './MATRICES/TF-NORMALIZADO/' + str(nombre).replace(".json", "") + ".xlsx"
    wb.save(url_save)
    return matriz_tf, tamanio, keys'''

# MATRIZ DE TF_IDF, GUARDA EN UN EXCEL  return matriz_tf
def TF_IDF(i,nombre):
    array_words = []

    # RECUPERAMOS LA URL DEL JSON
    url_creator = "./CORPUS-PREPROCESADO/" + i

    # ABRIMOS EL ARCHIVO JSON
    with open(url_creator, encoding="utf-8") as file:
        data = json.load(file)
    tamanio = len(data)

    # RECORREMOS EL JSON Y RECUPERAMOS EL ARREGLO DE WORDS Y EL IDENTIFICADOR DE LA LEY
    for aux in data:
        array_words.append(aux['tweet_p'])

    # REALIZAMOS EL FIT DE LAS PALABRAS DEL ARREGLO PREPROCESADO
    vectorizer = TfidfVectorizer(preprocessor=lambda x: x, tokenizer=lambda x: x)
    X = vectorizer.fit_transform(array_words)

    keys = list(vectorizer.get_feature_names())

    # REALIZAMOS LA MATRIZ DE TF-IDF
    rep = X.toarray()

    ############################################################################

    # HABILITAMOS LA LIBRERIA QUE NOS PERMITE TRABAJAR CON UN ARCHIVO EXCEL
    wb = openpyxl.Workbook()
    hoja = wb.active

    # AGREGAR MATRIZ PARA TF
    matriz_tf = []

    # GENERAMOS LAS FILAS USANDO LA MATRIZ DE BAG OF WORDS
    filas = []
    for i in range(tamanio):
        aux = list(rep[i])
        # AGREGAR A LA MATRIZ TF-IDF

        matriz_tf.append(aux)
        fila = [i] + aux
        filas.append(fila)

    # CREAMOS LA FILA CON LOS ENCABEZADOS (ARRAY_WORDS)
    array = [''] + keys
    hoja.append(array)

    # AGREGAMOS LAS FILAS A NUESTRA HOJA DE EXCEL
    for producto in filas:
        hoja.append(producto)


    url_save = './MATRICES/TF-IDF/' + str(nombre).replace(".json", "") + ".xlsx"
    wb.save(url_save)
    return matriz_tf, tamanio, keys

def Ponderado_Wordcloud_TFN(nombre, keys, tamanio, matriz_tf):
    print(tamanio)
    dic_ponderado = {}
    for i in range(0, len(keys)):
        contador = 0
        for j in range(0, tamanio):
            contador = contador + matriz_tf[j][i]
        dic_ponderado[str(keys[i])] = round(contador, 2)

    # ORDENAMOS DICCIONARIO DE PALABRAS PREPROCESADAS PARA PASARLO A UN EXCEL
    sorted_words = sorted(dic_ponderado.items(), key=lambda x: x[1], reverse=True)

    df = pd.DataFrame([[i[0], i[1]] for i in sorted_words], columns=['Word', 'Ponderado'])

    url_save = './PONDERADO/TF-NORMALIZADO/' + str(nombre).replace(".json", "") + ".csv"
    df.to_csv(url_save)

    # NUMERO DE PALABRAS
    print(len(keys))

    # CREAMOS LA NUBE DE PALABRAS Y LA GUARDAMOS
    url_save_png = './NUBE DE PALABRAS/TF-NORMALIZADO/' + str(nombre).replace(".json", "") + ".png"
    sc.gen_stylecloud(
        text=dic_ponderado,
        colors=['#ecf0f1', '#3498db', '#e74c3c'],
        icon_name='fas fa-cloud',
        background_color='#1A1A1A',
        output_name=url_save_png,
        size=2048,
        max_words=350,
        max_font_size=400
    )

def Ponderado_Wordcloud_TFIDF(nombre, keys, tamanio, matriz_tf):

    dic_ponderado = {}
    for i in range(0, len(keys)):
        contador = 0
        for j in range(0, tamanio):
            contador = contador + matriz_tf[j][i]
        dic_ponderado[str(keys[i])] = round(contador, 2)

    # ORDENAMOS DICCIONARIO DE PALABRAS PREPROCESADAS PARA PASARLO A UN EXCEL
    sorted_words = sorted(dic_ponderado.items(), key=lambda x: x[1], reverse=True)

    df = pd.DataFrame([[i[0], i[1]] for i in sorted_words], columns=['Word', 'Ponderado'])

    url_save = './PONDERADO/TF-IDF/' + str(nombre).replace(".json", "") + ".csv"
    df.to_csv(url_save)

    # NUMERO DE PALABRAS
    print(len(keys))

    # CREAMOS LA NUBE DE PALABRAS Y LA GUARDAMOS
    url_save_png = './NUBE DE PALABRAS/TF-IDF/' + str(nombre).replace(".json", "") + ".png"
    sc.gen_stylecloud(
        text=dic_ponderado,
        colors=['#ecf0f1', '#3498db', '#e74c3c'],
        icon_name='fas fa-cloud',
        background_color='#1A1A1A',
        output_name=url_save_png,
        size=2048,
        max_words=350,
        max_font_size=400
    )

def Bow_All():


    # LISTAR DIRECTORIOS DE NUESTRO CORPUS
    trends_preprocesados = os.listdir('CORPUS-PREPROCESADO')

    for i in trends_preprocesados:
        print(i)

        #TF_N = TF_Normalizado(i, i)
        TF_IDFF = TF_IDF(i, i)

        #Ponderado_Wordcloud_TFN(i, TF_N[2], TF_N[1], TF_N[0])
        Ponderado_Wordcloud_TFIDF(i, TF_IDFF[2], TF_IDFF[1], TF_IDFF[0])




###################################################### SEPARADO ########################################################

# LIMPIAR CARPETAS
CleanCarpet("MATRICES/TF-IDF")
CleanCarpet("MATRICES/TF-NORMALIZADO")

CleanCarpet("NUBE DE PALABRAS/TF-IDF")
CleanCarpet("NUBE DE PALABRAS/TF-NORMALIZADO")

CleanCarpet("PONDERADO/TF-IDF")
CleanCarpet("PONDERADO/TF-NORMALIZADO")

# BOW DE TODAS LAS ACCOUNTS
Bow_All()





