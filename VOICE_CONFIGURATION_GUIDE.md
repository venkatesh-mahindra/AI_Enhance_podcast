# Voice Configuration Guide

## Issue Summary
The application was only generating male voice output regardless of the selected voice style (Professional Female, AI Neutral, AI Energetic, etc.).

## Root Causes Identified

### 1. Multi-Narrator Mode Enabled by Default
- **Problem**: Multi-narrator mode was enabled by default in the frontend (`App.js`)
- **Impact**: When enabled, it overrides user voice selection with hardcoded voice assignments
- **Fix**: Changed default to `false` so user's voice selection takes effect

### 2. AI Voice Types Not Mapped
- **Problem**: `ai_neutral` and `ai_energetic` were not explicitly mapped to system voices
- **Impact**: These voice types defaulted to male voice
- **Fix**: Added proper voice mapping in `voice_cloner.py`

## Current Voice System Configuration

### Available System Voices (Windows TTS)
Your system has 2 built-in voices:
1. **Microsoft David** - Male voice (default)
2. **Microsoft Zira** - Female voice

### Voice Type Mappings
The application now maps voice types as follows:

| Voice Type | System Voice Used | Modifications Applied |
|-----------|------------------|----------------------|
| **Professional Male** | David (Male) | Lower pitch (-1.5 semitones) |
| **Professional Female** | Zira (Female) | Higher pitch (+3 semitones), faster (1.05x) |
| **AI Neutral** | Zira (Female) | Neutral speed, no pitch change |
| **AI Energetic** | Zira (Female) | Higher pitch (+2 semitones), faster (1.12x) |
| **Custom Voice** | Auto-detected | **Matches YOUR uploaded voice!** 🎤 |

## How It Works Now

### Single Narrator Mode (Default)
- User selects a voice style
- That voice is used for the entire podcast
- Post-processing applies pitch and speed modifications to differentiate voices

### Multi-Narrator Mode (Optional)
- User can enable via checkbox after character analysis
- System detects characters in the document
- Automatically assigns different voices based on character gender:
  - Male characters → David voice
  - Female characters → Zira voice
  - Narrator → AI Neutral (Zira with neutral tone)

### Custom Voice Mode (THE NOVELTY! 🎤)
- **Upload your own voice sample** (10+ seconds)
- System analyzes: pitch, tone, energy, speaking rate
- Generates podcast matching YOUR voice characteristics
- **This is the unique feature of this project!**
- See `CUSTOM_VOICE_GUIDE.md` for detailed instructions

## Testing the Voices

A test script has been created to verify voice synthesis:

```bash
cd backend
python test_voice_synthesis.py
```

This generates test audio files in `backend/test_output/` for each voice type.

## Limitations & Notes

### Current Limitations
1. **System Voices Only**: Using Windows built-in TTS (pyttsx3)
   - Limited to 2 voices (David and Zira)
   - Voice quality is basic compared to AI-generated voices

2. **No FFmpeg**: 
   - Warning appears: "Couldn't find ffmpeg or avconv"
   - MP3 conversion won't work (only WAV output)
   - Audio concatenation and post-processing still work

3. **Voice Differentiation**: 
   - Uses pitch shifting and time stretching to create variety
   - Results are noticeable but not as natural as true AI voices

### Upgrading to Better Voices (Optional)

For production-quality voices, you can install:

#### Option 1: Install FFmpeg (for MP3 support)
Download from: https://ffmpeg.org/download.html
- Adds MP3 export capability
- Improves audio processing

#### Option 2: Install Coqui TTS (for AI voices)
```bash
pip install TTS phonemizer torch
```
- Provides 100+ AI voices
- Natural-sounding multi-lingual support
- Requires ~2GB download for models
- Slower processing (GPU recommended)

#### Option 3: Use Cloud TTS APIs
- Google Cloud Text-to-Speech
- Amazon Polly
- Azure Cognitive Services
- ElevenLabs (premium quality)

## Configuration Files Modified

### Frontend Changes
- `frontend/src/App.js`: Changed `enableMultiNarrator` default to `false`
- `frontend/src/utils/api.js`: Fixed API URL to use relative path

### Backend Changes
- `backend/voice_cloner.py`: Improved voice selection and mapping logic
- `backend/.env`: Created with local storage configuration

## Troubleshooting

### Voice Not Changing
1. Make sure multi-narrator mode is **disabled** (unchecked)
2. Select your desired voice from the dropdown
3. Click "Generate Podcast"

### Only Hearing Male Voice
- This was the bug - now fixed!
- Clear browser cache and refresh
- Verify multi-narrator is disabled

### Poor Voice Quality
- Expected with system voices
- Consider upgrading to Coqui TTS or cloud APIs
- Install FFmpeg for better audio processing

## How to Use

1. **Upload PDF**
2. **Select Voice Style** from dropdown:
   - Professional Female (Clear, engaging)
   - AI Neutral (Modern, neutral tone)
   - AI Energetic (Upbeat, enthusiastic)
   - Professional Male (Deep, authoritative)
3. **Keep Multi-Narrator Disabled** (unless you want character voices)
4. **Generate Podcast**
5. **Listen to result** with your selected voice!

## Summary

✅ **Fixed**: Voice selection now works correctly
✅ **Default**: Single narrator mode with user's voice choice
✅ **Optional**: Multi-narrator for story content with dialogues
✅ **Tested**: All voice types generate successfully
⚠️ **Limitation**: Using basic Windows TTS (can be upgraded)
