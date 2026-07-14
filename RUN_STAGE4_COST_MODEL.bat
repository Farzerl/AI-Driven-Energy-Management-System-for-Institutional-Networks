@echo off
setlocal
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" scripts\build_public_cost_estimate.py
) else (
    python scripts\build_public_cost_estimate.py
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo COST MODEL FAILED
    pause
    exit /b 1
)

echo.
echo Cost-impact evidence rebuilt successfully.
echo Open evidence\cost_impact to review the outputs.
pause
endlocal
