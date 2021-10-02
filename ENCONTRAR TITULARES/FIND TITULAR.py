#################################################### LIBRERIAS #########################################################

import pandas as pd

import json

import re
from datetime import datetime
import wn

wn.download('spawn')

wn.synsets('chat')

import spacy

spacy.prefer_gpu()

nlp = spacy.load('es_core_news_lg')

from ast import literal_eval

import pymongo

#################################################### PREPROCESADO ######################################################


# ELIMINAR EMOJIS

def cutEmojis(tweet):
    regrex_pattern = re.compile(pattern="["u"\U0001F600-\U0001F64F"  # emoticons

                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs

                                        u"\U0001F680-\U0001F6FF"  # transport & map symbols

                                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)

                                        u"\U00002500-\U00002BEF"  # chinese char

                                        u"\U00002702-\U000027B0"

                                        u"\U00002702-\U000027B0"

                                        u"\U000024C2-\U0001F251"

                                        u"\U0001f926-\U0001f937"

                                        u"\U00010000-\U0010ffff"

                                        u"\u2640-\u2642"

                                        u"\u2600-\u2B55"

                                        u"\u200d"

                                        u"\u23cf"

                                        u"\u23e9"

                                        u"\u231a"

                                        u"\ufe0f"  # dingbats

                                        u"\u3030"

                                        "\u2033"

                                        "\u23f0"

                                        '\u20e3'

                                        '\u0107'

                                        '\u23f1'

                                        "]+", flags=re.UNICODE)

    return regrex_pattern.sub(r'', tweet)


# PREPROCESADO DE ELIMINACION DE SIGNOS DE PUNTUACION

def DeletePunctuation(tweet):
    punctuation = ["’", "[", "]", "′", "|", ";", '"']

    for aux in punctuation:
        tweet = tweet.replace(aux, "")

    return tweet


# OBTENER STOPWORDS DE NLTK + OURWORDS

def ObtenerStopwords():
    f = open('StopWordsTW.txt', 'r', encoding='utf-8')

    stopwords = f.read().splitlines()

    return stopwords


# ELIMINAR STOPWORDS DE UN TWEET

def DeleteStopwords(tweet):
    punctuation = ["EN VIVO"]

    for aux in punctuation:
        tweet = tweet.replace(aux, "")

    return tweet


# PREPROCESAR TITULAR: ELIMINAR WORDS, PUNTUACION, @, #

def Preprocesado_titular(texto):
    # ELIMINAR EMOJIS

    texto = cutEmojis(texto)

    # ELIMINAR ARROBAS (ETIQUETAS DE TWITTER) - HASHTAGS - HIPERVINCULOS

    texto = re.sub('#', '', texto)

    texto = re.sub('@', '', texto)

    texto = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)(?:(?:\/[^\s/]))*', '', texto)

    # ELIMINAR INFORMACION ANTES DEL SIGNO "|"

    inicio = texto.find("|")

    texto = str(texto[inicio + 1:]).strip()

    # ELIMINAR SIGNOS DE PUNTUACION

    texto = DeletePunctuation(texto)

    return texto


####################################################### WORDNET ########################################################


# ENCONTRAR SINONIMOS DE UN TERMINO CON WORDNET

def Find_Synonyms(term):
    # TERMINO LEMATIZADO

    doc = nlp(term)

    synonyms = [term]

    for token in doc:
        term = str(token.lemma_).strip()

    # ENCONTRAR SINONIMOS DEL TERMINO CON WORDNET

    words = wn.synsets(term)

    for i in words: synonyms += i.lemmas()

    synonyms = list(set(synonyms))

    return synonyms


##################################################### TITULARES ########################################################


# ENCONTRAR 'N' TITULARES DE UN DETERMINADO TOPICO (DEPORTE, POLITICA, FARANDULA)

def Titular_Topic(topic, n, keyword_usadas):
    # TERMINO RANKEADO

    url_tf = 'PONDERADO/PONDERADO KEYS + LDA/' + topic + '.csv'

    df = pd.read_csv(url_tf)

    lda = df['Words Topico'].values

    # ARREGLO DE TITULARES

    titulares = []

    contador_titulares = 0

    n_ponderado = 0

    while contador_titulares < n:

        # TERMINO RANKEADO CON SINONIMOS (WORDNET)

        termino = str(df.iloc[n_ponderado, 0]).lower()

        synonyms = Find_Synonyms(termino)

        # EXPLORAMOS LAS KEWYWORS YA USADAS, PARA NO REPETIR TEMAS

        if termino in keyword_usadas:

            n_ponderado += 1



        else:

            print("TER ->", termino)

            # RECUPERAR JSON PREPROCESADO

            url_trend = "CORPUS-PREPROCESADO/" + topic + ".json"

            with open(url_trend, encoding="utf-8") as file:

                data = json.load(file)

            # BUSCAR TERMINO(SINONIMOS) EN JSON PREPROCESADO Y AGREGAR A DICCIONARIO

            tweets_dic = {}

            id = 0

            for termino1 in synonyms:

                for tweet in data:

                    # SI TERMINO SE ENCUENTRA EN EL TWEET, GUARDAMOS EL TWEET CON SU PONDERADO EN UN DICCIONARIO

                    if termino1.lower() in [x.lower() for x in tweet['tweet_p']]:
                        id += 1

                        titular = tweet['tweet']

                        ponderado = (tweet['retweets'] * 3) + tweet['likes']

                        array = tweet['tweet_p']

                        url = tweet['url']

                        name = "TWEET-" + str(id)

                        info = [titular, ponderado, array, url]

                        tweets_dic[name] = info

            # ENCONTRAR MEJOR PONDERADO PARA TITULAR

            titular = ""

            ponderado = 0

            array = None

            for key, value in tweets_dic.items():

                if value[1] >= ponderado:
                    titular = value[0]

                    ponderado = value[1]

                    array = value[2]

            print(titular)

            print(array)

            # AÑADIR TITULARES

            titulares.append([Preprocesado_titular(titular), array, topic, url])

            # AÑADIR KEYWORDS USADAS, PARA NO REPETIRLAS

            keyword_usadas.append(termino)

            keyword_usadas += array

            array = (literal_eval(lda[n_ponderado]))

            for word in array:
                keyword_usadas.append(word)

            keyword_usadas = list(set(keyword_usadas))

            n_ponderado += 1

            contador_titulares += 1

    return titulares, keyword_usadas


# ENCONTRAR TITULARES DE LOS TOPICOS

def Matriz_Titulares(n_general, n_deporte, n_politica, n_farandula, n_mundial):
    titulares = []

    keywords_usadas = []

    print("============= GENERAL =============")

    general = Titular_Topic("GENERAL", n_general, keywords_usadas)

    titulares += general[0]

    keywords_usadas += general[1]

    print("============= DEPORTE =============")

    deporte = Titular_Topic("DEPORTE", n_deporte, keywords_usadas)

    titulares += deporte[0]

    keywords_usadas += deporte[1]

    print("============= POLITICA =============")

    politica = Titular_Topic("POLITICA", n_politica, keywords_usadas)

    titulares += politica[0]

    keywords_usadas += politica[1]

    print("============= FARANDULA =============")

    farandula = Titular_Topic("FARANDULA", n_farandula, keywords_usadas)

    titulares += farandula[0]

    keywords_usadas += farandula[1]

    print("============= MUNDIAL =============")

    mundial = Titular_Topic("MUNDIAL", n_mundial, keywords_usadas)

    titulares += mundial[0]

    keywords_usadas += mundial[1]

    return titulares


################################################# MAIN PRINCIPAL #######################################################


def ToJson(titulares2):
    data1 = []

    for titular in titulares2:
        print(titular)

        data1.append({

            "topic": titular[2],

            "tweet": titular[0],

            "preprocesado": titular[1],

            "url": titular[3]
        })
    datos = {}
    datos['noticias'] = data1
    now = datetime.now()
    datos['fecha'] = [now.year, now.month, now.day, now.hour]
    client = pymongo.MongoClient("mongodb+srv://unsaac:unsaac123@primero.6gh6z.mongodb.net/NoticiasUnsaac?retryWrites=true&w=majority")
    db = client["NoticiasUnsaac"]

    # Eliminamos los datos que ya se encontraban almacenados
    Collection = db["datosNoticias"]
    Collection.insert_one(datos)
    #with open("./TITULARES JSON.json", 'w', encoding="utf-8") as file:
    #    json.dump(datos, file, indent=4, ensure_ascii=False)


# MAIN, TITULARES EN CSV

# (N° TITULARES GENERAL, N° TITULARES DEPORTE,N° TITULARES POLITICA, N° TITULARES FARANDULA, N° TITULARES MUNDIAL)

titulares2 = Matriz_Titulares(2, 5, 7, 3, 3)

ToJson(titulares2)

df2 = pd.DataFrame([[i[2], i[0], i[1], i[3]] for i in titulares2], columns=['Topic', 'Tweet', 'Preprocesado', 'Url'])

df2.to_csv("TITULARES_TF-IDF.csv")