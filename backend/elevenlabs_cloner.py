"""
ElevenLabs Voice Cloning Integration
Perfect solution for 10-20 second voice samples
"""

import os
import requests
import tempfile
from typing import Dict, Optional

class ElevenLabsVoiceCloner:
    def __init__(self, api_key: str = None):
        """Initialize ElevenLabs voice cloner"""
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        self.base_url = "https://api.elevenlabs.io/v1"
        
        if not self.api_key:
            print("⚠️  ElevenLabs API key not found. Set ELEVENLABS_API_KEY environment variable")
        else:
            print("✅ ElevenLabs voice cloner initialized")
    
    def clone_and_generate(self, text: str, voice_sample_path: str, 
                          voice_name: str = "user_voice") -> str:
        """
        Clone voice from sample and generate speech
        Returns: path to generated audio file
        """
        
        if not self.api_key:
            raise Exception("ElevenLabs API key required")
        
        print(f"🎙️ Cloning voice and generating: '{text[:50]}...'")
        
        try:
            # Step 1: Add voice for cloning
            voice_id = self._add_voice(voice_sample_path, voice_name)
            print(f"✅ Voice cloned successfully: {voice_id}")
            
            # Step 2: Generate speech with cloned voice
            audio_path = self._generate_speech(text, voice_id)
            print(f"✅ Speech generated: {audio_path}")
            
            # Step 3: Clean up voice (optional - keeps API tidy)
            # self._delete_voice(voice_id)
            
            return audio_path
            
        except Exception as e:
            print(f"❌ ElevenLabs cloning failed: {e}")
            raise e
    
    def _add_voice(self, voice_sample_path: str, voice_name: str) -> str:
        """Add voice for cloning"""
        
        url = f"{self.base_url}/voices/add"
        
        headers = {
            'xi-api-key': self.api_key
        }
        
        with open(voice_sample_path, 'rb') as audio_file:
            files = {
                'files': (os.path.basename(voice_sample_path), audio_file, 'audio/wav')
            }
            data = {
                'name': voice_name,
                'description': f'Voice cloned from user sample - {voice_name}',
                'labels': '{"accent": "user", "gender": "auto", "age": "adult"}'
            }
            
            response = requests.post(url, files=files, data=data, headers=headers)
            
            if response.status_code != 200:
                raise Exception(f"Failed to add voice: {response.text}")
            
            return response.json()['voice_id']
    
    def _generate_speech(self, text: str, voice_id: str) -> str:
        """Generate speech with cloned voice"""
        
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        
        headers = {
            'xi-api-key': self.api_key,
            'Content-Type': 'application/json'
        }
        
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",  # Best model
            "voice_settings": {
                "stability": 0.75,      # How consistent the voice is
                "similarity_boost": 0.85,  # How similar to original
                "style": 0.5,          # Style exaggeration 
                "use_speaker_boost": True  # Enhance speaker similarity
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"Failed to generate speech: {response.text}")
        
        # Save generated audio
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_file.write(response.content)
        temp_file.close()
        
        return temp_file.name
    
    def _delete_voice(self, voice_id: str):
        """Delete cloned voice (cleanup)"""
        url = f"{self.base_url}/voices/{voice_id}"
        
        headers = {
            'xi-api-key': self.api_key
        }
        
        requests.delete(url, headers=headers)
        print(f"🗑️ Deleted voice: {voice_id}")

# Quick test function
def test_elevenlabs_cloning():
    """Test ElevenLabs voice cloning"""
    
    # You need to set ELEVENLABS_API_KEY environment variable
    cloner = ElevenLabsVoiceCloner()
    
    if not cloner.api_key:
        print("❌ Set ELEVENLABS_API_KEY environment variable first")
        print("   Get free key from: https://elevenlabs.io/")
        return
    
    # Test with sample
    test_text = "Hello, this is a test of the ElevenLabs voice cloning system. It should sound exactly like my voice!"
    
    # You would provide the path to uploaded voice sample
    voice_sample_path = "path/to/user/voice/sample.wav"
    
    try:
        result_path = cloner.clone_and_generate(test_text, voice_sample_path)
        print(f"🎉 Success! Generated audio: {result_path}")
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_elevenlabs_cloning()
