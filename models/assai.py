import os
import time
import json
import re
import selenium
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service, Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium import webdriver
from selenium.webdriver.chrome import remote_connection

LOJAS_ESTADOS = {
    "Maranhão": "Assaí Angelim",
    "Alagoas": "Assaí Maceió Farol",
    "Ceará": "Assaí Bezerra M (Fortaleza)",
    "Pará": "Assaí Belém",
    "Paraíba": "Assaí João Pessoa Geisel",
    "Pernambuco": "Assaí Avenida Recife",
    "Piauí": "Assaí Teresina",
    "Sergipe": "Assaí Aracaju",
    "Bahia": "Interior Vitória da Conquista",
}

BASE_URL = "https://www.assai.com.br/ofertas"
download_base_path = Path("downloads/Assai")
os.makedirs(download_base_path, exist_ok=True)

driver = WebDriverWait
wait = WebDriverWait

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def clicar_elemento(soup):
    elemento =  soup.select("arguments[0].scrollIntoView({block: 'center'});")
    elemento.click()
    
def scroll_down_and_up():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, 1);")
    time.sleep(0.5)

def baixar_imagens_da_pagina(soup, jornal_num, download_dir):
    baixados = []
    links = soup.select("a.download[href$='.jpeg']")

    for idx, a_tag in enumerate(links, 1):
        url = a_tag["href"]
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            filename = f"encarte_jornal_{jornal_num}_{idx}_{int(time.time())}.jpg"
            filepath = download_dir / filename

            with open(filepath, "wb") as f:
                for chunk in response.iter_content(8192):
                    f.write(chunk)

            print(f"✔️ Imagem salva: {filepath.name}")
            baixados.append(str(filepath.resolve()))
        except Exception as e:
            print(f"❌ Erro ao baixar {url}: {e}")

    return baixados

def encontrar_nome_data(soup):
    try:
        div = soup.select_one("div.ofertas-tab-validade")
        if div:
            texto = div.get_text(strip=True)
            nome_pasta = re.sub(r'[\\/*?:"<>|\s]', '_', texto)
            return nome_pasta
    except:
        pass
    return "sem_data"

def main():
    loja_param = os.environ.get("models/assai.py")
    all_downloaded_files = []

    try:
        response = requests.get(BASE_URL, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')

        nome_data = encontrar_nome_data(soup)
        nome_loja = loja_param.replace(' ', '_') if loja_param else "Assai"
        pasta_destino = download_base_path / f"encartes_{nome_loja}_{nome_data}"
        os.makedirs(pasta_destino, exist_ok=True)

        arquivos = baixar_imagens_da_pagina(soup, 1, pasta_destino)
        all_downloaded_files.extend(arquivos)

    except Exception as e:
        print(f"❌ Erro geral no processamento: {e}")

    print(f"DOWNLOADED_FILES:{json.dumps(all_downloaded_files)}")

if __name__ == "__main__":
    main()
