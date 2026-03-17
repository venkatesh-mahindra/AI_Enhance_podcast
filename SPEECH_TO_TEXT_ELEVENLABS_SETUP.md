# 🎙️ Speech-to-Text + Custom Voice with ElevenLabs API

## 🚀 **Complete Integration for Your Project**

### ✅ **What You Get:**
- **Speech-to-Text** → Convert audio to text (integrate your existing logic)
- **Custom Voice Creation** → Create voices from user audio samples
- **Text-to-Speech** → Generate speech with custom voices
- **Complete Workflow** → STT + Custom Voice TTS in one API call
- **React Components** → Ready-to-use frontend components
- **Flask Backend** → Complete API server

---

## 🔑 **Quick Setup (5 minutes)**

### **1. Get ElevenLabs API Key**
1. Go to: **https://elevenlabs.io/**
2. Sign up (free tier: 10,000 characters/month)
3. Go to: **Profile → API Key**
4. Copy your API key (starts with "sk-...")

### **2. Environment Setup**
```bash
# Create .env file
echo "ELEVENLABS_API_KEY=sk-your-api-key-here" > .env

# Install dependencies
pip install flask flask-cors requests python-dotenv
```

### **3. Start Backend**
```bash
python speech_to_text_app.py
```

### **4. Test API**
Visit: http://localhost:5000/api/health

---

## 🎯 **API Endpoints**

### **Health Check**
```
GET /api/health
```

### **Speech-to-Text** (integrate your logic)
```
POST /api/speech-to-text
Body: FormData with 'audio' file
```

### **Create Custom Voice**
```
POST /api/voice/create
Body: FormData with:
  - files: Audio samples (2-3 files recommended)
  - voice_name: Name for the voice
```

### **Generate Speech with Custom Voice**
```
POST /api/voice/generate
Body: JSON
{
  "text": "Text to convert",
  "voice_id": "voice_id_from_create"
}
```

### **List All Voices**
```
GET /api/voice/list
```

### **Complete Workflow** (STT + Custom TTS)
```
POST /api/complete-workflow
Body: FormData with:
  - audio: Input audio for STT
  - voice_id: Custom voice for output
```

---

## ⚛️ **React Integration**

### **1. Copy Components**
Copy these files to your React project:
- `react_custom_voice_components.js` → Main components
- `custom_voice_styles.css` → Styling

### **2. Import in Your App**
```jsx
import CustomVoiceApp from './components/CustomVoiceApp';
import './styles/custom_voice_styles.css';

function App() {
  return (
    <div className="App">
      <CustomVoiceApp />
    </div>
  );
}
```

### **3. Individual Components**
```jsx
import { 
  CustomVoiceCreator,
  CustomTextToSpeech,
  VoiceManager 
} from './components/CustomVoiceApp';

// Use individual components as needed
<CustomVoiceCreator />
<CustomTextToSpeech />
<VoiceManager />
```

---

## 🔧 **Integration with Your STT System**

### **Update Speech-to-Text Logic**
In `speech_to_text_app.py`, replace the dummy STT code:

```python
@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    try:
        audio_file = request.files['audio']
        
        # Save audio temporarily
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        audio_file.save(temp_file.name)
        temp_file.close()
        
        # 🔧 REPLACE THIS with your STT logic
        # transcribed_text = your_stt_function(temp_file.name)
        transcribed_text = "Replace with your STT result"
        
        # Cleanup
        os.unlink(temp_file.name)
        
        return {
            "success": True,
            "text": transcribed_text
        }
        
    except Exception as e:
        return {"error": str(e)}, 500
```

---

## 🎵 **Usage Examples**

### **1. Create Custom Voice**
```javascript
// Frontend JavaScript
const createVoice = async (audioFiles, voiceName) => {
  const formData = new FormData();
  formData.append('voice_name', voiceName);
  
  audioFiles.forEach(file => {
    formData.append('files', file);
  });
  
  const response = await fetch('/api/voice/create', {
    method: 'POST',
    body: formData
  });
  
  const result = await response.json();
  console.log('Voice created:', result.voice_id);
};
```

### **2. Generate Speech**
```javascript
const generateSpeech = async (text, voiceId) => {
  const response = await fetch('/api/voice/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text: text,
      voice_id: voiceId
    })
  });
  
  const audioBlob = await response.blob();
  const audioUrl = URL.createObjectURL(audioBlob);
  
  // Play or download audio
  const audio = new Audio(audioUrl);
  audio.play();
};
```

### **3. Complete Workflow**
```javascript
const completeWorkflow = async (audioFile, customVoiceId) => {
  const formData = new FormData();
  formData.append('audio', audioFile);
  formData.append('voice_id', customVoiceId);
  
  const response = await fetch('/api/complete-workflow', {
    method: 'POST',
    body: formData
  });
  
  const result = await response.json();
  console.log('Transcribed text:', result.transcribed_text);
  console.log('Generated audio:', result.audio_file);
};
```

---

## 🎯 **Project Structure**

```
your-speech-to-text-project/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── CustomVoiceApp.js      # React components
│   │   ├── styles/
│   │   │   └── custom_voice_styles.css # Styling
│   │   └── App.js                      # Main app
│   └── package.json
├── backend/
│   ├── speech_to_text_app.py          # Main Flask app
│   ├── elevenlabs_custom_voice_api.py # ElevenLabs integration
│   ├── .env                           # Environment variables
│   └── requirements.txt               # Python dependencies
└── README.md
```

---

## 📊 **Features Overview**

| Feature | Status | Description |
|---------|--------|-------------|
| **Custom Voice Creation** | ✅ Ready | Create voices from 2-3 audio samples |
| **Speech Generation** | ✅ Ready | Generate speech with custom voices |
| **Voice Management** | ✅ Ready | List, view, delete custom voices |
| **React Components** | ✅ Ready | Complete UI for voice operations |
| **Flask API** | ✅ Ready | RESTful API with all endpoints |
| **STT Integration** | 🔧 Your Code | Integrate your existing STT logic |

---

## 🎉 **Expected Workflow**

1. **User uploads audio samples** → Custom voice created
2. **User speaks into microphone** → Speech-to-text conversion
3. **System generates response** → Uses custom voice for TTS
4. **Result**: User hears response in their own voice! 🎯

---

## 💰 **ElevenLabs Pricing**

- **Free Tier**: 10,000 characters/month
- **Starter**: $5/month - 30,000 characters
- **Creator**: $22/month - 100,000 characters
- **Pro**: $99/month - 500,000 characters

**Perfect for development and small-scale projects!**

---

## 🚀 **Ready to Go!**

Your Speech-to-Text project with custom voice generation is now ready:

✅ **ElevenLabs API integration** → Professional voice cloning
✅ **React components** → Beautiful user interface  
✅ **Flask backend** → Complete API server
✅ **Custom voice workflow** → Create and use custom voices
✅ **Easy integration** → Drop into your existing project

**Just add your STT logic and you're ready for production!** 🎙️✨
