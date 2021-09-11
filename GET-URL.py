import requests
import pandas as pd
from bs4 import BeautifulSoup
import urllib
data = pd.read_csv('./TITULARES_TF-IDF.csv')
noticias = data.iloc[:, 3]
URLs =[]
adlt = 'off'
for i in range(len(noticias)):
    busqueda = noticias[i][1:-1]
    print(busqueda)
    busqueda = busqueda.split("', '")
    a = ' '.join(busqueda)
    a=a.replace(' ','+')
    URL='https://bing.com/images/search?q=' + a + '&safeSearch=' + adlt + '&count=' + str(1)
    print(URL)
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent": USER_AGENT}
    resp = requests.get(URL, headers=headers)
    route=[]
    soup = BeautifulSoup(resp.content, "html.parser")
    wow = soup.find_all('a',class_='iusc')
    count = 1
    for i in wow:
        try:
            resource = urllib.urlopen(eval(i['m'])['murl'])
            output = open("file01.jpg","wb")
            output.write(resource.read())
            output.close()
            print('encontre\n')
            break
        except:
            pass
print(URLs)
datos = data
datos['URLs'] = URLs
print(datos)
datos.to_csv('./TITULARES-20-08.csv')