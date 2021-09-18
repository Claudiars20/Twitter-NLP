import requests
import pandas as pd
import urllib
import time
import pyperclip as pc
import pyautogui
from bs4 import BeautifulSoup
from numpy.core.fromnumeric import clip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


data = pd.read_csv('TITULARES_TF-IDF.csv')
noticias = data.iloc[:, 3]
URLs =[]
adlt = 'off'
noticias_string=[]

for noticia in noticias:
    noticia = noticia[1:len(noticia)-1]
    nueva_noticia = ""
    for a in noticia:
        if a != "'" and a != ",":
            nueva_noticia += a
    noticias_string.append(nueva_noticia+" -elcomercio -gestion")



URLs = []
for noticia in (noticias_string):
    i=1
    print(noticia)
    while True:
        driver = webdriver.Chrome('./chromedriver.exe')
        action = ActionChains(driver)
        driver.get('https://www.google.com.pe/imghp?hl=es&ogbl')
        box = driver.find_element_by_xpath('//*[@id="sbtc"]/div/div[2]/input')
        box.send_keys(noticia)
        box.send_keys(Keys.ENTER)
        driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div['+str(i)+']/a[1]/div[1]/img').click()
        image = driver.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img')  
        action.context_click(image).perform()
        time.sleep(1)
        #actionchains.send_keys(Keys.ARROW_DOWN).perform()
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('enter')
        time.sleep(1)
        src = pc.paste()
        if("data" not in str(src)):
            print(src)
            URLs.append(src)
            driver.quit()
            break
        else:
            i+=1
        driver.quit()



datos = data
datos['URLs'] = URLs
print(datos)
datos.to_csv('TITULARES-20-08.csv')
