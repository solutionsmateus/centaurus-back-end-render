import os
import time
import requests
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import re
import sys
import json 

def get_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.binary_location = "/usr/bin/chromium-browser" 
    
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


driver = get_chrome_driver()
wait = WebDriverWait(driver, 20)


ENCARTE_DIR = Path.home() / "Desktop/Encartes-Concorrentes/Atakarejo"
ENCARTE_DIR.mkdir(parents=True, exist_ok=True)

driver.get("https://atakarejo.com.br/cidade/vitoria-da-conquista")



links = driver.find_elements(By.XPATH, '//a[contains(@class, "button-download-ofertas")]')
print(f"{len(links)} encarte(s) encontrado(s).")

def encontrar_data():
    # h3 - TEXT CSS IN PAGE TO FIND THE DATE OF PAGE"
    try: 
        enc_data = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//h3[contains("TEXT")]'))  
        )
    except:
        return "sem_data"
    
    for div in enc_data:
        texto = div.text.strip()
        if texto:
            nome_pasta = re.sub(r'[\\/*?:"<>|\s]', '_', texto)
            return nome_pasta
    return "sem_data"

for i, link in enumerate(links):
    url_pdf = link.get_attribute("href")
    nome = f"encarte_{i+1}.pdf"
    caminho = ENCARTE_DIR / nome
    try:
        response = requests.get(url_pdf)
        if response.status_code == 200:
            with open(caminho, 'wb') as f:
                f.write(response.content)
            print(f"Baixado: {caminho.name}")
        else:
            print(f"Falha no download: {url_pdf}")
    except Exception as e:
        print(f"Erro ao baixar: {e}")

driver.quit()
