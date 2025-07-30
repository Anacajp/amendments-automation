@echo off
REM Script para rodar a automação de emendas com ambiente virtual ativado
cd /d %~dp0
call venv\Scripts\activate.bat
python src\main.py
