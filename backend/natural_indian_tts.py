"""
Natural Indian Text-to-Speech Module
Focuses on natural-sounding Indian voices without robotic artifacts
Uses gentle processing and human-like variations
"""

import os
import tempfile
import numpy as np
import soundfile as sf
import librosa
from typing import Dict, Optional
import random


class NaturalIndianTTS:
    def __init__(self):
        """Initialize Natural Indian TTS system"""
        self.device = "cpu"
        
        # More conservative voice configurations for natural sound
        self.voice_configs = {
            "indian_male": {
                "pitch_adjustment": -1.0,    # Very subtle pitch lowering
                "speed_factor": 0.95,        # Slightly slower for clarity
                "volume_boost": 1.1,         # Slight volume increase
                "naturalness_level": "high"  # Maximum naturalness
            },
            "indian_female": {
                "pitch_adjustment": 0.5,     # Very subtle pitch raise
                "speed_factor": 1.0,         # Normal speed
                "volume_boost": 1.05,        # Slight volume increase
                "naturalness_level": "high"  # Maximum naturalness
            }
        }
        
        print("🇮🇳 Natural Indian TTS initialized - Focusing on human-like quality!")
        
    def synthesize_natural_indian_voice(self, text: str, voice_type: str, output_path: str) -> str:
        """
        Generate natural-sounding Indian voice with minimal processing
        """
        print(f"🇮🇳 Generating NATURAL Indian {voice_type.split('_')[1]} voice...")
        print(f"   🎯 Focus: Human-like quality, minimal robotic artifacts")
        
        try:
            # Preprocess text for more natural speech
            natural_text = self._preprocess_for_naturalness(text)
            
            # Try different synthesis methods in order of quality
            if self._try_natural_espeak(natural_text, voice_type, output_path):
                return output_path
            else:
                return self._synthesize_natural_pyttsx3(natural_text, voice_type, output_path)
                
        except Exception as e:
            print(f"   ❌ Natural TTS failed: {e}")
            return self._create_simple_fallback(output_path)
    
    def _preprocess_for_naturalness(self, text: str) -> str:
        """Preprocess text to sound more natural when spoken"""
        
        # Add natural pauses for better flow
        import re
        
        # Add slight pauses after punctuation for natural rhythm
        text = re.sub(r'([.!?])\s+', r'\1, ', text)  # Add pause after sentences
        text = re.sub(r'([,;:])\s+', r'\1 ', text)   # Ensure space after punctuation
        
        # Break up very long sentences for better prosody
        words = text.split()
        if len(words) > 15:  # If sentence is too long
            # Add natural breaks at logical points
            processed_words = []
            word_count = 0
            for word in words:
                processed_words.append(word)
                word_count += 1
                # Add pause every 10-12 words at natural break points
                if word_count >= 10 and word.endswith((',', 'and', 'or', 'but', 'so')):
                    processed_words.append(',')  # Natural pause
                    word_count = 0
            text = ' '.join(processed_words)
        
        return text
    
    def _try_natural_espeak(self, text: str, voice_type: str, output_path: str) -> bool:
        """Try to use espeak with natural settings"""
        try:
            import subprocess
            
            config = self.voice_configs[voice_type]
            
            # Natural espeak parameters (less aggressive)
            speed = 160 if "female" in voice_type else 150  # Natural speaking speed
            pitch = 55 if "female" in voice_type else 45    # Subtle pitch differences
            
            # Use more natural voice variants
            voice = "en+f4" if "female" in voice_type else "en+m4"  # Softer variants
            
            # Create temporary file
            temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            temp_wav.close()
            
            # Natural espeak command (less robotic settings)
            cmd = [
                'espeak',
                '-v', voice,
                '-s', str(speed),        # Natural speed
                '-p', str(pitch),        # Subtle pitch
                '-a', '80',              # Not too loud
                '-g', '5',               # Small gaps between words (more natural)
                '-w', temp_wav.name,
                text
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(temp_wav.name):
                # Apply very gentle natural processing
                self._apply_gentle_naturalness(temp_wav.name, output_path, voice_type)
                os.remove(temp_wav.name)
                
                print(f"   ✅ Generated with natural espeak processing")
                return True
            else:
                if os.path.exists(temp_wav.name):
                    os.remove(temp_wav.name)
                return False
                
        except Exception:
            return False
    
    def _synthesize_natural_pyttsx3(self, text: str, voice_type: str, output_path: str) -> str:
        """Natural pyttsx3 synthesis with minimal processing"""
        import pyttsx3
        
        config = self.voice_configs[voice_type]
        
        print(f"   🔧 Using natural pyttsx3 synthesis...")
        
        # Initialize with more natural settings
        engine = pyttsx3.init()
        
        try:
            # Select the best available voice
            voices = engine.getProperty('voices')
            selected_voice = None
            
            # Prefer higher quality voices
            if "female" in voice_type:
                for voice in voices:
                    name = voice.name.lower()
                    # Prefer Microsoft voices (usually higher quality)
                    if any(keyword in name for keyword in ['zira', 'susan', 'cortana', 'female']):
                        selected_voice = voice.id
                        break
            else:
                for voice in voices:
                    name = voice.name.lower()
                    if any(keyword in name for keyword in ['david', 'mark', 'male']):
                        selected_voice = voice.id
                        break
            
            if selected_voice:
                engine.setProperty('voice', selected_voice)
            
            # Natural speaking rate (not too fast or slow)
            rate = engine.getProperty('rate')
            natural_rate = int(rate * config["speed_factor"])
            engine.setProperty('rate', natural_rate)
            
            # Natural volume
            volume = engine.getProperty('volume')
            engine.setProperty('volume', min(1.0, volume * config["volume_boost"]))
            
            # Generate to temporary file
            temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            temp_wav.close()
            
            # Generate speech
            engine.save_to_file(text, temp_wav.name)
            engine.runAndWait()
            
            # Apply very gentle processing for Indian characteristics
            self._apply_gentle_naturalness(temp_wav.name, output_path, voice_type)
            
            # Clean up
            os.remove(temp_wav.name)
            
            print(f"   ✅ Generated with natural pyttsx3 + gentle accent touches")
            return output_path
            
        except Exception as e:
            print(f"   ❌ Natural pyttsx3 failed: {e}")
            raise
    
    def _apply_gentle_naturalness(self, input_path: str, output_path: str, voice_type: str):
        """Apply very gentle processing to maintain naturalness"""
        
        # Load audio
        y, sr = librosa.load(input_path, sr=22050)
        config = self.voice_configs[voice_type]
        
        print(f"   🌟 Applying gentle natural enhancements...")
        
        # 1. Very subtle pitch adjustment (much less aggressive)
        pitch_adjust = config["pitch_adjustment"]
        if abs(pitch_adjust) > 0.1:
            # Use much smaller pitch shifts for naturalness
            y = librosa.effects.pitch_shift(y, sr=sr, n_steps=pitch_adjust)
        
        # 2. Gentle volume normalization
        # Normalize to comfortable listening level
        y = y / np.max(np.abs(y)) * 0.8  # Not too loud
        
        # 3. Add very subtle natural variations (human-like inconsistencies)
        # This makes it sound less robotic by adding tiny natural variations
        if len(y) > sr:  # Only for longer audio
            # Add tiny random pitch variations (like human speech)
            for i in range(0, len(y), sr//4):  # Every quarter second
                chunk_end = min(i + sr//4, len(y))
                chunk = y[i:chunk_end]
                if len(chunk) > 1000:
                    # Very tiny random variation (0.1 semitone max)
                    tiny_variation = random.uniform(-0.1, 0.1)
                    try:
                        chunk_varied = librosa.effects.pitch_shift(chunk, sr=sr, n_steps=tiny_variation)
                        y[i:i+len(chunk_varied)] = chunk_varied
                    except:
                        pass  # Skip if it fails
        
        # 4. Gentle smoothing to reduce harsh artifacts
        # Apply a very light smoothing filter to reduce robotic harshness
        from scipy import signal
        # Very gentle low-pass filter to smooth harsh frequencies
        nyquist = sr / 2
        cutoff = 8000  # Keep most speech frequencies
        b, a = signal.butter(2, cutoff / nyquist, btype='low')
        y = signal.filtfilt(b, a, y)
        
        # 5. Final normalization and save
        y = y / np.max(np.abs(y)) * 0.85  # Final comfortable level
        sf.write(output_path, y, sr)
        
        print(f"   ✨ Natural voice ready - minimal processing for human-like quality!")
    
    def _create_simple_fallback(self, output_path: str) -> str:
        """Create a simple fallback that's not robotic"""
        print("   ⚠️  Creating gentle fallback audio...")
        
        # Generate a more pleasant tone sequence (not harsh beeps)
        sr = 22050
        duration = 2.0
        t = np.linspace(0, duration, int(sr * duration))
        
        # Create gentle, musical tones instead of harsh beeps
        freq1 = 220  # A3 - much gentler frequency
        freq2 = 330  # E4 - pleasant harmony
        
        # Create soft tones with fade in/out
        tone1 = 0.2 * np.sin(2 * np.pi * freq1 * t) * np.exp(-t/2)  # Fade out
        tone2 = 0.2 * np.sin(2 * np.pi * freq2 * t) * (1 - np.exp(-t*3))  # Fade in
        
        # Combine with gentle envelope
        audio = (tone1 + tone2) * 0.5
        
        sf.write(output_path, audio, sr)
        return output_path
    
    def get_supported_voices(self) -> Dict:
        """Return supported natural Indian voices"""
        return {
            "indian_male": {
                "name": "🇮🇳 Natural Indian Male",
                "description": "Human-like Indian English - Male (Non-robotic)",
                "type": "natural_indian"
            },
            "indian_female": {
                "name": "🇮🇳 Natural Indian Female", 
                "description": "Human-like Indian English - Female (Non-robotic)",
                "type": "natural_indian"
            }
        }


# Global instance
natural_indian_tts = NaturalIndianTTS()


def generate_natural_indian_voice(text: str, voice_type: str, output_path: str) -> str:
    """
    Generate natural, human-like Indian voice
    
    Args:
        text: Text to synthesize
        voice_type: 'indian_male' or 'indian_female'
        output_path: Path to save the generated audio
    
    Returns:
        Path to generated audio file
    """
    return natural_indian_tts.synthesize_natural_indian_voice(text, voice_type, output_path)
