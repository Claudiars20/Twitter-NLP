#################################################### LIBRERIAS #########################################################
import pandas as pd
import json
import re
import wn
wn.download('spawn')
wn.synsets('chat')

import spacy
spacy.prefer_gpu()
nlp = spacy.load('es_core_news_lg')


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
    punctuation = ["’", "[", "]", "′", "|", ";",'"']
    for aux in punctuation:
        tweet = tweet.replace(aux, "")

    return tweet

# OBTENER STOPWORDS DE NLTK + OURWORDS
def ObtenerStopwords():
    f = open('StopWordsTW.txt', 'r', encoding='utf-8')
    stopwords = f.read().splitlines()

    return  stopwords

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

    texto = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', texto)

    # ELIMINAR INFORMACION ANTES DEL SIGNO "|"
    inicio = texto.find("|")
    texto = str(texto[inicio + 1:]).strip()

    # ELIMINAR SIGNOS DE PUNTUACION
    texto = DeletePunctuation(texto)

    return texto





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
    url_tf = 'PONDERADO/' + topic + '.csv'
    df = pd.read_csv(url_tf)

    # ARREGLO DE TITULARES
    titulares = []

    contador_titulares = 0
    n_ponderado = 0
    while contador_titulares < n:

        # TERMINO RANKEADO CON SINONIMOS
        termino = str(df.iloc[n_ponderado, 0]).lower()
        synonyms = Find_Synonyms(termino)


        if termino in keyword_usadas:
            n_ponderado += 1
        else:
            # RECUPERAR JSON PREPROCESADO
            url_trend = "CORPUS-PREPROCESADO/" + topic + ".json"
            with open(url_trend, encoding="utf-8") as file:
                data = json.load(file)

            # BUSCAR TERMINO(SINONIMOS) EN JSON PREPROCESADO Y AGREGAR A DICCIONARIO
            tweets_dic = {}
            for termino1 in synonyms:

                for tweet in data:
                    id = 0
                    # SI TERMINO SE ENCUENTRA EN EL TWEET, GUARDAMOS EL TWEET CON SU PONDERADO EN UN DICCIONARIO
                    if termino1.lower() in [x.lower() for x in tweet['tweet_p']]:
                        id += 1
                        titular = tweet['tweet']
                        ponderado = tweet['retweets'] * 3 + tweet['likes']
                        array = tweet['tweet_p']

                        name = "TWEET-" + str(id)
                        info = [titular, ponderado, array]

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

            # AÑADIR TITULARES
            titulares.append([Preprocesado_titular(titular), array, topic])
            keyword_usadas.append([termino])

            n_ponderado += 1
            contador_titulares += 1

    return titulares, keyword_usadas

# ENCONTRAR TITULARES DE LOS TOPICOS
def Matriz_Titulares(tf):
    titulares = []
    keywords_usadas = []

    print("============= GENERAL =============")
    general = Titular_Topic("GENERAL",2,keywords_usadas)

    titulares += general[0]
    keywords_usadas += general[1]

    print("============= DEPORTE =============")
    deporte = Titular_Topic("DEPORTE",5,keywords_usadas)

    titulares += deporte[0]
    keywords_usadas += deporte[1]

    print("============= POLITICA =============")
    politica = Titular_Topic("POLITICA",5,keywords_usadas)

    titulares += politica[0]
    keywords_usadas += politica[1]

    print("============= FARANDULA =============")
    farandula = Titular_Topic("FARANDULA", 3, keywords_usadas)

    titulares += farandula[0]
    keywords_usadas += farandula[1]

    print("============= MUNDIAL =============")
    mundial = Titular_Topic("MUNDIAL", 3, keywords_usadas)

    titulares += mundial[0]
    keywords_usadas += mundial[1]

    return titulares








#titulares1 = Matriz_Titulares("TF-NORMALIZADO")

#df1 = pd.DataFrame([[i[2], i[0], i[1]] for i in titulares1], columns=['Topic','Tweet', 'Preprocesado'])
#df1.to_csv("TITULARES_TF-NORMALIZADO.csv")

# MAIN, TITULARES EN CSV
titulares2 = Matriz_Titulares("TF-IDF")

df2 = pd.DataFrame([[i[2], i[0], i[1]] for i in titulares2], columns=['Topic','Tweet', 'Preprocesado'])
df2.to_csv("TITULARES_TF-IDF.csv")