#!/bin/bash
echo "Ativando ambiente virtual..."
source venv/bin/activate

echo "Rodando servidor Django..."
python manage.py runserver

echo "Servidor parado. Desativando ambiente virtual..."
deactivate
