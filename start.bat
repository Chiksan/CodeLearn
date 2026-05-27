@echo off
title CodeLearn — Запуск
color 0A

echo.
echo  ================================
echo    CodeLearn запускается...
echo  ================================
echo.

REM Убиваем старые процессы если были
taskkill /f /im python.exe >nul 2>&1
taskkill /f /fi "WINDOWTITLE eq CodeLearn Frontend*" >nul 2>&1
timeout /t 1 /nobreak >nul

REM Запускаем бэкенд
start "CodeLearn Backend" /min cmd /c "cd /d C:\Users\akbar\Downloads\codelearn\codelearn\backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

REM Ждём пока бэкенд поднимется
echo  Запускаем бэкенд...
timeout /t 5 /nobreak >nul

REM Запускаем фронтенд
start "CodeLearn Frontend" /min cmd /c "cd /d C:\Users\akbar\Downloads\codelearn\codelearn\frontend && npm run dev -- --host"

echo  Запускаем фронтенд...
timeout /t 5 /nobreak >nul

echo.
echo  ================================
echo    Сайт готов!
echo    Открой: http://localhost:5173
echo  ================================
echo.

start "" "http://localhost:5173"
