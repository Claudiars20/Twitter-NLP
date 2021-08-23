import pandas as pd
import json
import re



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

def Preprocesado_titular(texto):

    # ELIMINAR EMOJIS
    texto = cutEmojis(texto)

    # ELIMINAR ARROBAS (ETIQUETAS DE TWITTER) - HASHTAGS - HIPERVINCULOS
    texto = re.sub('([#]|htt).*?(?=[\s|$])', '', texto)

    texto = re.sub('@', '', texto)

    texto = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', texto)

    return texto

def Titular_Topic(topic, n, tf, titulares):

    stopwords = ["covid-19","| video","video","foto","vacuna","pedro castillo","’","periodista","alianza lima","talibán","fecha","coronavirus",
                 "⏰","covid-19","fecha", "año","agosto","the","detalle","video", "the","and","país","año","of","presidente","to",
                 "persona","are","with","for", "persona","país","columna","vivo","agosto","caso","jueves"]

    # TERMINO RANKEADO
    url_tf = 'PONDERADO/'+ tf + '/'+ topic + '.csv'
    df = pd.read_csv(url_tf)

    titulares_a = []
    aux = 0
    i = -1
    while aux < n:
        i += 1
        termino = df.iloc[i, 1]

        if termino not in stopwords:
            aux += 1
            # RECUPERAR JSON PREPROCESADO
            url_trend = "CORPUS-PREPROCESADO/" + topic + ".json"
            with open(url_trend, encoding="utf-8") as file:
                data = json.load(file)

            # BUSCAR TERMINO EN JSONS Y ALMACENAR
            tweets_dic = {}

            for tweet in data:
                cont = 0
                # SI TERMINO SE ENCUENTRA EN EL TWEET, GUARDAMOS EL TWEET CON SU PONDERADO EN EL DICCIONARIO
                if termino in [x.lower() for x in tweet['tweet_p']]:
                    cont += 1
                    titular = tweet['tweet']
                    ponderado = tweet['retweets']*3 + tweet['likes']
                    array = tweet['tweet_p']

                    name = "TWEET-"+str(cont)
                    info = [titular, ponderado, array]

                    tweets_dic[name] = info


            # ENCONTRAR MEJOR PONDERADO PARA TITULAR
            titular = ""
            ponderado = 0
            array = None
            for key,value in tweets_dic.items():
                if value[1] >= ponderado:
                    titular = value[0]
                    ponderado = value[1]
                    array = value[2]

            # AÑADIR TITULARES
            if Preprocesado_titular(titular) not in titulares:
                titulares_a.append( [Preprocesado_titular(titular) , array, topic] )
            else:
                aux -= 1

    return titulares_a, titulares

def Matriz_Titulares(tf):
    titulares_a = []
    titulares = []

    print("============= GENERAL =============")
    general = Titular_Topic("GENERAL",1,tf, titulares)

    for i in general[0]:
        titulares_a.append( i )
        titulares.append( i[0] )
    print("============= DEPORTE =============")
    deporte = Titular_Topic("DEPORTE",3,tf, titulares)

    for i in deporte[0]:
        titulares_a.append( i )
        titulares.append(i[0])

    print("============= POLITICA =============")
    politica = Titular_Topic("POLITICA",5,tf, titulares)

    for i in politica[0]:
        titulares_a.append( i )
        titulares.append(i[0])

    print("============= FARANDULA =============")
    politica = Titular_Topic("FARANDULA", 4, tf, titulares)

    for i in politica[0]:
        titulares_a.append(i)
        titulares.append(i[0])

    print("============= MUNDIAL =============")
    mundial = Titular_Topic("MUNDIAL",4,tf, titulares)

    for i in mundial[0]:
        titulares_a.append( i )
        titulares.append(i[0])

    return titulares_a


#titulares1 = Matriz_Titulares("TF-NORMALIZADO")

#df1 = pd.DataFrame([[i[2], i[0], i[1]] for i in titulares1], columns=['Topic','Tweet', 'Preprocesado'])
#df1.to_csv("TITULARES_TF-NORMALIZADO.csv")



titulares2 = Matriz_Titulares("TF-IDF")

df2 = pd.DataFrame([[i[2], i[0], i[1]] for i in titulares2], columns=['Topic','Tweet', 'Preprocesado'])
df2.to_csv("TITULARES_TF-IDF.csv")