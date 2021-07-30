################################################## IMPORTACIONES #######################################################
import json
import os
import openpyxl
# LIBRERIA PARA REALIZAR LA MATRIZ DE BAG OF WORDS
from keras.preprocessing.text import Tokenizer

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

def BagOfWords(i):
    array_words = []

    # RECUPERAMOS LA URL DEL JSON
    url_creator = "./CORPUS-PREPROCESADO/" + i

    # ABRIMOS EL ARCHIVO JSON
    with open(url_creator, encoding="utf-8") as file:
        data = json.load(file)

    tamanio = len(data['trend'])
    # RECORREMOS EL JSON Y RECUPERAMOS EL ARREGLO DE WORDS Y EL IDENTIFICADOR DE LA LEY
    for aux in data['trend']:
        array_words.append(aux['tweet'])

    # REALIZAMOS EL FIT DE LAS PALABRAS DEL ARREGLO PREPROCESADO
    model = Tokenizer()
    model.fit_on_texts(array_words)

    # ARREGLO DE PALABRAS PREPROCESADAS
    keys = list(model.word_index.keys())

    # REALIZAMOS LA MATRIZ DE BAG OF WORDS
    rep = model.texts_to_matrix(array_words, mode='count')

    return rep, keys, array_words, tamanio

def ExcelTfIdf(nombre, rep, keys, array_words, tamanio):

    # AGREGAR MATRIZ PARA TF
    matriz_tf = []

    # HABILITAMOS LA LIBRERIA QUE NOS PERMITE TRABAJAR CON UN ARCHIVO EXCEL
    wb = openpyxl.Workbook()
    hoja = wb.active

    # GENERAMOS LAS FILAS USANDO LA MATRIZ DE BAG OF WORDS
    filas = []
    for i in range(tamanio):
        aux = list(rep[i])
        del aux[0]

        tamanio_ley = len(array_words[i])

        for j in range(0, len(aux)):
            if aux[j] > 0: aux[j] = round(aux[j] / tamanio_ley, 2)

        # AGREGAR A LA MATRIZ TF
        #print(aux)
        matriz_tf.append(aux)
        fila = [i] + aux
        filas.append(fila)

    # CREAMOS LA FILA CON LOS ENCABEZADOS (ARRAY_WORDS)
    array = [''] + keys
    hoja.append(array)

    # print(keys)

    # AGREGAMOS LAS FILAS A NUESTRA HOJA DE EXCEL
    for producto in filas:
        # producto es una tupla con los valores de un producto
        hoja.append(producto)

    # REDIMENSIONAMOS EL ARCHIVO EXCEL
    for column_cells in hoja.columns:
        new_column_letter = (openpyxl.utils.get_column_letter(column_cells[0].column))
        hoja.column_dimensions[new_column_letter].width = 12
    print("excel redimensionado")

    # GUARDAMOS EL ARCHIVO EXCEL CREADO
    url_save = './EXCEL/' + str(nombre).replace(".json","") + ".xlsx"
    wb.save(url_save)

    return matriz_tf


def WordCloud(nombre, keys, tamanio, matriz_tf):
    # DICCIONARIO DE PALABRAS (TF) PARA LA NUBE DE PALABRAS

    print(keys)
    dic_ponderado = {}
    for i in range(0, len(keys)):
        contador = 0
        for j in range(0, tamanio):
            contador = contador + matriz_tf[j][i]
        dic_ponderado[str(keys[i])] = round(contador, 2)
    print("diccionario terminado")

    # ORDENAMOS DICCIONARIO DE PALABRAS PREPROCESADAS PARA PASARLO A UN EXCEL
    sorted_words = sorted(dic_ponderado.items(), key=lambda x: x[1], reverse=True)
    wb1 = openpyxl.Workbook()
    hoja1 = wb1.active
    for i in range(len(sorted_words)):
        fila = [sorted_words[i][0], sorted_words[i][1]]
        hoja1.append(fila)
    url_save = './EXCEL-TF/' + str(nombre).replace(".json","") + "-TF.xlsx"
    wb1.save(url_save)

    # NUMERO DE PALABRAS
    print(len(keys))

    # CREAMOS LA NUBE DE PALABRAS Y LA GUARDAMOS
    url_save_png = './NUBE DE PALABRAS/' + str(nombre).replace(".json","") + ".png"
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


CleanCarpet("EXCEL")
CleanCarpet("EXCEL-TF")
CleanCarpet("NUBE DE PALABRAS")

# LISTAR DIRECTORIOS DE NUESTRO CORPUS
trends_preprocesados = os.listdir('CORPUS-PREPROCESADO')

for i in trends_preprocesados:

    print(i)

    BOF = BagOfWords(i)

    TFIDF = ExcelTfIdf(i, BOF[0], BOF[1], BOF[2], BOF[3])

    #print(TFIDF)

    WordCloud(i, BOF[1], BOF[3], TFIDF)



