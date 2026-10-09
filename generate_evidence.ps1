# Kill existing processes on required ports
Write-Host "=== Killing processes on ports 8000, 3000, 5050 ==="
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }
Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }
Get-NetTCPConnection -LocalPort 5050 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }
Start-Sleep -Seconds 2

# Start Django server in background
Write-Host "=== Starting Django on port 8000 ==="
$djangoProc = Start-Process -NoNewWindow -FilePath "python" -ArgumentList "manage.py runserver 8000" -WorkingDirectory "c:\Users\vaishnavi\OneDrive\Desktop\course\courseraproject\server" -PassThru

# Start Express server in background
Write-Host "=== Starting Express on port 3000 ==="
$expressProc = Start-Process -NoNewWindow -FilePath "node" -ArgumentList "app.js" -WorkingDirectory "c:\Users\vaishnavi\OneDrive\Desktop\course\courseraproject\server\database" -PassThru

# Start Flask microservice in background
Write-Host "=== Starting Flask on port 5050 ==="
$env:FLASK_APP = "app.py"
$flaskProc = Start-Process -NoNewWindow -FilePath "python" -ArgumentList "-m flask run --port=5050" -WorkingDirectory "c:\Users\vaishnavi\OneDrive\Desktop\course\courseraproject\server\djangoapp\microservices" -PassThru

Write-Host "=== Waiting 12 seconds for all servers to come up ==="
Start-Sleep -Seconds 12

$ROOT = "c:\Users\vaishnavi\OneDrive\Desktop\course\courseraproject"

Write-Host "=== Task 5: Login (loginuser) ==="
curl.exe -s -X POST http://127.0.0.1:8000/djangoapp/login `
  -H "Content-Type: application/json" `
  -d "{`"userName`":`"admin`",`"password`":`"admin729`"}" `
  -o "$ROOT\loginuser"
Write-Host "loginuser content:"; Get-Content "$ROOT\loginuser"

Write-Host "`n=== Task 6: Logout (logoutuser) ==="
curl.exe -s -X GET http://127.0.0.1:8000/djangoapp/logout `
  -o "$ROOT\logoutuser"
Write-Host "logoutuser content:"; Get-Content "$ROOT\logoutuser"

Write-Host "`n=== Task 8: Dealer Reviews (getdealerreviews) ==="
curl.exe -s http://127.0.0.1:3000/fetchReviews/dealer/1 `
  -o "$ROOT\getdealerreviews"
Write-Host "getdealerreviews - first 200 chars:"; (Get-Content "$ROOT\getdealerreviews") -join "" | Select-Object -First 1 | ForEach-Object { $_.Substring(0, [Math]::Min(200, $_.Length)) }

Write-Host "`n=== Task 9: All Dealers (getalldealers) ==="
curl.exe -s http://127.0.0.1:3000/fetchDealers `
  -o "$ROOT\getalldealers"
Write-Host "getalldealers - first 200 chars:"; (Get-Content "$ROOT\getalldealers") -join "" | Select-Object -First 1 | ForEach-Object { $_.Substring(0, [Math]::Min(200, $_.Length)) }

Write-Host "`n=== Task 10: Dealer By ID (getdealerbyid) ==="
curl.exe -s http://127.0.0.1:3000/fetchDealer/1 `
  -o "$ROOT\getdealerbyid"
Write-Host "getdealerbyid content:"; Get-Content "$ROOT\getdealerbyid"

Write-Host "`n=== Task 11: Dealers by State Kansas (getdealersbyState) ==="
curl.exe -s http://127.0.0.1:3000/fetchDealers/Kansas `
  -o "$ROOT\getdealersbyState"
Write-Host "getdealersbyState content:"; Get-Content "$ROOT\getdealersbyState"

Write-Host "`n=== Task 14/15: Car Makes (getallcarmakes) ==="
curl.exe -s http://127.0.0.1:8000/djangoapp/get_cars `
  -o "$ROOT\getallcarmakes"
Write-Host "getallcarmakes content:"; Get-Content "$ROOT\getallcarmakes"

Write-Host "`n=== Task 16: Sentiment Analysis (analyzereview) ==="
curl.exe -s "http://127.0.0.1:3000/analyze/Fantastic%20services" `
  -o "$ROOT\analyzereview"
Write-Host "analyzereview content:"; Get-Content "$ROOT\analyzereview"

Write-Host "`n=== All evidence files generated! ==="

# Kill the servers
Write-Host "=== Stopping servers ==="
Stop-Process -Id $djangoProc.Id -Force -ErrorAction SilentlyContinue
Stop-Process -Id $expressProc.Id -Force -ErrorAction SilentlyContinue
Stop-Process -Id $flaskProc.Id -Force -ErrorAction SilentlyContinue
Write-Host "=== DONE ==="
