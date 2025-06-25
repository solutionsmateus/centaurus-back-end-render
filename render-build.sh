#!/usr/bin/env bash

# Atualiza a lista de pacotes
apt-get update

# Instala o Chromium e o chromedriver
apt-get install -y chromium-browser chromium-chromedriver

# Opcional: Limpa o cache do apt para economizar espaço
apt-get clean
rm -rf /var/lib/apt/lists/*

# Adicione aqui quaisquer outros comandos de build que você já tenha
# Por exemplo, a instalação das dependências Python, se não for feita automaticamente pelo Render
# pip install -r requirements.txt
