#################################################### LIBRERIAS #########################################################
import pandas as pd
import json

import gensim
from gensim import corpora

import numpy
#################################################### FUNCIONES #########################################################

# TOPÍC MODELING DE KEYWORDS DE DEPORTE, POLITICA ....

# ENCONTRAR WORDS PREPROCESADOS DONDE APARECE CADA KEYWORD DE UN TOPICO
def Keywords_WithWords( topic ):
    # LEER CSV DE PONDERADO
    url = "PONDERADO/PONDERADO +/"+ topic + ".csv"
    dfDeportes = pd.read_csv(url,sep=',')

    # LEER ARCHIVO JSON PREPROCESADO
    url_trend = "CORPUS-PREPROCESADO/" + topic + ".json"
    with open(url_trend, encoding="utf-8") as file:
        data = json.load(file)
    keywords = dfDeportes['Word'].values

    print(len(keywords))

    # DEFINIR DICCIONARIO
    dic_key_pln = {}

    # RECORREMOS EL CSV DE PONDERADOS
    n = 100
    if len(keywords) < 100: n = len(keywords)
    for i in range(n):

        tweet_p_general = []
        # RECORREMOS JSON PREPROCESADO
        for aux in data:
            if keywords[i] in aux["tweet_p"]:
                tweet_p_general += aux["tweet_p"]

        # AGREGAMOS KEYWORD Y LISTA DE PREPROCESADO A DICCIONARIO
        dic_key_pln[keywords[i]] = tweet_p_general

    # GUARDAR DATA EN UN CSV
    df = pd.DataFrame([[key, dic_key_pln[key]] for key in dic_key_pln.keys()], columns=['Name', 'KeywordsByWord'])
    url = "PONDERADO/PONDERADO CON CONTEXTO/" + topic + ".csv"
    df.to_csv(url)

# TOPIC MODELING DE LAS KEYWORDS DE CADA TOPICO
def TopicModeling( topic ):
    # LEER CSV DE KEYWORDS CON SUS WORDS
    url = "PONDERADO/PONDERADO CON CONTEXTO/" + topic + ".csv"
    df = pd.read_csv(url)

    text_data = []
    for i in range(df.shape[0]):
      a = df.iloc[i,2][2:-2]
      a = a.split("', '")
      text_data.append(a)

    # DICCIONARIO DE PALABRAS DEL CONJUNTO DE DATOS
    dicc = corpora.Dictionary(text_data)

    # CREAMOS BAG OF WORDS POR TOPICO
    corpus = [dicc.doc2bow(text) for text in text_data]

    # NUMERO DE TOPICOS DE CLASIFICACION
    NUM = 20
    # ENTRENAMOS EL MODELO Y LO GUARDAMOS
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM, id2word=dicc,random_state=100,update_every=1, passes=1, alpha='symmetric',decay=0.5,offset=1)
    ldamodel.save('modelo.gensim')

    # APLICAMOS EL LDA CON EL MODELO ENTRENADO
    topics = ldamodel.print_topics(num_words=4)
    #for topic in topics: print(topic)
    lda = gensim.models.ldamodel.LdaModel.load('modelo.gensim')

    # CLASIFICAMOS LAS KEYWORDS A UN TOPICO
    def topic_documents(ldamodel=ldamodel, corpus=corpus, texts=dicc):
        # CREAMOS DATAFRAME
        df_out = pd.DataFrame()

        # OBTENEMOS EL TOPICO PRINCIPAL DE CADA DOCUMENTO
        for i, row in enumerate(ldamodel[corpus]):
            row = sorted(row, key=lambda x: (x[1]), reverse=True)
            # OBTENEMOS EL TOPICO DOMINANTE, LA CONTRIBUCIÓN PORCENTUAL Y LAS PALABRAS CLAVE DE CADA DOCUMENTO
            for j, (topic_num, prop_topic) in enumerate(row):
                if j == 0:  # => TOPICO DOMINANTE
                    wp = ldamodel.show_topic(topic_num)
                    topic_keywords = ", ".join([word for word, prop in wp])
                    df_out = df_out.append(pd.Series([int(topic_num), round(prop_topic, 4), topic_keywords]), ignore_index=True)
                else:
                    break
        df_out.columns = ['Topico Dominante', 'Porcentaje de Contribución', 'KeyWords']

        # AGREGAMOS TEXTO ORIGINAL AL FINAL
        contents = pd.Series(texts)
        df_out = pd.concat([df_out, contents], axis=1)

        return df_out

    # FORMATO LDA BASADO EN EL CORPUS
    df_topicsXkeyword = topic_documents(ldamodel=ldamodel, corpus=corpus, texts=dicc)

    # FORMATO CSV ORGANIZADO
    df_dominant_topic = df_topicsXkeyword.reset_index()
    df_dominant_topic.columns = ['Trend', 'Topico Dominante', 'Porcentaje de Contribución', 'KeyWords', 'Tokens']

    df_dominant_topic['Trend'] = df['Name']
    df_dominant_topic = df_dominant_topic.drop(['KeyWords', 'Tokens'], axis=1)

    df_dominant_topic = df_dominant_topic.dropna()

    df_dominant_topic.drop(df_dominant_topic.loc[df_dominant_topic['Porcentaje de Contribución'] <= 0.8].index, inplace=True)



    # GUARDAMOS EL ARCHIVO CSV
    url = "PONDERADO/PONDERADO CON LDA/" + topic + ".csv"
    df_dominant_topic.to_csv(url, index=False)


# UNIR KEYWORDS CON SUS KEYWORDS DE TOPIC MODELING
def Csv_With_TopicModeling( topic ):

    # LEER CSV DE KEYWORDS CON SUS WORDS
    url = "PONDERADO/PONDERADO CON LDA/" + topic + ".csv"
    df = pd.read_csv(url)
    df = df.dropna()

    keywords = df['Trend'].values
    topico = df['Topico Dominante'].values
    keywords_by_topic = []

    # RECORRER CSV Y AGRUPAR KEYWORDS POR TOPICO
    for aux in range(0,20):
        keys = []
        #RECORRER CSV DE KEYWORDS
        for i in range(len(keywords)):
            if not numpy.isnan(topico[i]):
                if int(topico[i]) == aux:
                    keys.append(keywords[i])

        keywords_by_topic.append(keys)

    # AGREGAR ARREGLO DE KEYWORDS DE TOPICO A CADA WORD
    context_topic = []
    for i in topico:
        if not numpy.isnan(i):
            context_topic.append(keywords_by_topic[int(i)])
    dfFinal = pd.DataFrame({"Keyword": keywords,"Words Topico": context_topic})

    url_creado = "PONDERADO/PONDERADO KEYS + LDA/" + topic + ".csv"
    dfFinal.to_csv(url_creado, index=False)

# METODOS ANTERIORES UNIDOS POR TOPICO
def Main( topic, n_topics ):
    Keywords_WithWords(topic)
    TopicModeling(topic)
    Csv_With_TopicModeling(topic)


################################################# MAIN PRINCIPAL #######################################################

Main( "GENERAL", 8 )
Main( "DEPORTE", 8 )
Main( "POLITICA" , 8 )
Main( "FARANDULA", 8 )
Main( "MUNDIAL", 8 )
