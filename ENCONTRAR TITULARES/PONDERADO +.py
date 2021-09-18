import pandas as pd
from fuzzywuzzy import fuzz

def Ponderado(topic):
    url = "PONDERADO/TF-IDF/" + topic + ".csv"
    dfDeportes = pd.read_csv(url,sep=',')
    del dfDeportes[dfDeportes.columns[0]]

    Palabras = dfDeportes['Word'].values
    Ponderado = dfDeportes['Ponderado'].values
    PonderadoNuevo = {}
    dic1 = {}
    temp = 0
    for pal in Palabras:
        dic1[pal]=[]
        PonderadoNuevo[pal] = Ponderado[temp]
        temp=temp+1

    f = open('StopWordsTW.txt','r',encoding='utf-8')
    stopwords = f.read().splitlines()
    f.close()

    PalabrasUsadas = []
    PalFinales = []
    for k in range(len(Palabras)-1):
        pal = Palabras[k]
        if(pal in stopwords):
            PalabrasUsadas.append(pal)
        else:
            PalFinales.append(pal)
        if(pal not in PalabrasUsadas):
            PalabrasUsadas.append(pal)
            for j in range(k+1,len(Palabras)):
                otra_pal = Palabras[j]
                if(otra_pal not in PalabrasUsadas):
                    #Evaluamos la similitud
                    partial_radio = fuzz.partial_ratio(pal.lower(),otra_pal.lower())
                    if(partial_radio >= 90):
                        dic1[pal].append(otra_pal)
                        PalabrasUsadas.append(otra_pal)
                        #Sumar ponderados
                        PonderadoNuevo[pal]=PonderadoNuevo[pal] + Ponderado[j]

    def addParecidos(pal):
        return dic1[pal]
    def addParecidos2(pal):
        return PonderadoNuevo[pal]
    dfFinal = pd.DataFrame(PalFinales,columns=['Word'])
    dfFinal['PonderadoApilado'] = dfFinal['Word'].apply(addParecidos2)
    dfFinal['Similares'] = dfFinal['Word'].apply(addParecidos)
    dfFinal = dfFinal.sort_values(by=['PonderadoApilado'],ascending=False,ignore_index=True)

    datosInvalidos = [len(x)==2 for x in dfFinal['Similares']]
    dfFinal = dfFinal.drop(dfFinal[datosInvalidos].index)

    url_creado = "PONDERADO/" + topic + ".csv"
    dfFinal.to_csv(url_creado, index=False)

    print("\n================================" + topic + "================================\n")

# PREPROCESADO GENERAL
Ponderado("GENERAL")

# PREPROCESADO DEPORTE
Ponderado("DEPORTE")

# PREPROCESADO POLITICA
Ponderado("POLITICA")

# PREPROCESADO FARANDULA
Ponderado("FARANDULA")

# PREPROCESADO FARANDULA
Ponderado("MUNDIAL")
