#Importando bibliotecas
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import requests
from datetime import datetime
import time
import os
from tkinter import *

def bot() -> None:
    driver = open_browser()
    if not os.path.exists('receitas.csv'):
        search_file(driver)
    else:
        os.remove('receitas.csv')
        search_file(driver)
    json_data = read_and_convert_csv()
    response, json_informations = send_to_api(json_data)
    if response.status_code == 200:
        json_data = json.loads(json_informations)
        window_text.delete(1.0, END)
        window_text.insert(END, f'Arquivo enviado com sucesso\n{response.json()}\n{json.dumps(json_data, indent=4, ensure_ascii=False)}')
    else:
        window_text.delete(1.0, END)
        window_text.insert(END, 'Algo deu errado')
    return

def open_browser() -> webdriver:
    #Definindo diretório de download
    project_directory = os.path.dirname(os.path.abspath(__file__))
    chrome_options = Options()
    prefs = {'download.default_directory': project_directory}
    chrome_options.add_experimental_option('prefs', prefs)

    # Inicializando Chrome
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    #Acessando url
    url = 'https://portaldatransparencia.gov.br'
    driver.get(url)
    return driver

def search_file(driver) -> None:
    #Navegando até o arquivo e baixando o mesmo
    driver.find_element(By.XPATH,'//*[@id="despesas-card"]').click()
    driver.find_element(By.XPATH,'//*[@id="receitas-links"]/li[2]/a').click()
    driver.find_element(By.XPATH,'//*[@id="btnBaixar"]').click()
    while not os.path.exists('receitas.csv'):
        time.sleep(1)
    driver.quit()
    return

def read_and_convert_csv() -> json:
    #Lendo o arquivo CSV e convertendo para Json
    data_frame = pd.read_csv('receitas.csv', delimiter=';').iloc[:,[2,6,8,9]]
    json_df = data_frame.to_json()
    return json.loads(json_df)

def send_to_api(json_data) -> str:
    informations = {
        "Autor": "Tales Brandt Nascimento",
        "Data": f"{datetime.now().strftime("%Y-%m-%d")}",
        "Dados": json_data
    }
    json_informations = json.dumps(informations, ensure_ascii=False)
    headers = {'Content-Type': 'application/json'}
    response = requests.post('https://devbunnycofco.azurewebsites.net/acontador.aspx', headers= headers, data=json_informations)
    return response, json_informations

#Janela do projeto
window = Tk()
window.title('Bot')
button_start = Button(window, text='Start', command=bot)
button_start.grid(column=0, row=0)
window_text = Text(window, wrap=WORD, width=100, height=100)
window_text.grid(column=0, row=1)
window.mainloop()