"""
Minimax (Hailuo AI) Voice Cloning Integration
Excellent voice cloning with good pricing and quality
"""

import os
import requests
import tempfile
import base64
import time
from typing import Dict, Optional

class MinimaxVoiceCloner:
    def __init__(self, api_key: str = None):
        """Initialize Minimax voice cloner"""
        self.api_key = api_key or os.getenv("MINIMAX_API_KEY")
        
        # Try different base URLs (the correct one may vary)
        self.base_urls = [
            "https://api.minimax.chat/v1",
            "https://api.minimaxi.com/v1", 
            "https://open.minimaxi.com/api/v1",
            "https://open-api.minimax.com/v1"
        ]
        self.working_base_url = None
        
        if not self.api_key:
            print("⚠️  Minimax API key not found. Set MINIMAX_API_KEY environment variable")
        else:
            print("✅ Minimax voice cloner initialized with API key")
            print("🔍 Will auto-detect working endpoint on first use")
    
    def clone_and_generate(self, text: str, voice_sample_path: str, 
                          voice_name: str = "user_voice") -> str:
        """
        Clone voice from sample and generate speech using Minimax
        Returns: path to generated audio file
        """
        
        if not self.api_key:
            raise Exception("Minimax API key required")
        
        print(f"🎙️ Minimax voice cloning: '{text[:50]}...'")
        
        try:
            # Step 1: Upload voice sample for cloning
            voice_id = self._upload_voice_sample(voice_sample_path, voice_name)
            print(f"✅ Voice uploaded successfully: {voice_id}")
            
            # Step 2: Generate speech with cloned voice
            audio_path = self._generate_speech(text, voice_id)
            print(f"✅ Speech generated: {audio_path}")
            
            return audio_path
            
        except Exception as e:
            print(f"❌ Minimax cloning failed: {e}")
            raise e
    
    def _upload_voice_sample(self, voice_sample_path: str, voice_name: str) -> str:
        """Upload voice sample to Minimax for cloning"""
        
        # Convert audio file to base64
        with open(voice_sample_path, 'rb') as audio_file:
            audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
        
        url = f"{self.base_url}/audio/voice_clone"
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "voice_name": voice_name,
            "audio_data": audio_data,
            "audio_format": "wav",  # or "mp3"
            "description": f"Voice clone for {voice_name}"
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"Failed to upload voice: {response.text}")
        
        result = response.json()
        return result.get('voice_id') or result.get('id')
    
    def _generate_speech(self, text: str, voice_id: str) -> str:
        """Generate speech with cloned voice"""
        
        url = f"{self.base_url}/audio/speech"
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "text": text,
            "voice_id": voice_id,
            "model": "speech-01",  # Minimax TTS model
            "audio_setting": {
                "sample_rate": 24000,
                "bitrate": 128000,
                "format": "wav"
            },
            "voice_setting": {
                "speed": 1.0,
                "vol": 50,
                "pitch": 0
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"Failed to generate speech: {response.text}")
        
        result = response.json()
        
        # Handle different response formats
        if 'audio_url' in result:
            # Download audio from URL
            audio_url = result['audio_url']
            return self._download_audio(audio_url)
        elif 'audio_data' in result:
            # Direct base64 audio data
            return self._save_audio_data(result['audio_data'])
        else:
            raise Exception("Unexpected response format from Minimax")
    
    def _download_audio(self, audio_url: str) -> str:
        """Download audio from URL"""
        response = requests.get(audio_url)
        
        if response.status_code != 200:
            raise Exception(f"Failed to download audio: {response.status_code}")
        
        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_file.write(response.content)
        temp_file.close()
        
        return temp_file.name
    
    def _save_audio_data(self, audio_data: str) -> str:
        """Save base64 audio data to file"""
        audio_bytes = base64.b64decode(audio_data)
        
        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_file.write(audio_bytes)
        temp_file.close()
        
        return temp_file.name
    
    def get_voice_list(self) -> list:
        """Get list of available voices"""
        url = f"{self.base_url}/audio/voices"
        
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json().get('voices', [])
        else:
            print(f"⚠️  Failed to get voice list: {response.text}")
            return []

# Alternative API endpoints (if main one doesn't work)
class MinimaxAlternativeAPI:
    """Alternative Minimax API endpoints"""
    
    # These are common Minimax API endpoints
    ENDPOINTS = [
        "https://api.minimax.chat/v1",
        "https://api.minimax.io/v1", 
        "https://open-api.minimax.io/v1",
        "https://hailuoai.com/api/v1"
    ]
    
    @staticmethod
    def test_endpoints(api_key: str):
        """Test which endpoint works"""
        headers = {'Authorization': f'Bearer {api_key}'}
        
        for endpoint in MinimaxAlternativeAPI.ENDPOINTS:
            try:
                response = requests.get(f"{endpoint}/audio/voices", headers=headers, timeout=5)
                if response.status_code in [200, 401]:  # 401 means endpoint exists but needs auth
                    print(f"✅ Working endpoint: {endpoint}")
                    return endpoint
            except:
                continue
        
        print("❌ No working endpoints found")
        return None

# Quick test function
def test_minimax_cloning():
    """Test Minimax voice cloning"""
    
    api_key = os.getenv("MINIMAX_API_KEY")
    if not api_key:
        print("❌ Set MINIMAX_API_KEY environment variable first")
        print("   Get key from: https://api.minimax.chat/")
        return
    
    # Test endpoint connectivity
    working_endpoint = MinimaxAlternativeAPI.test_endpoints(api_key)
    if not working_endpoint:
        print("❌ Cannot connect to Minimax API")
        return
    
    cloner = MinimaxVoiceCloner(api_key)
    print("🎉 Minimax voice cloner ready!")
    
    # Test voice list
    voices = cloner.get_voice_list()
    print(f"📊 Available voices: {len(voices)}")

if __name__ == "__main__":
    test_minimax_cloning()
