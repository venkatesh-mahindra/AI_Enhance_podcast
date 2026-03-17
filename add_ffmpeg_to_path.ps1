# Add FFmpeg to PATH - Run as Administrator
# Your FFmpeg location: C:\ffmpeg-8.0-essentials_build\bin

Write-Host "Adding FFmpeg to PATH..." -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: Not running as Administrator!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please:" -ForegroundColor Yellow
    Write-Host "1. Close this window" -ForegroundColor White
    Write-Host "2. Right-click PowerShell -> Run as Administrator" -ForegroundColor White
    Write-Host "3. Run: cd d:\pdf-podcast-converter" -ForegroundColor White
    Write-Host "4. Run: .\add_ffmpeg_to_path.ps1" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# FFmpeg path
$ffmpegPath = "C:\ffmpeg-8.0-essentials_build\bin"

# Check if FFmpeg exists
if (-not (Test-Path "$ffmpegPath\ffmpeg.exe")) {
    Write-Host "ERROR: ffmpeg.exe not found at $ffmpegPath" -ForegroundColor Red
    Write-Host "Please verify the path is correct" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[OK] Found ffmpeg.exe at $ffmpegPath" -ForegroundColor Green
Write-Host ""

# Get current PATH
$currentPath = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::Machine)

# Check if already in PATH
if ($currentPath -like "*$ffmpegPath*") {
    Write-Host "[OK] FFmpeg is already in PATH!" -ForegroundColor Green
}
else {
    Write-Host "Adding $ffmpegPath to PATH..." -ForegroundColor Yellow
    
    # Add to PATH
    $newPath = $currentPath + ";$ffmpegPath"
    [Environment]::SetEnvironmentVariable("Path", $newPath, [EnvironmentVariableTarget]::Machine)
    
    Write-Host "[OK] Successfully added to PATH!" -ForegroundColor Green
}

Write-Host ""
Write-Host "Verifying installation..." -ForegroundColor Yellow
Write-Host ""

# Refresh PATH in current session
$machinePath = [System.Environment]::GetEnvironmentVariable("Path","Machine")
$userPath = [System.Environment]::GetEnvironmentVariable("Path","User")
$env:Path = $machinePath + ";" + $userPath

# Test ffmpeg
try {
    $version = & ffmpeg -version 2>&1 | Select-Object -First 1
    Write-Host "[OK] FFmpeg is working!" -ForegroundColor Green
    Write-Host $version -ForegroundColor White
    Write-Host ""
    Write-Host "SUCCESS! Installation complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "NEXT STEPS:" -ForegroundColor Cyan
    Write-Host "1. Close ALL PowerShell/Terminal windows" -ForegroundColor White
    Write-Host "2. Close your IDE (VS Code/etc)" -ForegroundColor White
    Write-Host "3. Reopen your IDE" -ForegroundColor White
    Write-Host "4. Restart backend server" -ForegroundColor White
    Write-Host "5. Test MP3 download - it will work now!" -ForegroundColor White
}
catch {
    Write-Host "WARNING: FFmpeg added to PATH but not available yet" -ForegroundColor Yellow
    Write-Host "Please close ALL terminals and IDE, then reopen" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Press Enter to exit"
