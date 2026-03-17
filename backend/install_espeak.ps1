# Install eSpeak for Enhanced Indian TTS
# PowerShell script to install eSpeak on Windows for better Indian voice quality

Write-Host "🇮🇳 Installing eSpeak for Enhanced Indian TTS..." -ForegroundColor Green
Write-Host "This will provide better quality Indian accent generation" -ForegroundColor Yellow

# Check if Chocolatey is installed
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "📦 Chocolatey not found. Installing Chocolatey first..." -ForegroundColor Yellow
    
    # Install Chocolatey
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    
    # Refresh environment variables
    $env:ChocolateyInstall = Convert-Path "$((Get-Command choco).Path)\..\.."   
    Import-Module "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
    refreshenv
}

try {
    Write-Host "📥 Installing eSpeak via Chocolatey..." -ForegroundColor Yellow
    choco install espeak -y
    
    Write-Host "✅ eSpeak installed successfully!" -ForegroundColor Green
    Write-Host "🔄 Please restart your terminal/PowerShell for changes to take effect" -ForegroundColor Yellow
    
    # Test installation
    Write-Host "🧪 Testing eSpeak installation..." -ForegroundColor Yellow
    espeak --version
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "🎉 eSpeak is working correctly!" -ForegroundColor Green
        Write-Host "🇮🇳 Your Indian TTS quality will now be significantly improved!" -ForegroundColor Green
    } else {
        Write-Host "⚠️  eSpeak installed but may need system restart" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "❌ Failed to install eSpeak via Chocolatey" -ForegroundColor Red
    Write-Host "💡 Alternative: Download manually from https://espeak.sourceforge.net/" -ForegroundColor Yellow
    Write-Host "   1. Download eSpeak setup.exe" -ForegroundColor White
    Write-Host "   2. Run as administrator" -ForegroundColor White
    Write-Host "   3. Add C:\Program Files\eSpeak\command_line to PATH" -ForegroundColor White
}

Write-Host "`n🚀 After installation, restart backend server to use enhanced Indian voices!" -ForegroundColor Cyan
