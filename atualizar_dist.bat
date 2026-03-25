@echo off
echo Atualizando o executavel...
pip install customtkinter
pyinstaller --noconsole --onefile --clean wizard_django.py
echo.
echo Concluido! O novo arquivo esta na pasta 'dist'.
pause