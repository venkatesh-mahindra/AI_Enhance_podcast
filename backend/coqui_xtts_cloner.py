"""
Coqui XTTS Voice Cloning - FREE & Self-Hosted
Zero API costs, runs locally, supports voice cloning from short audio samples
"""

import os
import tempfile
import torch
from pathlib import Path
from typing import Optional
import warnings
warnings.filterwarnings("ignore")

class CoquiXTTSCloner:
    def __init__(self):
        """Initialize Coqui XTTS voice cloner"""
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🚀 Initializing Coqui XTTS (Free Voice Cloning)")
        print(f"   Device: {self.device}")
        
        try:
            from TTS.api import TTS
            self.model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(self.device)
            print("✅ Coqui XTTS loaded successfully!")
            print("   - ₹0 cost forever")
            print("   - Voice cloning from short samples")
            print("   - Multi-language support")
        except ImportError:
            print("❌ TTS library not found. Install with: pip install TTS")
            raise
        except Exception as e:
            print(f"❌ Failed to load XTTS model: {e}")
            raise
    
    def clone_voice(self, 
                   text: str, 
                   reference_audio_path: str, 
                   output_path: Optional[str] = None,
                   language: str = "en") -> str:
        """
        Clone voice and generate speech
        
        Args:
            text: Text to convert to speech
            reference_audio_path: Path to reference audio (3-10 seconds recommended)
            output_path: Output file path (optional)
            language: Language code (default: "en")
            
        Returns:
            Path to generated audio file
        """
        if not self.model:
            raise Exception("Model not initialized")
        
        if not os.path.exists(reference_audio_path):
            raise FileNotFoundError(f"Reference audio not found: {reference_audio_path}")
        
        # Create output path if not provided
        if not output_path:
            output_path = tempfile.mktemp(suffix=".wav")
        
        try:
            print(f"🎙️ Cloning voice from: {os.path.basename(reference_audio_path)}")
            print(f"   Text length: {len(text)} characters")
            print(f"   Language: {language}")
            
            # Generate speech with cloned voice
            self.model.tts_to_file(
                text=text,
                speaker_wav=reference_audio_path,
                language=language,
                file_path=output_path
            )
            
            print(f"✅ Voice cloned successfully!")
            print(f"   Output: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Voice cloning failed: {e}")
            raise
    
    def get_supported_languages(self) -> list:
        """Get list of supported languages"""
        return [
            "en",    # English
            "es",    # Spanish
            "fr",    # French
            "de",    # German
            "it",    # Italian
            "pt",    # Portuguese
            "pl",    # Polish
            "tr",    # Turkish
            "ru",    # Russian
            "nl",    # Dutch
            "cs",    # Czech
            "ar",    # Arabic
            "zh-cn", # Chinese
            "ja",    # Japanese
            "hu",    # Hungarian
            "ko"     # Korean
        ]
    
    def is_available(self) -> bool:
        """Check if model is loaded and ready"""
        return self.model is not None


# Simple test function
def test_voice_cloning(reference_audio: str, test_text: str = None):
    """Test voice cloning with a reference audio file"""
    
    if test_text is None:
        test_text = "Hello, this is a test of the Coqui XTTS voice cloning system. It can clone voices from just a few seconds of audio."
    
    print("="*60)
    print("🧪 TESTING COQUI XTTS VOICE CLONING")
    print("="*60)
    
    try:
        # Initialize cloner
        cloner = CoquiXTTSCloner()
        
        # Test cloning
        output_file = cloner.clone_voice(
            text=test_text,
            reference_audio_path=reference_audio,
            output_path="test_cloned_voice.wav",
            language="en"
        )
        
        print("\n" + "="*60)
        print("🎉 SUCCESS!")
        print("="*60)
        print(f"✅ Voice cloned and saved to: {output_file}")
        print(f"📊 File size: {os.path.getsize(output_file) / 1024:.1f} KB")
        print(f"💡 Play the audio to verify quality!")
        print("="*60)
        
        return output_file
        
    except Exception as e:
        print("\n" + "="*60)
        print("❌ TEST FAILED")
        print("="*60)
        print(f"Error: {e}")
        print("="*60)
        return None


if __name__ == "__main__":
    import sys
    
    print("🎙️ Coqui XTTS Voice Cloner")
    print("=" * 60)
    
    # Check if audio file provided
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
        test_text = sys.argv[2] if len(sys.argv) > 2 else None
        test_voice_cloning(audio_file, test_text)
    else:
        print("Usage: python coqui_xtts_cloner.py <audio_file> [text]")
        print("\nExample:")
        print('  python coqui_xtts_cloner.py voice.mp3 "Hello world"')
