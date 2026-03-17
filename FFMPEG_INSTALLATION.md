# FFmpeg Installation Guide

## What is FFmpeg?

FFmpeg is a free, open-source tool for audio/video processing. It's needed for **MP3 conversion** in this project.

## Current Status

✅ **WAV Download**: Works without ffmpeg
⚠️ **MP3 Download**: Requires ffmpeg installation

## Installation Options

### Option 1: Chocolatey (Easiest for Windows)

If you have Chocolatey package manager:

```powershell
# Run as Administrator
choco install ffmpeg
```

### Option 2: Manual Installation (Windows)

1. **Download ffmpeg**
   - Go to: https://www.gyan.dev/ffmpeg/builds/
   - Download: `ffmpeg-release-essentials.zip`

2. **Extract**
   - Extract to: `C:\ffmpeg`
   - You should have: `C:\ffmpeg\bin\ffmpeg.exe`

3. **Add to PATH**
   ```powershell
   # Run as Administrator in PowerShell
   $env:Path += ";C:\ffmpeg\bin"
   
   # Make it permanent
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\ffmpeg\bin", [EnvironmentVariableTarget]::Machine)
   ```

4. **Verify Installation**
   ```powershell
   ffmpeg -version
   ```

5. **Restart your terminal/IDE**

### Option 3: Scoop (Windows Package Manager)

```powershell
scoop install ffmpeg
```

### Option 4: Direct Download

1. Download from: https://ffmpeg.org/download.html
2. Choose "Windows builds from gyan.dev"
3. Download the essentials build
4. Follow extraction and PATH steps above

## Verify Installation

After installation, verify ffmpeg is available:

```powershell
# Should show version info
ffmpeg -version

# Should show path to ffmpeg.exe
where ffmpeg
```

## Restart Backend

After installing ffmpeg:

```bash
# Stop the backend (Ctrl+C)
# Restart it
cd backend
python app.py
```

## Testing MP3 Conversion

1. Generate a podcast
2. Click "Download MP3"
3. Check backend logs:
   - ✅ Success: "MP3 conversion successful for job {id}"
   - ❌ Failed: "MP3 conversion failed - ffmpeg not found"

## Without FFmpeg

If you don't want to install ffmpeg:
- ✅ **WAV download still works perfectly**
- ⚠️ MP3 button will download WAV instead
- 💡 WAV files are higher quality but larger
- 📊 Size comparison: MP3 (~5MB), WAV (~50MB) for 10min podcast

## Troubleshooting

### "ffmpeg not found" after installation

**Solution**: 
1. Close ALL terminals/command prompts
2. Close your IDE (VS Code/etc)
3. Reopen and try again
4. Verify PATH: `echo $env:Path` (should include ffmpeg path)

### "Access denied" during PATH modification

**Solution**:
- Run PowerShell as Administrator
- Or manually add to PATH via:
  - Control Panel → System → Advanced → Environment Variables

### MP3 still not working after install

**Solution**:
1. Restart backend server
2. Check logs: `backend/logs/app.log`
3. Try WAV download first to verify basic download works

## File Size Reference

Example 10-minute podcast:
- **WAV**: ~50 MB (high quality, lossless)
- **MP3 (192 kbps)**: ~14 MB (good quality, compressed)
- **MP3 (128 kbps)**: ~9 MB (acceptable quality, more compressed)

## Alternative: Cloud Conversion

If ffmpeg installation is difficult, consider:
1. Download WAV
2. Convert online:
   - https://cloudconvert.com/wav-to-mp3
   - https://online-audio-converter.com/
3. Or use local tools: VLC, Audacity, etc.

## Summary

- 📦 **Optional but Recommended**: FFmpeg enables MP3 downloads
- ✅ **WAV Works Now**: Always available, higher quality
- ⚡ **Quick Install**: Chocolatey or Scoop (5 minutes)
- 🔄 **Restart Required**: Backend must restart after installation

Install FFmpeg to unlock MP3 downloads! 🎵
