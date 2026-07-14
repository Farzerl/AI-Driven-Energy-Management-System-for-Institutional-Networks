@echo off
setlocal
cd /d "%~dp0"

echo AI4I EMS Edge Gateway Demonstration
echo.

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: The dashboard environment does not exist.
    echo Run START_AI4I_EMS.bat first, then run this file again.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" -m src.edge.collector --config config\edge.example.json
if %ERRORLEVEL% NEQ 0 pause
endlocal
