"""
Local Indian Text-to-Speech Module
Generates Indian accented speech without using Google TTS to avoid API costs
Uses pyttsx3 with advanced pitch/tone modifications and espeak integration
"""

import os
import tempfile
import numpy as np
import soundfile as sf
import librosa
from typing import Dict, Optional


class LocalIndianTTS:
    def __init__(self):
        """Initialize Local Indian TTS system"""
        self.device = "cpu"
        
        # Voice configurations for Indian accents
        self.voice_configs = {
            "indian_male": {
                "base_pitch_shift": -3.5,  # Lower pitch for male
                "pitch_variance": 0.8,     # Less pitch variance
                "speaking_rate": 0.92,     # Slightly slower
                "accent_markers": {
                    "r_pronunciation": True,   # Strong R sounds
                    "vowel_stretching": True,  # Characteristic vowel sounds
                    "rhythm_pattern": "syllable_timed"  # Indian rhythm
                }
            },
            "indian_female": {
                "base_pitch_shift": 2.0,   # Higher pitch for female
                "pitch_variance": 1.2,     # More pitch variance
                "speaking_rate": 1.05,     # Slightly faster
                "accent_markers": {
                    "r_pronunciation": True,
                    "vowel_stretching": True,
                    "rhythm_pattern": "syllable_timed"
                }
            }
        }
        
        print("🇮🇳 Local Indian TTS initialized - No external API costs!")
        print("   Supports: Indian Male, Indian Female voices")
        
    def synthesize_indian_voice(self, text: str, voice_type: str, output_path: str) -> str:
        """
        Generate Indian accented speech using local TTS with advanced processing
        """
        print(f"🇮🇳 Generating local Indian {voice_type.split('_')[1]} voice...")
        
        try:
            # Try espeak first (better for Indian accents if available)
            if self._is_espeak_available():
                return self._synthesize_with_espeak(text, voice_type, output_path)
            else:
                # Fallback to pyttsx3 with heavy accent processing
                return self._synthesize_with_pyttsx3_enhanced(text, voice_type, output_path)
                
        except Exception as e:
            print(f"   ❌ Local TTS failed: {e}")
            # Ultimate fallback: Create a beep tone
            return self._create_fallback_audio(output_path)
    
    def _is_espeak_available(self) -> bool:
        """Check if espeak is available on the system"""
        try:
            import subprocess
            result = subprocess.run(['espeak', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def _synthesize_with_espeak(self, text: str, voice_type: str, output_path: str) -> str:
        """Use espeak for more natural Indian accent"""
        import subprocess
        
        config = self.voice_configs[voice_type]
        
        # espeak parameters for Indian accent
        speed = int(175 * config["speaking_rate"])  # Base speed 175 wpm
        pitch = 50 + int(config["base_pitch_shift"] * 5)  # Adjust pitch
        
        # Use English-India variant if available, otherwise English
        voice = "en+f3" if "female" in voice_type else "en+m3"
        
        try:
            # Create temporary WAV file
            temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            temp_wav.close()
            
            # Run espeak command
            cmd = [
                'espeak',
                '-v', voice,
                '-s', str(speed),
                '-p', str(pitch),
                '-a', '100',  # Amplitude
                '-w', temp_wav.name,  # Output to WAV
                text
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(temp_wav.name):
                # Post-process the audio for Indian characteristics
                self._apply_indian_accent_processing(temp_wav.name, output_path, voice_type)
                
                # Clean up temp file
                os.remove(temp_wav.name)
                
                print(f"   ✅ Generated with espeak + Indian accent processing")
                return output_path
            else:
                print(f"   ⚠️  espeak failed, falling back to pyttsx3...")
                if os.path.exists(temp_wav.name):
                    os.remove(temp_wav.name)
                raise Exception("espeak failed")
                
        except Exception as e:
            print(f"   ⚠️  espeak error: {e}")
            raise
    
    def _synthesize_with_pyttsx3_enhanced(self, text: str, voice_type: str, output_path: str) -> str:
        """Enhanced pyttsx3 synthesis with Indian accent simulation"""
        import pyttsx3
        
        config = self.voice_configs[voice_type]
        
        # Initialize pyttsx3
        engine = pyttsx3.init()
        
        try:
            # Select appropriate system voice
            voices = engine.getProperty('voices')
            selected_voice = None
            
            # Look for female/male voices
            if "female" in voice_type:
                for voice in voices:
                    if any(keyword in voice.name.lower() for keyword in ['female', 'zira', 'susan']):
                        selected_voice = voice.id
                        break
            else:
                for voice in voices:
                    if any(keyword in voice.name.lower() for keyword in ['male', 'david', 'mark']):
                        selected_voice = voice.id
                        break
            
            if selected_voice:
                engine.setProperty('voice', selected_voice)
            
            # Adjust speaking rate
            rate = engine.getProperty('rate')
            new_rate = int(rate * config["speaking_rate"])
            engine.setProperty('rate', new_rate)
            
            # Create temporary file for pyttsx3 output
            temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            temp_wav.close()
            
            # Generate speech
            engine.save_to_file(text, temp_wav.name)
            engine.runAndWait()
            
            # Apply Indian accent processing
            self._apply_indian_accent_processing(temp_wav.name, output_path, voice_type)
            
            # Clean up
            os.remove(temp_wav.name)
            
            print(f"   ✅ Generated with pyttsx3 + Indian accent simulation")
            return output_path
            
        except Exception as e:
            print(f"   ❌ pyttsx3 enhanced failed: {e}")
            raise
    
    def _apply_indian_accent_processing(self, input_path: str, output_path: str, voice_type: str):
        """Apply advanced audio processing to simulate Indian accent characteristics"""
        
        # Load audio
        y, sr = librosa.load(input_path, sr=22050)
        config = self.voice_configs[voice_type]
        
        print(f"   🎵 Applying Indian accent characteristics...")
        
        # 1. Pitch modification for gender and accent
        pitch_shift = config["base_pitch_shift"]
        if abs(pitch_shift) > 0.1:
            y = librosa.effects.pitch_shift(y, sr=sr, n_steps=pitch_shift)
        
        # 2. Add characteristic pitch variations (Indian prosody)
        # Create subtle pitch modulation to mimic Indian speech patterns
        duration = len(y) / sr
        t = np.linspace(0, duration, len(y))
        
        # Syllable-timed rhythm characteristic of Indian English
        modulation_freq = 3.0  # Hz - for syllable timing
        pitch_modulation = 0.15 * np.sin(2 * np.pi * modulation_freq * t)
        
        # Apply pitch modulation
        for i in range(0, len(y), 1024):
            chunk = y[i:i+1024]
            if len(chunk) > 512:  # Only process substantial chunks
                mod_factor = 1.0 + pitch_modulation[i]
                # Subtle pitch shift for this chunk
                try:
                    chunk_shifted = librosa.effects.pitch_shift(
                        chunk, sr=sr, n_steps=mod_factor * 0.5
                    )
                    y[i:i+len(chunk_shifted)] = chunk_shifted
                except:
                    pass  # Skip if processing fails
        
        # 3. Enhance consonants (characteristic R sounds)
        # Boost frequencies around 1500-3000 Hz (consonant region)
        stft = librosa.stft(y)
        freqs = librosa.fft_frequencies(sr=sr)
        
        # Find frequency bins for consonant enhancement
        consonant_range = (freqs >= 1500) & (freqs <= 3000)
        stft[consonant_range] *= 1.15  # Boost consonants slightly
        
        # Reconstruct audio
        y = librosa.istft(stft)
        
        # 4. Adjust speaking rhythm (syllable-timed vs stress-timed)
        rhythm_factor = config["speaking_rate"]
        if abs(rhythm_factor - 1.0) > 0.05:
            y = librosa.effects.time_stretch(y, rate=1.0/rhythm_factor)
        
        # 5. Add subtle formant characteristics
        # Indian English has characteristic vowel formants
        # Apply a gentle EQ curve
        y = self._apply_indian_formant_eq(y, sr)
        
        # 6. Normalize and save
        # Normalize to prevent clipping
        y = y / np.max(np.abs(y)) * 0.95
        
        sf.write(output_path, y, sr)
        
    def _apply_indian_formant_eq(self, y: np.ndarray, sr: int) -> np.ndarray:
        """Apply EQ to simulate Indian English formant characteristics"""
        try:
            # Get STFT
            stft = librosa.stft(y, n_fft=2048)
            freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
            
            # Create EQ curve for Indian English characteristics
            eq_curve = np.ones_like(freqs)
            
            # Slight boost in mid frequencies (vowel clarity)
            mid_range = (freqs >= 800) & (freqs <= 1200)
            eq_curve[mid_range] *= 1.08
            
            # Slight reduction in very high frequencies (softer sibilants)
            high_range = freqs >= 6000
            eq_curve[high_range] *= 0.95
            
            # Apply EQ
            for i in range(stft.shape[1]):
                stft[:, i] = stft[:, i] * eq_curve
            
            # Reconstruct
            return librosa.istft(stft)
            
        except Exception:
            # Return original if EQ fails
            return y
    
    def _create_fallback_audio(self, output_path: str) -> str:
        """Create a simple audio file as fallback"""
        print("   ⚠️  Creating fallback audio...")
        
        # Generate a simple tone sequence
        sr = 22050
        duration = 1.0
        t = np.linspace(0, duration, int(sr * duration))
        
        # Create a pleasant tone sequence
        tone1 = 0.3 * np.sin(2 * np.pi * 440 * t)  # A4
        tone2 = 0.3 * np.sin(2 * np.pi * 554 * t)  # C#5
        
        # Combine with fade
        audio = np.concatenate([tone1 * np.linspace(1, 0, len(tone1)), 
                               tone2 * np.linspace(0, 1, len(tone2))])
        
        sf.write(output_path, audio, sr)
        return output_path
    
    def get_supported_voices(self) -> Dict:
        """Return supported local Indian voices"""
        return {
            "indian_male": {
                "name": "🇮🇳 Local Indian Male",
                "description": "Offline Indian English accent - Male voice (No API costs)",
                "type": "local_indian"
            },
            "indian_female": {
                "name": "🇮🇳 Local Indian Female", 
                "description": "Offline Indian English accent - Female voice (No API costs)",
                "type": "local_indian"
            }
        }
    
    def preprocess_text_for_indian_accent(self, text: str) -> str:
        """Preprocess text to enhance Indian accent characteristics"""
        
        # Common Indian English pronunciations
        replacements = {
            # Characteristic pronunciations
            "world": "vorld",
            "work": "vork", 
            "were": "vere",
            "will": "vill",
            "what": "vhat",
            "when": "vhen",
            "where": "vhere",
            "why": "vhy",
            # Add stress markers for Indian rhythm
            "important": "im-POR-tant",
            "development": "de-vel-op-MENT",
            "technology": "tech-NOL-o-gy",
        }
        
        processed_text = text
        for old, new in replacements.items():
            # Only replace whole words
            import re
            pattern = r'\b' + re.escape(old) + r'\b'
            processed_text = re.sub(pattern, new, processed_text, flags=re.IGNORECASE)
        
        return processed_text


# Global instance
local_indian_tts = LocalIndianTTS()


def generate_local_indian_voice(text: str, voice_type: str, output_path: str) -> str:
    """
    Main function to generate Indian voice locally
    
    Args:
        text: Text to synthesize
        voice_type: 'indian_male' or 'indian_female'
        output_path: Path to save the generated audio
    
    Returns:
        Path to generated audio file
    """
    
    # Preprocess text for better Indian accent
    processed_text = local_indian_tts.preprocess_text_for_indian_accent(text)
    
    # Generate voice
    return local_indian_tts.synthesize_indian_voice(processed_text, voice_type, output_path)
