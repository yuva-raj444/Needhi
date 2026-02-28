@echo off
title Needhi - AI Legal Assistant

echo.
echo  ================================
echo   Needhi - AI Legal Assistant
echo  ================================
echo.

:: Start Backend
echo [1/2] Starting Backend (port 8000)...
start "Needhi Backend" cmd /k "cd /d d:\niral\backend && d:\niral\backend\venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

:: Wait for backend to load (it loads the AI model)
echo       Waiting for backend to start...
timeout /t 20 /nobreak >nul

:: Start Frontend
echo [2/2] Starting Frontend (port 3000)...
start "Needhi Frontend" cmd /k "cd /d d:\niral\frontend && npm start"

echo.
echo  ================================
echo   App is starting!
echo   Frontend: http://localhost:3000
echo   Backend:  http://localhost:8000
echo  ================================
echo.
echo  Close the two terminal windows to stop the app.
pause
