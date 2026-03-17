"""
ElevenLabs Custom Voice API Integration
For Speech-to-Text project with custom voice generation
"""

import os
import requests
import tempfile
import base64
import time
from typing import Dict, Optional, List
import json

class ElevenLabsCustomVoice:
    def __init__(self, api_key: str = None):
        """Initialize ElevenLabs API for custom voice generation"""
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        self.base_url = "https://api.elevenlabs.io/v1"
        
        if not self.api_key:
            raise Exception("ElevenLabs API key required. Get from: https://elevenlabs.io/")
        
        print("✅ ElevenLabs Custom Voice API initialized")
    
    def create_custom_voice(self, voice_files: List[str], voice_name: str = "CustomVoice") -> str:
        """
        Create a custom voice from audio files
        Args:
            voice_files: List of paths to audio files (WAV, MP3)
            voice_name: Name for the custom voice
        Returns:
            voice_id: ID of the created custom voice
        """
        
        print(f"🎙️ Creating custom voice: {voice_name}")
        url = f"{self.base_url}/voices/add"
        
        headers = {
            'xi-api-key': self.api_key
        }
        
        # Prepare files for upload
        files = []
        for i, file_path in enumerate(voice_files):
            with open(file_path, 'rb') as f:
                files.append(('files', (f'sample_{i}.wav', f.read(), 'audio/wav')))
        
        data = {
            'name': voice_name,
            'description': f'Custom voice: {voice_name}',
            'labels': json.dumps({
                "accent": "custom",
                "description": "User uploaded custom voice",
                "age": "adult",
                "gender": "auto"
            })
        }
        
        response = requests.post(url, files=files, data=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            voice_id = result['voice_id']
            print(f"✅ Custom voice created: {voice_id}")
            return voice_id
        else:
            raise Exception(f"Failed to create voice: {response.text}")
    
    def generate_speech(self, text: str, voice_id: str, output_path: str = None) -> str:
        """
        Generate speech with custom voice
        Args:
            text: Text to convert to speech
            voice_id: ID of the custom voice
            output_path: Where to save the audio (optional)
        Returns:
            Path to generated audio file
        """
        
        print(f"🔊 Generating speech with custom voice...")
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        
        headers = {
            'xi-api-key': self.api_key,
            'Content-Type': 'application/json'
        }
        
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",  # Best model for custom voices
            "voice_settings": {
                "stability": 0.75,
                "similarity_boost": 0.85,
                "style": 0.5,
                "use_speaker_boost": True
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            # Save audio file
            if output_path is None:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                output_path = temp_file.name
                temp_file.close()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Speech generated: {output_path}")
            return output_path
        else:
            raise Exception(f"Failed to generate speech: {response.text}")
    
    def list_voices(self) -> List[Dict]:
        """Get list of all available voices (including custom ones)"""
        url = f"{self.base_url}/voices"
        
        headers = {
            'xi-api-key': self.api_key
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()['voices']
        else:
            raise Exception(f"Failed to get voices: {response.text}")
    
    def delete_voice(self, voice_id: str):
        """Delete a custom voice"""
        url = f"{self.base_url}/voices/{voice_id}"
        
        headers = {
            'xi-api-key': self.api_key
        }
        
        response = requests.delete(url, headers=headers)
        
        if response.status_code == 200:
            print(f"✅ Voice deleted: {voice_id}")
        else:
            print(f"⚠️  Failed to delete voice: {response.text}")
    
    def get_voice_info(self, voice_id: str) -> Dict:
        """Get information about a specific voice"""
        url = f"{self.base_url}/voices/{voice_id}"
        
        headers = {
            'xi-api-key': self.api_key
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get voice info: {response.text}")

# Flask API Integration
def create_flask_routes(app, elevenlabs_api):
    """Create Flask routes for ElevenLabs integration"""
    
    @app.route('/api/voice/create', methods=['POST'])
    def create_custom_voice():
        """Create custom voice from uploaded audio files"""
        try:
            if 'files' not in request.files:
                return {"error": "No audio files provided"}, 400
            
            files = request.files.getlist('files')
            voice_name = request.form.get('voice_name', 'CustomVoice')
            
            # Save uploaded files temporarily
            temp_files = []
            for file in files:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                file.save(temp_file.name)
                temp_files.append(temp_file.name)
            
            # Create custom voice
            voice_id = elevenlabs_api.create_custom_voice(temp_files, voice_name)
            
            # Cleanup temp files
            for temp_file in temp_files:
                os.unlink(temp_file)
            
            return {
                "success": True,
                "voice_id": voice_id,
                "voice_name": voice_name
            }
            
        except Exception as e:
            return {"error": str(e)}, 500
    
    @app.route('/api/voice/generate', methods=['POST'])
    def generate_speech():
        """Generate speech with custom voice"""
        try:
            data = request.get_json()
            text = data.get('text')
            voice_id = data.get('voice_id')
            
            if not text or not voice_id:
                return {"error": "Text and voice_id required"}, 400
            
            # Generate speech
            audio_path = elevenlabs_api.generate_speech(text, voice_id)
            
            # Return audio file
            return send_file(audio_path, as_attachment=True, download_name="generated_speech.wav")
            
        except Exception as e:
            return {"error": str(e)}, 500
    
    @app.route('/api/voice/list', methods=['GET'])
    def list_voices():
        """Get list of all voices"""
        try:
            voices = elevenlabs_api.list_voices()
            return {"voices": voices}
        except Exception as e:
            return {"error": str(e)}, 500
    
    @app.route('/api/voice/delete/<voice_id>', methods=['DELETE'])
    def delete_voice(voice_id):
        """Delete a custom voice"""
        try:
            elevenlabs_api.delete_voice(voice_id)
            return {"success": True}
        except Exception as e:
            return {"error": str(e)}, 500

# Example usage
if __name__ == "__main__":
    # Initialize API (you need to set ELEVENLABS_API_KEY environment variable)
    api = ElevenLabsCustomVoice()
    
    print("🧪 ElevenLabs Custom Voice API Test")
    print("=" * 50)
    
    # Example: List available voices
    try:
        voices = api.list_voices()
        print(f"📊 Available voices: {len(voices)}")
        for voice in voices[:3]:  # Show first 3
            print(f"   - {voice['name']} ({voice['voice_id']})")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure to set ELEVENLABS_API_KEY environment variable")
        print("   Get API key from: https://elevenlabs.io/")
