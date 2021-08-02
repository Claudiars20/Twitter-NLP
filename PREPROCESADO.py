################################################## IMPORTACIONES #######################################################import os
import json
import os
import pandas as pd

# LIBRERIA PARA STOPWORDS Y TOKENIZER
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# LIBRERIA PARA ANALISIS LE LENGUAJE NATURAL DESARROLLADA CON REDES NEURONALES
import stanza

# INSTALANDO DEPENDENCIAS PARA PODER OPERAR CON EL LENGUAJE ESPAÑOL
stanza.download('es', package='ancora', processors='tokenize,mwt,pos,lemma', verbose=True)
stNLP = stanza.Pipeline(processors='tokenize,mwt,pos,lemma', lang='es', use_gpu=True)


#################################################### PREPROCESADO ######################################################

def Lemmatization(word):
    # LEMATIZAMOS EL PARAMETRO (PALABRA)
    doc = stNLP(word)
    # RECUPERAMOS EL LEMA DEL WORD
    aux = doc.sentences[0].words[0]
    return (aux.lemma)

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
                               "]+", flags=re.UNICODE)
    return regrex_pattern.sub(r' ', tweet)

def Preprocessing(texto):
    word_tokens = word_tokenize(texto)

    # RECUPERAMOS LOS STOP_WORDS DE LA LIBRERIA NLTK.CORPUS
    stop_words = set(stopwords.words('spanish'))

    # NUESTROS STOPWORDS
    our_stopwords = {"https", "http","...","..","q","/","*","'"}

    # UNIMOS LOS STOPWORDS DE LA LIBRERIA CON NUESTROS STOPWORDS
    stop_words = stop_words.union(our_stopwords)

    # FILTRAMOS EL ARREGLO TOKENIZADO
    filtered = []
    bandera = False
    for i in range(0, len(word_tokens)):

        # CONVERTIMOS A MINUSCULA
        word_tokens[i] = word_tokens[i].lower()

        # ELIMINAMOS SIGNOS DE PUNTUACION
        signos = ["?", "¿", "¡", "!", " ", ",", ".", ";", ":", "#"]
        if (word_tokens[i] in signos): word_tokens[i] = ' '

        # ELIMINAMOS ESPACIOS
        word_tokens[i] = re.sub('\s+', ' ', word_tokens[i])

        # ELIMINAMOS EMOJIS

        word_tokens[i] = cutEmojis(word_tokens[i])

        # VALIDAMOS QUE SEAN DIFERENTES A VACIO POR LA FUNCION R.SUB

        # VALIDAMOS ETIQUETAS DE USUARIOS
        if (word_tokens[i] == "@"): bandera = True

        if (word_tokens[i] != ' ' and word_tokens[i] != "@" and bandera == False):
            # ELIMINAMOS LOS STOPWORDS
            if (word_tokens[i] not in stop_words):

                if ("//" not in word_tokens[i]):
                    # REALIZAMOS LA LEMATIZACION
                    word_tokens[i] = Lemmatization(word_tokens[i])
                    if (word_tokens[i] not in stop_words and len(word_tokens[i])>2):
                        filtered.append(word_tokens[i])

        if (bandera == True and word_tokens[i] != "@"): bandera = False


    return filtered

def CleanCarpet():
    folder = 'CORPUS-PREPROCESADO'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)



# LIMPIAR CARPETA
CleanCarpet()

# LISTAR DIRECTORIOS DE NUESTRO CORPUS
url_JSONs = os.listdir('CORPUS')


for i in url_JSONs:

    tweets = []
    url_trend = "CORPUS/" + i
    for line in open(url_trend, encoding="utf8"):
        tweets.append(json.loads(line))

    #### CREAMOS EL JSON (LEY <==> ARREGLO DE PALABRAS PREPROCESADAS)
    data1 = {}
    data1['trend'] = []

    # PREPROCESADO DE CADA TWEET
    for tweet in tweets:

        pre_trend = Preprocessing( tweet['tweet'] )
        print(pre_trend)

        # AGREGAMOS AL ARCHIVO JSON (LEY <==> ARREGLO DE PALABRAS PREPROCESADAS)
        data1['trend'].append({
            'tweet': pre_trend
        })


    nombre_archivo = "./CORPUS-PREPROCESADO/" + str(i)
    print(nombre_archivo)
    with open(nombre_archivo, 'w', encoding="utf-8") as file:
        json.dump(data1, file, indent=4, ensure_ascii=False)

