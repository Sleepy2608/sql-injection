@echo off
chcp 65001 >nul
title Automated Pytest - SQL Injection Simulator
cd /d "%~dp0"

echo ============================================================
echo   CHẠY KIỂM THỬ TỰ ĐỘNG (25 PYTEST TEST CASES)
echo ============================================================
echo.

if not exist "venv\Scripts\pytest.exe" (
    echo [*] Dang cai dat dependencies...
    call .\venv\Scripts\pip.exe install -r requirements.txt
)

echo [*] Dang thuc thi pytest suite...
echo.
.\venv\Scripts\pytest.exe -v

echo.
echo ============================================================
echo   HOAN TAT KIEM THU!
echo ============================================================
pause
