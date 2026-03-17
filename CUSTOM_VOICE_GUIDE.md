# Custom Voice Feature - User Guide

## 🎤 The Novelty: Upload Your Voice, Get Your Podcast!

This is the **core innovation** of this project - upload a sample of your voice, and the system will generate podcasts that match your voice characteristics!

## How It Works

### Voice Matching Technology
Since Coqui TTS doesn't support Python 3.12 yet, we've implemented a **voice characteristic matching** system:

1. **Analysis**: System analyzes your uploaded voice for:
   - Pitch (fundamental frequency)
   - Tone/Timbre (spectral characteristics)
   - Energy/Volume levels
   - Speech rate

2. **Matching**: When generating podcast:
   - Selects closest system voice (male/female)
   - Adjusts pitch to match your voice
   - Matches volume/energy levels
   - Post-processes audio to approximate your tone

3. **Result**: Generated podcast sounds closer to your voice!

## How to Use Custom Voice

### Step 1: Prepare Your Voice Sample

**Requirements:**
- **Duration**: Minimum 10 seconds (15-30 seconds recommended)
- **Format**: MP3, WAV, or OGG
- **Quality**: 
  - Clear recording (minimal background noise)
  - Normal speaking pace
  - Conversational tone (as you'd narrate a podcast)
- **Content**: Read a paragraph naturally - the actual words don't matter

**Tips for Best Results:**
- ✅ Record in a quiet room
- ✅ Use a decent microphone (phone is OK)
- ✅ Speak clearly and naturally
- ✅ Maintain consistent volume
- ❌ Avoid background music or noise
- ❌ Don't shout or whisper

### Step 2: Upload Your Voice Sample

1. Upload your PDF document first
2. In the Voice Selection section, choose **"Your Voice"**
3. Upload your voice sample (10+ seconds)
4. System will analyze and show:
   - Duration
   - Pitch characteristics
   - Voice quality assessment

### Step 3: Generate Podcast

1. Make sure "Your Voice" is selected
2. Keep "Multi-Narrator" disabled (unless you want mixed voices)
3. Click "Generate Podcast"
4. System will:
   - Analyze your voice characteristics
   - Generate speech matching your pitch/tone
   - Apply voice adjustments to match your sample

## Technical Details

### What Gets Matched
- ✅ **Pitch/Frequency**: Shifted to match your voice's pitch
- ✅ **Volume/Energy**: Normalized to match your speaking volume
- ✅ **Gender**: Auto-detects male/female and selects appropriate base voice
- ⚠️ **Timbre**: Partially matched (limited by system voices)
- ⚠️ **Accent**: Not matched (uses system voice accent)

### Limitations

**Current Implementation (Voice Matching):**
- Uses Windows TTS voices as base
- Applies pitch/tone adjustments
- Result: Recognizable similarity to your voice
- Quality: Good approximation, not perfect clone

**Future Enhancement (True Voice Cloning):**
When Coqui TTS supports Python 3.12:
- True AI voice cloning
- Near-perfect replication
- All characteristics matched
- Requires ~2GB model download

## Example Workflow

```
1. Record yourself reading for 20 seconds:
   "Hello, I'm recording this sample for my custom podcast voice. 
    This system will analyze my voice characteristics and use them 
    to generate podcasts that sound like me. I'm speaking naturally 
    as I would when narrating content."

2. Save as: my_voice.mp3

3. Upload to application:
   - Select "Your Voice" option
   - Upload my_voice.mp3
   - Wait for analysis (3-5 seconds)

4. Generate Podcast:
   - Upload your PDF
   - Select language
   - Keep "Your Voice" selected
   - Click Generate
   - Wait for custom voice podcast!

5. Result:
   ✅ Podcast generated with pitch matching your voice
   ✅ Volume/energy matched
   ✅ Recognizable as your voice style
```

## Troubleshooting

### Voice Sample Rejected
**Error: "Voice sample too short"**
- Solution: Record at least 10 seconds (15-30 recommended)

**Error: "Invalid audio format"**
- Solution: Use MP3, WAV, or OGG format only

### Generated Voice Doesn't Sound Like Me
**Issue: Very different pitch**
- Solution: Speak normally (not too high/low) in sample
- Check: System might have selected wrong gender base voice

**Issue: Different accent**
- Limitation: Uses system voice accent (can't be changed with current method)

**Issue: Robotic sound**
- Expected: System voices have some robotic quality
- Future: Will improve with Coqui TTS when Python 3.12 supported

### Upload Failed
**Error: "Voice profile not found"**
- Solution: Make sure to upload voice AFTER uploading PDF
- Check: Refresh page and try again

## API Reference

### Upload Voice Endpoint
```http
POST /api/upload-voice
Content-Type: multipart/form-data

Parameters:
- file: Audio file (MP3/WAV/OGG)
- job_id: PDF job ID from upload

Response:
{
  "message": "Voice uploaded successfully",
  "job_id": "abc-123",
  "voice_profile": {
    "analysis": {
      "duration": 20.5,
      "pitch_mean": 145.2,
      "pitch_std": 12.3,
      "energy": 0.05,
      "quality": "good"
    }
  }
}
```

### Generate with Custom Voice
```http
POST /api/generate-podcast
Content-Type: application/json

{
  "job_id": "abc-123",
  "language": "en",
  "voice_type": "custom",
  "enable_multi_narrator": false
}
```

## Voice Quality Comparison

| Voice Option | Quality | Speed | Customization |
|--------------|---------|-------|---------------|
| Professional Male | Good | Fast | None |
| Professional Female | Good | Fast | None |
| AI Neutral | Good | Fast | None |
| AI Energetic | Good | Fast | None |
| **Your Voice** | **Better** | **Medium** | **High** |

## Future Enhancements

### Planned (When Coqui TTS supports Python 3.12):
- ✨ True AI voice cloning
- ✨ Perfect voice replication
- ✨ Accent preservation
- ✨ Emotion matching
- ✨ Multi-lingual with your voice

### Alternative (Available Now):
- Cloud API integration:
  - ElevenLabs Voice Cloning (premium)
  - Resemble.AI (professional)
  - Play.ht (affordable)

## Summary

✅ **Custom voice feature is NOW WORKING!**
🎤 Upload your voice sample (10+ seconds)
📊 System matches pitch, tone, and energy
🎧 Get podcasts that sound like you!
⚡ Fast processing with voice matching
🔮 Will improve when Coqui TTS supports Python 3.12

**This is the unique selling point of your project - voice personalization!**
