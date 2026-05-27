@echo off
cd /d C:\Users\akbar\Downloads\codelearn\codelearn\backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
