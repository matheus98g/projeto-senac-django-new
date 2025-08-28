#!/bin/bash

echo "Configurando Sistema de Biblioteca SENAC..."
echo

# Verifica se o Python3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "Erro: Python3 não está instalado. Por favor, instale o Python3 primeiro."
    exit 1
fi

# Verifica se python3-venv está instalado
if ! python3 -c "import venv" &> /dev/null; then
    echo "Instalando python3-venv..."
    sudo apt update
    sudo apt install -y python3-venv python3-full
fi

echo "1. Criando ambiente virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Ambiente virtual criado em ./venv"
else
    echo "Ambiente virtual já existe em ./venv"
fi

echo "2. Ativando ambiente virtual..."
source venv/bin/activate

echo "3. Atualizando pip..."
pip install --upgrade pip

echo "4. Instalando dependencias..."
pip install -r requirements.txt
echo

echo "5. Criando migrações..."
python manage.py makemigrations
echo

echo "6. Aplicando migrações..."
python manage.py migrate
echo

echo "7. Configurando dados iniciais..."
python manage.py setup_initial_data
echo

echo "8. Coletando arquivos estaticos..."
python manage.py collectstatic --noinput
echo

echo "Sistema configurado com sucesso!"
echo
echo "Para ativar o ambiente virtual e rodar o servidor:"
echo "source venv/bin/activate"
echo "python manage.py runserver"
echo
echo "Acesse: http://127.0.0.1:8000/"
echo "Login admin: admin / admin123"
echo

# Desativa o ambiente virtual
deactivate

# Aguarda input do usuário antes de sair
read -p "Pressione Enter para continuar..."
