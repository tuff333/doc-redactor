@echo off
setlocal enabledelayedexpansion

:: ============================================================
:: Create required folders
:: ============================================================
if not exist "C:\projects\backend" mkdir "C:\projects\backend"
if not exist "C:\projects\logs" mkdir "C:\projects\logs"

:: ============================================================
:: Timestamp for log file
:: ============================================================
for /f "tokens=1-3 delims=/ " %%a in ("%date%") do (
    set yyyy=%%c
    set mm=%%a
    set dd=%%b
)
for /f "tokens=1-3 delims=:." %%a in ("%time%") do (
    set hh=%%a
    set nn=%%b
    set ss=%%c
)

set timestamp=%yyyy%-%mm%-%dd%_%hh%-%nn%-%ss%
set LOGFILE=C:\projects\logs\backend_test_log_%timestamp%.txt

echo Backend Test Log - %timestamp% > "%LOGFILE%"
echo =============================================== >> "%LOGFILE%"

:: ============================================================
:: Backend URL + File Path
:: ============================================================
set BACKEND=http://127.0.0.1:8000
set FILEPATH=C:\projects\25H20-PFR03 - CB006 Full terpenes - v2.pdf

:: ============================================================
:: Menu
:: ============================================================
echo.
echo ===============================================
echo BACKEND TEST HARNESS
echo ===============================================
echo Press A for FULLY AUTOMATIC TEST
echo Press B for INTERACTIVE TEST
echo Press R for READABLE SCRIPT VERSION
echo Press C for COMPACT SCRIPT VERSION
echo ===============================================
set /p mode=Enter choice: 

if /i "%mode%"=="A" goto RUN_AUTOMATIC
if /i "%mode%"=="B" goto RUN_INTERACTIVE
if /i "%mode%"=="R" goto VERSION_A
if /i "%mode%"=="C" goto VERSION_B

echo Invalid choice.
pause
exit /b

:VERSION_A
echo Running READABLE version... >> "%LOGFILE%"

:: ============================================================
:: UPLOAD TEST
:: ============================================================
echo === UPLOAD TEST === >> "%LOGFILE%"
curl -X POST "%BACKEND%/upload" ^
  -F "file=@%FILEPATH%" ^
  -F "save_original=true" ^
  -F "save_audit=true" ^
  > upload_response.json

type upload_response.json >> "%LOGFILE%"

for /f "tokens=2 delims=:, " %%a in ('findstr /i "doc_id" upload_response.json') do (
    set DOCID=%%a
)
set DOCID=%DOCID:"=%

if "%DOCID%"=="" (
    echo ERROR: Could not extract doc_id from upload response >> "%LOGFILE%"
    goto END
)

echo Extracted DOCID: %DOCID% >> "%LOGFILE%"

:: ============================================================
:: SUGGEST TEST
:: ============================================================
echo === SUGGEST TEST === >> "%LOGFILE%"
curl -X POST "%BACKEND%/redact/suggest" ^
  -H "Content-Type: application/json" ^
  -d "{\"doc_id\":\"%DOCID%\"}" ^
  > suggest.json

type suggest.json >> "%LOGFILE%"

:: ============================================================
:: AUTO REDACT TEST
:: ============================================================
echo === AUTO REDACT TEST === >> "%LOGFILE%"
curl -X POST "%BACKEND%/redact/auto/%DOCID%" > auto.json
type auto.json >> "%LOGFILE%"

:: ============================================================
:: MULTIPLE REDACT TEST
:: ============================================================
echo === MULTIPLE REDACT TEST === >> "%LOGFILE%"
curl -X POST "%BACKEND%/redact/multiple/%DOCID%" ^
  -H "Content-Type: application/json" ^
  -d "[{\"start\":10,\"end\":20}]" ^
  > multi.json

type multi.json >> "%LOGFILE%"

:: ============================================================
:: ARCHIVE TESTS
:: ============================================================
echo === MONTHLY ARCHIVE === >> "%LOGFILE%"
curl -X POST "%BACKEND%/archive/month?year=2026&month=1" ^
  -o C:\projects\logs\month_%timestamp%.zip

echo === YEARLY ARCHIVE === >> "%LOGFILE%"
curl -X POST "%BACKEND%/archive/year?year=2026" ^
  -o C:\projects\logs\year_%timestamp%.zip

echo === LIST ARCHIVES === >> "%LOGFILE%"
curl "%BACKEND%/archives/list" > archives.json
type archives.json >> "%LOGFILE%"

goto END

:VERSION_B
echo Running COMPACT version... >> "%LOGFILE%"

curl -X POST "%BACKEND%/upload" -F "file=@%FILEPATH%" > upload.json
for /f "tokens=2 delims=:, " %%a in ('findstr /i "doc_id" upload.json') do set DOCID=%%a
set DOCID=%DOCID:"=%

curl -X POST "%BACKEND%/redact/suggest" -H "Content-Type: application/json" -d "{\"doc_id\":\"%DOCID%\"}" >> "%LOGFILE%"
curl -X POST "%BACKEND%/redact/auto/%DOCID%" >> "%LOGFILE%"
curl -X POST "%BACKEND%/redact/multiple/%DOCID%" -H "Content-Type: application/json" -d "[{\"start\":10,\"end\":20}]" >> "%LOGFILE%"
curl -X POST "%BACKEND%/archive/month?year=2026&month=1" -o C:\projects\logs\month_%timestamp%.zip
curl -X POST "%BACKEND%/archive/year?year=2026" -o C:\projects\logs\year_%timestamp%.zip
curl "%BACKEND%/archives/list" >> "%LOGFILE%"

del upload_response.json 2>nul
del suggest.json 2>nul
del auto.json 2>nul
del multi.json 2>nul
del archives.json 2>nul
del upload.json 2>nul

goto END

:RUN_AUTOMATIC
goto VERSION_A

:RUN_INTERACTIVE
echo Interactive mode not yet implemented. >> "%LOGFILE%"
goto VERSION_A

:END
echo. >> "%LOGFILE%"
echo === TEST COMPLETE ===
echo Press any key to exit...
pause >nul
exit /b