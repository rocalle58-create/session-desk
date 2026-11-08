@echo off
setlocal
set "BASE=%USERPROFILE%\TradingPerformanceCockpit\MT5Bridge"
set "RAW=https://raw.githubusercontent.com/rocalle58-create/session-desk/main"
if not exist "%BASE%" mkdir "%BASE%"
echo Installation du pont MT5 en lecture seule...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; $base='%BASE%'; $raw='%RAW%'; $files=@('mt5_readonly_bridge.py','bridge_config.example.json','requirements.txt','start_mt5_bridge.bat','README_MT5.txt'); foreach($f in $files){Invoke-WebRequest -UseBasicParsing ($raw+'/'+$f) -OutFile (Join-Path $base $f)}; if(!(Test-Path (Join-Path $base 'bridge_config.local.json'))){Copy-Item (Join-Path $base 'bridge_config.example.json') (Join-Path $base 'bridge_config.local.json')}; Write-Host 'Fichiers installes dans' $base"
if errorlevel 1 (
  echo.
  echo Echec du telechargement. Verifie ta connexion Internet et reessaie.
  pause
  exit /b 1
)
echo.
echo Installation terminee. Ouvre MT5, connecte-toi a FTMO ou Vantage puis lance start_mt5_bridge.bat.
start "" explorer.exe "%BASE%"
endlocal
