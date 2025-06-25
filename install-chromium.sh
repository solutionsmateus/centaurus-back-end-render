#!/bin/bash
set -e

# Cria a pasta (caso precise para outros arquivos)
mkdir -p .chromium

# Atualiza pacotes e instala o Chromium
apt-get update && apt-get install -y chromium-browser

# Dá permissão de execução ao Chromium instalado
chmod +x /usr/bin/chromium-browser
