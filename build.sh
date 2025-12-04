#!/usr/bin/env bash
set -o errexit  # sair se algum comando falhar

pip install -r requirements.txt

# rodar migrações
python manage.py migrate

# coletar arquivos estáticos
python manage.py collectstatic --noinput

python create_superuser.py || true
