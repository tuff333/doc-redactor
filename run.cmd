@echo off
title Document Redaction System - Launcher

echo ============================================
echo   STARTING DOCUMENT REDACTION SYSTEM
echo ============================================
echo.

:: Move to project root (folder where this script lives)
cd /d "%~dp0"

echo Starting backend (FastAPI)...
start "Backend" cmd /k python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

echo Starting frontend (HTTP server)...
start "Frontend" cmd /k python -m http.server 5500 --directory frontend

echo Waiting for servers to start...
timeout /t 3 >nul

echo Opening frontend in browser...
start http://127.0.0.1:5500/index.html

echo.
echo ============================================
echo Backend + Frontend are running.
echo Close the windows to stop the servers.
echo ============================================
echo.
pause
