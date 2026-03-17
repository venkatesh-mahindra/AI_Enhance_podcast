"""
Coqui TTS - Completely FREE Voice Cloning
No API key needed, runs locally, unlimited usage
"""

import os
import tempfile
from typing import Dict, Optional

class CoquiFreeVoiceCloner:
    def __init__(self):
        """Initialize Coqui TTS voice cloner (completely free)"""
        try:
            from TTS.api import TTS
            
            # Initialize TTS model for voice cloning
            # Using XTTS-v2 model which supports voice cloning
            self.tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")
            print("✅ Coqui TTS initialized (FREE voice cloning)")
            self.available = True
            
        except ImportError:
            print("⚠️  Coqui TTS not installed. Run: pip install TTS")
            self.available = False
        except Exception as e:
            print(f"⚠️  Coqui TTS initialization failed: {e}")
            self.available = False
    
    def clone_and_generate(self, text: str, voice_sample_path: str, 
                          output_path: str = None) -> str:
        """
        Clone voice and generate speech - COMPLETELY FREE
        Args:
            text: Text to synthesize
            voice_sample_path: Path to user's voice sample (10-20 seconds)
            output_path: Where to save the generated audio
        Returns:
            Path to generated audio file
        """
        
        if not self.available:
            raise Exception("Coqui TTS not available. Run: pip install TTS")
        
        print(f"🎙️ FREE Coqui voice cloning: '{text[:50]}...'")
        
        try:
            # Create output path if not provided
            if output_path is None:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                output_path = temp_file.name
                temp_file.close()
            
            # Clone voice and generate speech
            print("🔄 Processing with Coqui TTS (this may take 10-30 seconds)...")
            
            self.tts.tts_to_file(
                text=text,
                speaker_wav=voice_sample_path,  # User's voice sample
                language="en",
                file_path=output_path
            )
            
            print(f"✅ FREE voice cloning complete: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Coqui TTS failed: {e}")
            raise e
    
    def is_available(self) -> bool:
        """Check if Coqui TTS is available"""
        return self.available

# Quick test function
def test_coqui_cloning():
    """Test Coqui TTS voice cloning"""
    
    cloner = CoquiFreeVoiceCloner()
    
    if not cloner.is_available():
        print("❌ Install Coqui TTS first:")
        print("   pip install TTS")
        return
    
    print("🎉 Coqui TTS ready for FREE voice cloning!")
    print("📊 Benefits:")
    print("   ✅ Completely FREE")
    print("   ✅ No API limits") 
    print("   ✅ Runs locally")
    print("   ✅ Good quality voice cloning")

if __name__ == "__main__":
    test_coqui_cloning()
