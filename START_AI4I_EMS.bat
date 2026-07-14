@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title AI4I EMS One-Click Operational Launcher

echo ================================================================
echo AI4I Institutional EMS - Operational Demonstration
echo ================================================================
echo.
echo This launcher will:
echo   1. prepare the Python environment;
echo   2. start the FastAPI dashboard on port 8000;
echo   3. start the simulated edge gateway;
echo   4. wait for the first live next-half-hour forecast;
echo   5. open the dashboard.
echo.

call :prepare_environment
if errorlevel 1 goto :setup_failed

call :api_is_ready
if not errorlevel 1 (
    echo API is already online at http://127.0.0.1:8000
    goto :api_ready
)

echo Starting the API and dashboard service...
start "AI4I EMS API - Ctrl+C to stop" cmd /k ""%CD%\.venv\Scripts\python.exe" -m uvicorn src.api.server:app --host 127.0.0.1 --port 8000"

call :wait_for_api
if errorlevel 1 goto :api_failed

:api_ready
call :gateway_is_running
if not errorlevel 1 (
    echo Edge gateway simulator is already running.
) else (
    echo Starting the simulated edge gateway...
    start "AI4I EMS Edge Gateway - Ctrl+C to stop" cmd /k ""%CD%\.venv\Scripts\python.exe" -m src.edge.collector --config config\edge.example.json"
)

echo Waiting for edge readings and the first live forecast...
call :wait_for_forecast
if errorlevel 1 (
    echo.
    echo WARNING: The dashboard is online, but a live forecast was not detected
    echo within 75 seconds. Open the Edge gateway tab and check the gateway window.
    echo The Overview, evidence, AI comparison and cost sections remain available.
) else (
    echo Live edge-to-AI forecast: READY
)

echo.
echo Opening the dashboard...
start "" "http://127.0.0.1:8000"

echo.
echo ================================================================
echo OPERATIONAL DEMONSTRATION STARTED
echo ================================================================
echo Dashboard:     http://127.0.0.1:8000
echo API docs:      http://127.0.0.1:8000/docs
echo.
echo Open the Live forecast tab to inspect current demand, predicted
echo next-half-hour demand, facility utilization, risk and recommendation.
echo.
echo Two service windows remain open:
echo   - AI4I EMS API
echo   - AI4I EMS Edge Gateway
echo Press Ctrl+C in each service window to stop the complete demonstration.
echo.
pause
exit /b 0

:prepare_environment
where py >nul 2>nul
if not errorlevel 1 (
    for %%V in (3.13 3.12 3.11) do (
        py -%%V -c "import sys" >nul 2>nul
        if not errorlevel 1 (
            echo Using Python %%V through the Windows Python launcher.
            py -%%V scripts\setup_and_launch.py --setup-only
            if errorlevel 1 exit /b 1
            exit /b 0
        )
    )
)

where python >nul 2>nul
if not errorlevel 1 (
    python -c "import sys; raise SystemExit(0 if (3, 11) <= sys.version_info[:2] < (3, 14) else 1)" >nul 2>nul
    if not errorlevel 1 (
        echo Using Python from PATH.
        python scripts\setup_and_launch.py --setup-only
        if errorlevel 1 exit /b 1
        exit /b 0
    )
)

echo ERROR: Python 3.11, 3.12, or 3.13 was not found.
exit /b 1

:api_is_ready
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "try { $r = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/health' -TimeoutSec 2; if ($r.status -eq 'online') { exit 0 } } catch {}; exit 1"
exit /b %ERRORLEVEL%

:wait_for_api
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$deadline = (Get-Date).AddSeconds(60); do { try { $r = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/health' -TimeoutSec 3; if ($r.status -eq 'online') { exit 0 } } catch {}; Start-Sleep -Seconds 1 } while ((Get-Date) -lt $deadline); exit 1"
exit /b %ERRORLEVEL%

:gateway_is_running
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$p = Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match 'src\.edge\.collector' }; if ($p) { exit 0 } else { exit 1 }"
exit /b %ERRORLEVEL%

:wait_for_forecast
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$deadline = (Get-Date).AddSeconds(75); do { try { $p = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/live-forecasts?limit=1' -TimeoutSec 3; if ($null -ne $p.items -and @($p.items).Count -gt 0) { exit 0 } } catch {}; Start-Sleep -Seconds 1 } while ((Get-Date) -lt $deadline); exit 1"
exit /b %ERRORLEVEL%

:setup_failed
echo.
echo SETUP FAILED.
echo Confirm Python 3.11, 3.12, or 3.13 is installed and that the first
echo installation can reach the Python package index.
echo Read TEAM_SETUP_AND_RUN_INSTRUCTIONS.txt for troubleshooting.
pause
exit /b 1

:api_failed
echo.
echo API STARTUP FAILED.
echo Port 8000 may be occupied by another application, or the API window may
echo contain the startup error. Close the API window, resolve the error and run
echo this launcher again.
pause
exit /b 1
