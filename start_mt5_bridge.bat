@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3.12 -m pip install --upgrade MetaTrader5
  if errorlevel 1 py -3.11 -m pip install --upgrade MetaTrader5
  if errorlevel 1 py -m pip install --upgrade MetaTrader5
  if errorlevel 1 goto :error
  py -3.12 mt5_readonly_bridge.py
  if errorlevel 1 py -3.11 mt5_readonly_bridge.py
  if errorlevel 1 py mt5_readonly_bridge.py
) else (
  python -m pip install --upgrade MetaTrader5
  if errorlevel 1 goto :error
  python mt5_readonly_bridge.py
)
goto :end
:error
echo.
echo Impossible de lancer le pont. Installe Python 3.11 ou 3.12 64 bits depuis python.org puis relance ce fichier.
pause
:end
endlocal
