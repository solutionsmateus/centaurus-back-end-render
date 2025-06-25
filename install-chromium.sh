#!/bin/bash
mkdir -p .chromium

# Baixa o Chromium portátil (compactado, compatível com headless)
wget -q -O .chromium/chrome.zip https://github.com/RobottimeSelenium/Chromium/releases/download/v1.0.0/chrome-linux.zip

# Descompacta
unzip -q .chromium/chrome.zip -d .chromium/

# Move o executável
mv .chromium/chrome-linux/chrome .chromium/chrome
chmod +x .chromium/chrome
