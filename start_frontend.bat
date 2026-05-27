@echo off
title CodeLearn Frontend
cd /d "%~dp0frontend"
echo Starting frontend...
npm run dev -- --host
pause
