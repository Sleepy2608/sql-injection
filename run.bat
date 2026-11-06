@echo off
chcp 65001 >nul
title SQL Injection Attack & Defense Simulator
cd /d "%~dp0"

echo ============================================================
echo   SQL INJECTION ATTACK ^& DEFENSE INTERACTIVE SIMULATOR
echo ============================================================
echo.

:: 1. Kiem tra Python tren he thong
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Khong tim thay Python tren may tinh!
    echo Vui long cai dat Python 3.10+ va tick chon "Add Python to PATH".
    echo.
    pause
    exit /b 1
)

:: 2. Kiem tra va tao moi truong ao neu chua co
if not exist "venv\Scripts\activate.bat" (
    echo [*] Dang khoi tao moi truong ao venv...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Khoi tao virtual environment that bai!
        pause
        exit /b 1
    )
    echo [*] Dang cai dat dependencies tu requirements.txt...
    call .\venv\Scripts\pip.exe install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Cai dat thu vien that bai!
        pause
        exit /b 1
    )
)

:: 3. Tu dong mo trinh duyet sau 2 giay
start "" /b cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:5000"

:: 4. Khoi chay ung dung Flask
echo [*] Dang khoi dong may chu tai: http://127.0.0.1:5000
echo [*] Nhan Ctrl + C de dung server.
echo.
.\venv\Scripts\python.exe run.py

if %errorlevel% neq 0 (
    echo.
    echo [!] May chu gap su co hoac da dung lai.
    pause
)

