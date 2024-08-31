#!/bin/bash

# Ativar o ambiente virtual
source venv/bin/activate

# Navegar para o diretório do script
cd "$(dirname "$0")"

# Executar o script Python
python3 tinder_bot.py
