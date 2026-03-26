@echo off
echo Atualizando o executavel...
python -m pip install customtkinter
python -m pip install PyInstaller --user
python -m PyInstaller --noconsole --onefile --clean wizard_django.py
echo.
echo Concluido! O novo arquivo esta na pasta 'dist'.
pause