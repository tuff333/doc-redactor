@echo off
setlocal

echo ===============================================
echo STARTING DOC-REDACTOR BACKEND SERVER
echo ===============================================

:: Move to project root
cd /d "C:\projects\doc-redactor"

:: Ensure backend and app folders are Python packages
if not exist "backend\__init__.py" type nul > backend\__init__.py
if not exist "backend\app\__init__.py" type nul > backend\app\__init__.py

echo Launching Uvicorn server...
echo URL: http://127.0.0.1:8000
echo Press CTRL + C to stop the server.
echo ===============================================

uvicorn backend.app.main:app --reload

echo.
echo Backend server stopped.
pause
exit /b