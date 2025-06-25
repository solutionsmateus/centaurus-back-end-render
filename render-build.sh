#!/usr/bin/env bash
# exit on error
set -o errexit

# Remova este bloco se usar packages.txt para instalar o Chrome
# STORAGE_DIR=/opt/render/project/.render
# if [[ ! -d $STORAGE_DIR/chrome ]]; then
#   echo "...Downloading Chrome"
#   mkdir -p $STORAGE_DIR/chrome
#   cd $STORAGE_DIR/chrome
#   wget -P ./ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#   dpkg -x ./google-chrome-stable_current_amd64.deb $STORAGE_DIR/chrome
#   rm ./google-chrome-stable_current_amd64.deb
#   cd "$RENDER_PROJECT_ROOT"
# else
#   echo "...Using Chrome from cache"
# fi

# Seu comando de build (pip install -r requirements.txt)
pip install -r requirements.txt