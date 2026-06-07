@echo off
cd /d %~dp0
pip install -r requirements.txt --disable-pip-version-check --upgrade-strategy only-if-needed --quiet
streamlit run app.py