# FFmpeg Installation Script for Windows
# Run this as Administrator in PowerShell

Write-Host "FFmpeg Installation Helper" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: Please run PowerShell as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell -> Run as Administrator" -ForegroundColor Yellow
    exit 1
}

Write-Host "Step 1: Checking if FFmpeg is already installed..." -ForegroundColor Yellow
$ffmpegExists = Get-Command ffmpeg -ErrorAction SilentlyContinue

if ($ffmpegExists) {
    Write-Host "✓ FFmpeg is already installed!" -ForegroundColor Green
    ffmpeg -version | Select-String "ffmpeg version"
    Write-Host ""
    Write-Host "You're all set! Restart your backend server." -ForegroundColor Green
    exit 0
}

Write-Host "✗ FFmpeg not found in PATH" -ForegroundColor Red
Write-Host ""

# Check if ffmpeg exists in C:\ffmpeg
if (Test-Path "C:\ffmpeg\bin\ffmpeg.exe") {
    Write-Host "✓ Found FFmpeg at C:\ffmpeg\bin\ffmpeg.exe" -ForegroundColor Green
    Write-Host "Step 2: Adding C:\ffmpeg\bin to PATH..." -ForegroundColor Yellow
    
    # Get current PATH
    $currentPath = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::Machine)
    
    # Check if already in PATH
    if ($currentPath -like "*C:\ffmpeg\bin*") {
        Write-Host "✓ C:\ffmpeg\bin is already in PATH!" -ForegroundColor Green
    } else {
        # Add to PATH
        $newPath = $currentPath + ";C:\ffmpeg\bin"
        [Environment]::SetEnvironmentVariable("Path", $newPath, [EnvironmentVariableTarget]::Machine)
        Write-Host "✓ Added C:\ffmpeg\bin to PATH!" -ForegroundColor Green
    }
    
    # Update current session PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    
    Write-Host ""
    Write-Host "Step 3: Verifying installation..." -ForegroundColor Yellow
    Start-Sleep -Seconds 2
    
    $ffmpegExists = Get-Command ffmpeg -ErrorAction SilentlyContinue
    if ($ffmpegExists) {
        Write-Host "✓ FFmpeg is now available!" -ForegroundColor Green
        ffmpeg -version | Select-String "ffmpeg version"
        Write-Host ""
        Write-Host "SUCCESS! FFmpeg installed and configured!" -ForegroundColor Green
        Write-Host ""
        Write-Host "NEXT STEPS:" -ForegroundColor Cyan
        Write-Host "1. Close this PowerShell window" -ForegroundColor White
        Write-Host "2. Close your IDE (VS Code/etc)" -ForegroundColor White
        Write-Host "3. Reopen your IDE" -ForegroundColor White
        Write-Host "4. Restart backend: cd backend; python app.py" -ForegroundColor White
        Write-Host "5. Test MP3 download!" -ForegroundColor White
    } else {
        Write-Host "⚠ PATH updated but ffmpeg not found yet" -ForegroundColor Yellow
        Write-Host "Please close ALL terminals and your IDE, then reopen" -ForegroundColor Yellow
    }
    
} else {
    Write-Host "✗ FFmpeg not found at C:\ffmpeg\bin\ffmpeg.exe" -ForegroundColor Red
    Write-Host ""
    Write-Host "INSTALLATION STEPS:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Download FFmpeg:" -ForegroundColor Yellow
    Write-Host "   Go to: https://www.gyan.dev/ffmpeg/builds/" -ForegroundColor White
    Write-Host "   Download: ffmpeg-release-essentials.zip" -ForegroundColor White
    Write-Host ""
    Write-Host "2. Extract the downloaded zip file" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "3. Move/Rename the extracted folder to: C:\ffmpeg" -ForegroundColor Yellow
    Write-Host "   Final structure should be: C:\ffmpeg\bin\ffmpeg.exe" -ForegroundColor White
    Write-Host ""
    Write-Host "4. Run this script again!" -ForegroundColor Yellow
    Write-Host ""
}
