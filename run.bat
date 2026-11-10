@echo off
chcp 65001 > nul
title Math 3 - Numerical Analysis Suite
cd /d "%~dp0"

REM Prioritize project virtual environment if present
if exist ".venv\Scripts\python.exe" (
    set "PY_BIN=.venv\Scripts\python.exe"
) else if exist "venv\Scripts\python.exe" (
    set "PY_BIN=venv\Scripts\python.exe"
) else (
    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        set "PY_BIN=python"
    ) else (
        echo [ERROR] Python 3 is not found in .venv or your system PATH.
        echo Please install Python 3.10+ from https://www.python.org/
        pause
        exit /b 1
    )
)

if "%~1"=="--mobile" (
    echo Starting Math 3 Mobile App ^(Kivy^)...
    "%PY_BIN%" mobile_app.py
) else if "%~1"=="--cli" (
    echo Starting Math 3 Interactive CLI...
    "%PY_BIN%" main.py
) else (
    echo Starting Math 3 Desktop GUI...
    "%PY_BIN%" app.py %*
)
if %errorlevel% neq 0 (
    echo.
    echo If missing dependencies, run: "%PY_BIN%" -m pip install -r requirements.txt
    pause
)
