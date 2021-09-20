# Encontrar titulares - Twitter

## Orden de Ejecución
1. `CORPUS CREATOR.py`
2. `PREPROCESADO.py`
3. `BOW - WORDCLOUD.py`
4. `PONDERADO +.py`
5. `LDA.py`
6. `FIND TITULAR.py`

## Descripción de Archivos .py

- 📎 `CORPUS CREATOR.py`: Crea Corpus de tweets de un determinado día(hora peruana) a partir de las cuentas de twitter de noticiarios peruanos y mundiales, se encuentra en: 📁`CUENTAS DE TWITTER/CUENTAS.csv`. El Corpus creado se almacena en la carpeta 📁`CORPUS` en archivos .json.

- 📎 `PREPROCESADO.py`: Realiza el preprocesado de los tweets ubicados en 📁`CORPUS`, limpiando ruido y identificando keywords. El resultado de los keywords se encuentra en: 📁`CORPUS-PREPROCESADO`, en estos se almacenan las keywords, n° de retweets, n° de likes, url de la noticia de cada tweet en archivo .json.

- 📎 `BOW - WORDCLOUD.py`: Realiza el ponderado de los keywords ubicados en 📁`CORPUS-PREPROCESADO` usando TF-IDF, este resultado se encuentra en: 📁`MATRICES` en archivos .csv, y el resumen de este se encuentra en 📁`PONDERADO/PONDERADO TF-IDF`. Con el resultado de TF-IDF obtenemos nubes de palabras, el resultado se encuentra en: 📁`NUBE DE PALABRAS`.

- 📎 `PONDERADO +.py`: Este archivo es una mejora del ponderado obtenido en 📁`PONDERADO/PONDERADO TF-IDF` y se además se generaliza en tópicos (GENERAL, POLITICA, DEPORTE, FARANDULA, MUNDIAL). Esta mejora se realizó con la aplicación de Fuzzy-Matching con un umbral de >= 90% de similitud y eliminación de stopwords. El resultado del ponderado mejorado se encuentra en: 📁`PONDERADO/PONDERADO +`.

