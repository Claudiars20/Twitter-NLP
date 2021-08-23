################################################## IMPORTACIONES #######################################################import os
import json
import os
import pandas as pd

# LIBRERIA PARA STOPWORDS Y TOKENIZER
import re
import nltk
'''nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# LIBRERIA PARA ANALISIS LE LENGUAJE NATURAL DESARROLLADA CON REDES NEURONALES
import stanza

# INSTALANDO DEPENDENCIAS PARA PODER OPERAR CON EL LENGUAJE ESPAÑOL
stanza.download('es', package='ancora', processors='tokenize,mwt,pos,lemma', verbose=True)
stNLP = stanza.Pipeline(processors='tokenize,mwt,pos,lemma', lang='es', use_gpu=True)'''

# ERN
import spacy
spacy.prefer_gpu()
nlp = spacy.load('es_core_news_lg')


#################################################### LIMPIANDO RUIDO ###################################################

# PREPROCESADO DE ELIMINACION DE EMOJIS
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
    return regrex_pattern.sub(r'', tweet)

# PREPROCESADO DE UN TWEET
def Preprocessing(texto):

    # ELIMINAR EMOJIS
    texto = cutEmojis(texto)

    # ELIMINAR ARROBAS (ETIQUETAS DE TWITTER) - HASHTAGS - HIPERVINCULOS
    texto = re.sub('([@#]|htt).*?(?=[\s|$])', '', texto)

    preprocesado = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', texto)

    return preprocesado

# POST TAGGING DE TERMINOS DEL TWEET
def Tagging(preprocesado, doc):

    tags = []
    # RECUPERAR TOKENS DE TAG = PROPN, NOUN
    for token in doc:
        if token.pos_ == "PROPN" or token.pos_ == "NOUN":
            tags.append(str(token.lemma_))

    return tags

# RECONOCIMIENTO DE LAS ENTIDADES (LOC, MISC, ORG, PER)
def NER(doc):

    entidades = []
    # RECUPERAR ENTIDADES
    for word in doc.ents:
        entidades.append(str(word))

    return entidades

# IDENTIFICAR KEYWORDS (TAGS + ENTIDADES)
def Tags_NER(tags, entidades):

    keywords = []
    for i in entidades: keywords.append(i)

    # SI TAG NO ESTA EN ENTIDADES, SE AGREGA COMO KEYWORDS
    entidades_array = " ".join(entidades)

    for word in tags:
        if word not in entidades_array:
            keywords.append(word)

    return keywords

def CleanNoise(texto):

    preprocesado = Preprocessing(texto)

    doc = nlp(preprocesado)
    tags = Tagging(preprocesado, doc)

    entidades = NER(doc)

    keywords = Tags_NER(tags, entidades)

    return keywords


#################################################### FUNCIONES #########################################################

def CleanCarpet(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

# DICCIONARIO DE CUENTAS DE TWITTER DE DONDE EXTRAEREMOS LOS TWEETS
def Account_Dicctionary():
    df = pd.read_csv("CUENTAS DE TWITTER/CUENTAS.csv")
    dicc = {}
    for i in range(df.shape[0]):
        a = [df.iloc[i, 1], df.iloc[i, 2]]
        dicc[df.iloc[i, 0]] = a
    return dicc

# PROCESADO DE TWEETS DE TODAS LAS CUENTAS DE TWITTER
def NLP_Account():
    # LISTAR DIRECTORIOS DE NUESTRO CORPUS
    url_JSONs = os.listdir('CORPUS')


    ## CONVERTIR TWEET DE UNA CUENTA EN ARREGLO DE PALABRAS PREPROCESADAS
    for i in url_JSONs:

        tweets = []
        url_trend = "CORPUS/" + i
        for line in open(url_trend, encoding="utf8"):
            tweets.append(json.loads(line))

        ### CREAMOS EL JSON ( TWEET : [PALABRAS PREPROCESADAS] )
        data1 = []

        ## PREPROCESADO DE UN TWEET
        for tweet in tweets:
            pre_trend = CleanNoise( tweet['tweet'] )
            tweet_aux = tweet['tweet']
            username = tweet['username']
            retweets = tweet["retweets_count"]
            likes = tweet["likes_count"]

            # AGREGAMOS AL ARCHIVO JSON
            data1.append({
                'account': username,
                'tweet': tweet_aux,
                'tweet_p': pre_trend,
                "retweets": retweets,
                "likes": likes
            })

        ## GUARDAR JSON PREPROCESADO
        nombre_archivo = "./CORPUS-PREPROCESADO/" + str(i)
        print(nombre_archivo)
        with open(nombre_archivo, 'w', encoding="utf-8") as file:
            json.dump(data1, file, indent=4, ensure_ascii=False)

        print("\n================================" + str(i) + "================================\n")

# UNION DE TODOS LOS PROCESADOS DE LAS CUENTAS DE TWITTER
def NLP_Union():
    # LISTAR DIRECTORIOS DE CUENTAS PREPROCESADAS
    url_JSONs = os.listdir('CORPUS')

    ### CREAMOS EL JSON ( TWEET : [PALABRAS PREPROCESADAS] )
    data1 = []

    ## UNIR LOS TWEETS PREPROCESADAS
    for i in url_JSONs:

        # RECUPERAMOS LA URL DEL JSON
        url_creator = "./CORPUS-PREPROCESADO/" + i

        # ABRIMOS EL ARCHIVO JSON
        with open(url_creator, encoding="utf-8") as file:
            data = json.load(file)

        # UNIMOS
        data1 += data

    ## GUARDAR JSON PREPROCESADO
    nombre_archivo = "./CORPUS-PREPROCESADO/GENERAL.json"
    print(nombre_archivo)
    with open(nombre_archivo, 'w', encoding="utf-8") as file:
        json.dump(data1, file, indent=4, ensure_ascii=False)

# UNION DE TODOS LOS PROCESADOS DE LAS CUENTAS DE TWITTER POR TOPICO
def NLP_Topico(dic, tipo):

    # LISTAR DIRECTORIOS DE CUENTAS PREPROCESADAS
    url_JSONs = os.listdir('CORPUS')

    ### CREAMOS EL JSON ( TWEET : [PALABRAS PREPROCESADAS] )
    data1 = []


    ## UNIR LOS TWEETS PREPROCESADAS
    for i in url_JSONs:
        name = i.replace(".json","")
        if (dic[name][1] == tipo):


            # RECUPERAMOS LA URL DEL JSON
            url_creator = "./CORPUS-PREPROCESADO/" + i

            # ABRIMOS EL ARCHIVO JSON
            with open(url_creator, encoding="utf-8") as file:
                data = json.load(file)

            # RECORREMOS EL JSON Y RECUPERAMOS EL ARREGLO DE WORDS Y EL IDENTIFICADOR DE LA LEY
            data1 += data


    ## GUARDAR JSON PREPROCESADO
    nombre_archivo = "./CORPUS-PREPROCESADO/"+tipo+".json"
    print(nombre_archivo)
    with open(nombre_archivo, 'w', encoding="utf-8") as file:
        json.dump(data1, file, indent=4, ensure_ascii=False)

################################################ PREPROCESADO TO JSONS #################################################

# LIMPIAR CARPETA
CleanCarpet('CORPUS-PREPROCESADO')

# PREPROCESADO DE LAS CUENTAS DE TWITTER
NLP_Account()


dic = Account_Dicctionary()

# PREPROCESADO GENERAL
NLP_Union()

# PREPROCESADO DEPORTE
NLP_Topico(dic,"DEPORTE")

# PREPROCESADO POLITICA
NLP_Topico(dic,"POLITICA")

# PREPROCESADO FARANDULA
NLP_Topico(dic,"FARANDULA")

# PREPROCESADO FARANDULA
NLP_Topico(dic,"MUNDIAL")



