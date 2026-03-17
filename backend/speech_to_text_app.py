"""
Complete Flask App for Speech-to-Text with Custom Voice Generation
Using ElevenLabs API for custom voice creation and synthesis
"""

import os
import tempfile
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our custom voice API
from elevenlabs_custom_voice_api import ElevenLabsCustomVoice, create_flask_routes

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize ElevenLabs API
try:
    elevenlabs_api = ElevenLabsCustomVoice()
    print("✅ ElevenLabs API initialized successfully")
except Exception as e:
    print(f"❌ ElevenLabs API initialization failed: {e}")
    print("💡 Make sure to set ELEVENLABS_API_KEY environment variable")
    elevenlabs_api = None

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "elevenlabs_available": elevenlabs_api is not None,
        "message": "Speech-to-Text with Custom Voice API is running"
    }

# Speech-to-Text endpoint (you can integrate your existing STT logic here)
@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    """Convert speech to text (integrate your existing STT logic)"""
    try:
        if 'audio' not in request.files:
            return {"error": "No audio file provided"}, 400
        
        audio_file = request.files['audio']
        
        # Save audio temporarily
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        audio_file.save(temp_file.name)
        temp_file.close()
        
        # TODO: Integrate your speech-to-text logic here
        # For now, returning dummy text
        transcribed_text = "This is where your speech-to-text conversion result would appear."
        
        # Cleanup
        os.unlink(temp_file.name)
        
        return {
            "success": True,
            "text": transcribed_text,
            "message": "Speech converted to text successfully"
        }
        
    except Exception as e:
        return {"error": str(e)}, 500

# Custom Voice Endpoints (created by our ElevenLabs integration)
if elevenlabs_api:
    create_flask_routes(app, elevenlabs_api)
else:
    # Fallback endpoints when ElevenLabs is not available
    @app.route('/api/voice/create', methods=['POST'])
    def create_custom_voice_fallback():
        return {"error": "ElevenLabs API not configured. Please set ELEVENLABS_API_KEY"}, 503
    
    @app.route('/api/voice/generate', methods=['POST'])
    def generate_speech_fallback():
        return {"error": "ElevenLabs API not configured. Please set ELEVENLABS_API_KEY"}, 503
    
    @app.route('/api/voice/list', methods=['GET'])
    def list_voices_fallback():
        return {"error": "ElevenLabs API not configured. Please set ELEVENLABS_API_KEY"}, 503

# Complete workflow endpoint: STT + Custom Voice TTS
@app.route('/api/complete-workflow', methods=['POST'])
def complete_workflow():
    """
    Complete workflow: Speech-to-Text + Custom Voice Text-to-Speech
    Upload audio -> Convert to text -> Generate with custom voice
    """
    try:
        if not elevenlabs_api:
            return {"error": "ElevenLabs API not configured"}, 503
        
        # Get parameters
        audio_file = request.files.get('audio')
        voice_id = request.form.get('voice_id')
        
        if not audio_file or not voice_id:
            return {"error": "Audio file and voice_id required"}, 400
        
        # Step 1: Speech-to-Text
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        audio_file.save(temp_audio.name)
        temp_audio.close()
        
        # TODO: Replace with your actual STT logic
        transcribed_text = "This is the transcribed text from your speech-to-text system."
        
        # Step 2: Generate speech with custom voice
        output_audio = elevenlabs_api.generate_speech(transcribed_text, voice_id)
        
        # Cleanup
        os.unlink(temp_audio.name)
        
        # Return both text and audio
        return {
            "success": True,
            "transcribed_text": transcribed_text,
            "audio_file": output_audio,
            "message": "Complete workflow executed successfully"
        }
        
    except Exception as e:
        return {"error": str(e)}, 500

# API documentation endpoint
@app.route('/api/docs', methods=['GET'])
def api_documentation():
    """API documentation"""
    docs = {
        "title": "Speech-to-Text with Custom Voice API",
        "version": "1.0.0",
        "description": "Complete API for speech-to-text conversion with custom voice generation using ElevenLabs",
        "endpoints": {
            "health": {
                "method": "GET",
                "url": "/api/health",
                "description": "Health check and API status"
            },
            "speech_to_text": {
                "method": "POST",
                "url": "/api/speech-to-text",
                "description": "Convert speech audio to text",
                "parameters": {
                    "audio": "Audio file (WAV, MP3, etc.)"
                }
            },
            "create_voice": {
                "method": "POST",
                "url": "/api/voice/create",
                "description": "Create custom voice from audio samples",
                "parameters": {
                    "files": "List of audio files for voice training",
                    "voice_name": "Name for the custom voice"
                }
            },
            "generate_speech": {
                "method": "POST",
                "url": "/api/voice/generate",
                "description": "Generate speech with custom voice",
                "parameters": {
                    "text": "Text to convert to speech",
                    "voice_id": "ID of the custom voice to use"
                }
            },
            "list_voices": {
                "method": "GET",
                "url": "/api/voice/list",
                "description": "Get list of all available voices"
            },
            "complete_workflow": {
                "method": "POST",
                "url": "/api/complete-workflow",
                "description": "Complete STT + Custom Voice TTS workflow",
                "parameters": {
                    "audio": "Input audio for STT",
                    "voice_id": "Custom voice ID for TTS output"
                }
            }
        },
        "setup": {
            "environment_variables": {
                "ELEVENLABS_API_KEY": "Your ElevenLabs API key from https://elevenlabs.io/"
            },
            "installation": [
                "pip install flask flask-cors requests python-dotenv",
                "Set ELEVENLABS_API_KEY in .env file",
                "Run: python speech_to_text_app.py"
            ]
        }
    }
    return docs

if __name__ == '__main__':
    # Check if ElevenLabs API key is set
    if not os.getenv('ELEVENLABS_API_KEY'):
        print("⚠️  WARNING: ELEVENLABS_API_KEY not set!")
        print("   1. Get API key from: https://elevenlabs.io/")
        print("   2. Set in .env file: ELEVENLABS_API_KEY=your_key_here")
        print("   3. Restart the application")
        print()
    
    print("🚀 Starting Speech-to-Text with Custom Voice API")
    print("=" * 60)
    print("📡 API Server: http://localhost:5000")
    print("💚 Health Check: http://localhost:5000/api/health")
    print("📖 Documentation: http://localhost:5000/api/docs")
    print("=" * 60)
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
