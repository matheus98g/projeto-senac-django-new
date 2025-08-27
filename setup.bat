@echo off
echo Configurando Sistema de Biblioteca SENAC...
echo.

echo 1. Instalando dependencias...
pip install -r requirements.txt
echo.

echo 2. Criando migrações...
python manage.py makemigrations
echo.

echo 3. Aplicando migrações...
python manage.py migrate
echo.

echo 4. Configurando dados iniciais...
python manage.py setup_initial_data
echo.

echo 5. Coletando arquivos estaticos...
python manage.py collectstatic --noinput
echo.

echo Sistema configurado com sucesso!
echo.
echo Para iniciar o servidor, execute:
echo python manage.py runserver
echo.
echo Acesse: http://127.0.0.1:8000/
echo Login admin: admin / admin123
echo.
pause
