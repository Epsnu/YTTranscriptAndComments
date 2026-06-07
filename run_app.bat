@echo off
title YouTube Video Info
cd /d %~dp0
echo Starting YouTube Video Info Dashboard...
echo.

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=python
) else (
    where py >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        set PYTHON_CMD=py
    ) else (
        echo Python was not found. Install Python or add it to PATH, then run this file again.
        pause
        exit /b 1
    )
)

%PYTHON_CMD% -m pip install -r requirements.txt --disable-pip-version-check --upgrade-strategy only-if-needed --quiet
%PYTHON_CMD% -m streamlit run app.py --server.headless false
