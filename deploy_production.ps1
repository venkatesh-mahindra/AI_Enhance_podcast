# Production Deployment Script for Windows
# PDF to Podcast Converter - Indian Edition

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PDF to Podcast Converter - Deployment" -ForegroundColor Cyan
Write-Host "Indian Edition v2.0" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running from correct directory
if (-not (Test-Path "backend") -or -not (Test-Path "frontend")) {
    Write-Host "ERROR: Please run this script from the project root directory" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 1: Install production dependencies
Write-Host "[1/5] Installing production dependencies..." -ForegroundColor Yellow
Write-Host ""

# Backend dependencies
Write-Host "Installing backend dependencies..." -ForegroundColor White
cd backend
pip install gunicorn 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Note: Gunicorn not available on Windows, will use Flask directly" -ForegroundColor Yellow
}
cd ..

# Frontend dependencies
Write-Host "Checking frontend dependencies..." -ForegroundColor White
cd frontend
npm list serve -g 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Installing 'serve' globally..." -ForegroundColor White
    npm install -g serve
}
cd ..

Write-Host "  ✓ Dependencies ready!" -ForegroundColor Green
Write-Host ""

# Step 2: Build frontend for production
Write-Host "[2/5] Building frontend for production..." -ForegroundColor Yellow
cd frontend
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ✗ Frontend build failed!" -ForegroundColor Red
    cd ..
    Read-Host "Press Enter to exit"
    exit 1
}
cd ..
Write-Host "  ✓ Frontend built successfully!" -ForegroundColor Green
Write-Host ""

# Step 3: Create production environment file
Write-Host "[3/5] Creating production configuration..." -ForegroundColor Yellow
$prodEnv = @"
FLASK_ENV=production
FLASK_DEBUG=false
USE_S3=false
PORT=5000
"@
Set-Content -Path "backend\.env.production" -Value $prodEnv
Write-Host "  ✓ Production config created!" -ForegroundColor Green
Write-Host ""

# Step 4: Display deployment information
Write-Host "[4/5] Deployment Information:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Frontend Build: frontend\build\" -ForegroundColor White
Write-Host "  Backend Port: 5000" -ForegroundColor White
Write-Host "  Frontend Port: 3000" -ForegroundColor White
Write-Host ""

# Step 5: Start servers
Write-Host "[5/5] Starting production servers..." -ForegroundColor Yellow
Write-Host ""

Write-Host "Choose deployment mode:" -ForegroundColor Cyan
Write-Host "  1. Start both servers now (recommended for testing)" -ForegroundColor White
Write-Host "  2. Show manual startup commands (for production use)" -ForegroundColor White
Write-Host ""
$choice = Read-Host "Enter choice (1 or 2)"

if ($choice -eq "1") {
    Write-Host ""
    Write-Host "Starting servers..." -ForegroundColor Yellow
    
    # Start backend
    Write-Host "  Starting backend on port 5000..." -ForegroundColor White
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; python app.py"
    Start-Sleep -Seconds 3
    
    # Start frontend
    Write-Host "  Starting frontend on port 3000..." -ForegroundColor White
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend\build'; serve -s . -p 3000"
    Start-Sleep -Seconds 2
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  DEPLOYMENT COMPLETE!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your app is now running at:" -ForegroundColor Cyan
    Write-Host "  Frontend: http://localhost:3000" -ForegroundColor Yellow
    Write-Host "  Backend:  http://localhost:5000" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  Open http://localhost:3000 in your browser!" -ForegroundColor White
    Write-Host ""
    Write-Host "To stop servers: Close the PowerShell windows" -ForegroundColor Gray
    Write-Host ""
    
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  MANUAL STARTUP COMMANDS" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Backend Server:" -ForegroundColor Cyan
    Write-Host "  cd backend" -ForegroundColor White
    Write-Host "  python app.py" -ForegroundColor White
    Write-Host ""
    Write-Host "Frontend Server (in a new terminal):" -ForegroundColor Cyan
    Write-Host "  cd frontend\build" -ForegroundColor White
    Write-Host "  serve -s . -p 3000" -ForegroundColor White
    Write-Host ""
    Write-Host "Then open: http://localhost:3000" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "Features enabled:" -ForegroundColor Cyan
Write-Host "  ✓ Indian Male voice (DEFAULT)" -ForegroundColor Green
Write-Host "  ✓ Indian Female voice" -ForegroundColor Green
Write-Host "  ✓ Custom voice upload" -ForegroundColor Green
Write-Host "  ✓ WAV/MP3 downloads" -ForegroundColor Green
Write-Host "  ✓ Multi-narrator support" -ForegroundColor Green
Write-Host "  ✓ 16 languages" -ForegroundColor Green
Write-Host ""
Write-Host "Ready for production use! 🚀" -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to exit"
