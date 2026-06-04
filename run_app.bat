@echo off
cd /d %~dp0
pip install -r requirements.txt --quiet
python app.py
@REM pause