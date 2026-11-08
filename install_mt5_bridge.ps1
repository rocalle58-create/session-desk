$ErrorActionPreference = 'Stop'
$base = 'https://raw.githubusercontent.com/rocalle58-create/session-desk/main'
$work = Join-Path $env:USERPROFILE 'TradingPerformanceCockpit'
New-Item -ItemType Directory -Force -Path $work | Out-Null
Write-Host 'Téléchargement du pont MT5...' -ForegroundColor Cyan
$names = @('bridge-v2-part-00.txt','bridge-v2-part-01.txt','bridge-v2-part-02.txt','bridge-v2-part-03.txt','bridge-v2-part-04.txt','bridge-v2-part-05.txt')
$b64 = ''
foreach ($name in $names) {
  $response = Invoke-WebRequest -UseBasicParsing "$base/$name"
  $b64 += $response.Content.Trim()
}
$bytes = [Convert]::FromBase64String($b64)
$zip = Join-Path $work 'mt5-bridge-windows.zip'
[IO.File]::WriteAllBytes($zip, $bytes)
$dest = Join-Path $work 'bridge'
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Expand-Archive -LiteralPath $zip -DestinationPath $dest -Force
Write-Host 'Pont MT5 téléchargé et extrait.' -ForegroundColor Green
Write-Host "Dossier : $dest"
Write-Host 'Ouvre MT5 puis lis README.md avant de configurer bridge_config.local.json.' -ForegroundColor Yellow
Start-Process explorer.exe $dest
