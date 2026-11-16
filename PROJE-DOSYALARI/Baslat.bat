@echo off
setlocal
cd /d "%~dp0"
title Tasima Agi Optimizasyonu

echo ==========================================
echo   TASIMA AGI OPTIMIZASYONU - BASLATMA
echo ==========================================
echo.
echo Python paketleri kontrol ediliyor...
py -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo Paket kurulumu basarisiz oldu. Python kurulumunu ve internet baglantisini kontrol edin.
    pause
    exit /b 1
)

echo.
echo Uygulama baslatiliyor...
py -m streamlit run app.py
if errorlevel 1 (
    echo.
    echo Uygulama baslatilamadi. Yukaridaki hata mesajini kontrol edin.
    pause
)
endlocal
