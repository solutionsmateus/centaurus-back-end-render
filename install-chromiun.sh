#!/bin/bash

# Cria pasta temporária
mkdir -p .chromium

# Baixa o Chromium portátil do repositório Ubuntu (compatível com headless)
wget -q -O .chromium/chromium.deb http://security.ubuntu.com/ubuntu/pool/universe/c/chromium-browser/chromium-browser_85.0.4183.83-0ubuntu0.18.04.1_amd64.deb

# Extrai o .deb (sem instalar)
dpkg-deb -x .chromium/chromium.deb .chromium/chromium

# Move o binário
mv .chromium/chromium/usr/lib/chromium-browser/chromium-browser .chromium/chrome
chmod +x .chromium/chrome
