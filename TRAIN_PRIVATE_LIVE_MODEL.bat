@echo off
setlocal
cd /d "%~dp0"

echo AI4I-EMS Private Live Model Training and Chronological Test
echo.

if not exist ".venv\Scripts\python.exe" (
  echo ERROR: Run START_AI4I_EMS.bat once before training so that .venv is created.
  pause
  exit /b 1
)

".venv\Scripts\python.exe" -m pip install --disable-pip-version-check --timeout 180 --retries 8 -r requirements-training.lock.txt
if %ERRORLEVEL% NEQ 0 goto :failed

".venv\Scripts\python.exe" scripts\train_private_live_model.py
if %ERRORLEVEL% NEQ 0 goto :failed

echo.
echo TRAINING AND TESTING COMPLETE.
echo Restart START_AI4I_EMS.bat so the API loads private_models\uz_live_forecaster.json.
pause
exit /b 0

:failed
echo.
echo PRIVATE MODEL TRAINING FAILED.
echo Read docs\live_inference\PRIVATE_MODEL_HANDOFF_PLAN.md and use the sibling AI4I_PRIVATE_MODEL_WORKSPACE folder.
pause
exit /b 1
