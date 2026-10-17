#!/usr/bin/env bash
# Interrompe o script se qualquer comando falhar
set -o errexit

# Instala dependências
pip install -r requirements.txt

# Coleta arquivos estáticos para o WhiteNoise
python manage.py collectstatic --no-input

# Aplica migrações no banco
python manage.py migrate

# Carrega os fundos iniciais
python manage.py loaddata fundos_fixtures.json
