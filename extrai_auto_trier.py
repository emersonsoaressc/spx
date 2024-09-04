import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By

def cadastra_planograma():
    #abre a instancia do chrome na pagina:
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(2)
    url = 'http://179.184.16.200:4647/sgfpod1/Menu.pod'
    driver.get(url)
    