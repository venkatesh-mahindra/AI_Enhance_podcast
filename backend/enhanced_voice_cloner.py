"""
Enhanced Voice Cloner - Better Custom Voice Quality
Addresses robotic/mixed voice issues with advanced processing
"""

import os
import tempfile
import librosa
import numpy as np
import soundfile as sf
from typing import Dict, Optional
from pydub import AudioSegment

class EnhancedVoiceCloner:
    def __init__(self):
        """Initialize enhanced voice cloner"""
        print("🎙️ Enhanced Voice Cloner initialized")
        print("   ✅ Advanced voice matching enabled")
        
    def analyze_voice_advanced(self, audio_path: str) -> Dict:
        """Advanced voice analysis with more characteristics"""
        try:
            # Load with higher quality
            audio, sr = librosa.load(audio_path, sr=44100)  # Higher sample rate
            
            # Basic features
            duration = librosa.get_duration(y=audio, sr=sr)
            
            # Advanced pitch analysis
            pitches, magnitudes = librosa.piptrack(y=audio, sr=sr, threshold=0.1)
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                if pitches[index, t] > 0:
                    pitch_values.append(pitches[index, t])
            
            # Voice characteristics
            pitch_mean = np.mean(pitch_values) if pitch_values else 150
            pitch_std = np.std(pitch_values) if pitch_values else 20
            
            # Formants (vocal tract resonances)
            formants = self._extract_formants(audio, sr)
            
            # Voice timbre features
            mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
            mfcc_mean = np.mean(mfcc, axis=1)
            
            # Spectral features for voice quality
            spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=audio, sr=sr))
            spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=audio, sr=sr))
            
            # Voice energy and rhythm
            energy = np.mean(librosa.feature.rms(y=audio))
            tempo, _ = librosa.beat.beat_track(y=audio, sr=sr)
            
            # Gender detection (improved - more accurate)
            # Female voices typically have pitch >= 165 Hz, but don't require both conditions
            is_female = pitch_mean >= 165  # Simplified, more reliable detection
            
            print(f"🔍 Gender analysis: pitch={pitch_mean:.1f}Hz -> {'Female' if is_female else 'Male'}")
            
            return {
                "duration": float(duration),
                "pitch": {
                    "mean": float(pitch_mean),
                    "std": float(pitch_std),
                    "range": float(max(pitch_values) - min(pitch_values)) if pitch_values else 50
                },
                "formants": formants,
                "mfcc": mfcc_mean.tolist(),
                "spectral": {
                    "centroid": float(spectral_centroid),
                    "rolloff": float(spectral_rolloff)
                },
                "energy": float(energy),
                "tempo": float(tempo),
                "is_female": is_female,
                "quality": self._assess_quality(audio, sr),
                "sr": sr
            }
            
        except Exception as e:
            raise Exception(f"Enhanced voice analysis failed: {str(e)}")
    
    def _extract_formants(self, audio, sr):
        """Extract formant frequencies (vocal tract resonances)"""
        try:
            # Pre-emphasis
            pre_emphasized = np.append(audio[0], audio[1:] - 0.97 * audio[:-1])
            
            # Window the signal
            windowed = pre_emphasized * np.hanning(len(pre_emphasized))
            
            # LPC analysis for formants
            from scipy import signal
            lpc_coeffs = self._lpc_analysis(windowed, order=12)
            roots = np.roots(lpc_coeffs)
            
            # Extract formants from LPC roots
            formants = []
            for root in roots:
                if np.imag(root) != 0:
                    freq = np.abs(np.angle(root)) * sr / (2 * np.pi)
                    if 200 < freq < 4000:  # Typical formant range
                        formants.append(freq)
            
            formants.sort()
            return {
                "f1": formants[0] if len(formants) > 0 else 700,
                "f2": formants[1] if len(formants) > 1 else 1200,
                "f3": formants[2] if len(formants) > 2 else 2500
            }
        except:
            # Fallback formant values
            return {"f1": 700, "f2": 1200, "f3": 2500}
    
    def _lpc_analysis(self, signal, order):
        """Linear Predictive Coding analysis"""
        try:
            from scipy.signal import lfilter
            # Simple LPC implementation
            R = np.correlate(signal, signal, mode='full')
            R = R[len(R)//2:]
            r = R[:order+1]
            
            # Levinson-Durbin algorithm (simplified)
            a = np.zeros(order + 1)
            a[0] = 1.0
            
            for i in range(1, order + 1):
                k = -sum(a[j] * r[i-j] for j in range(i)) / r[0]
                a[1:i+1] = a[1:i+1] + k * a[i-1:0:-1]
                a[i] = k
            
            return a
        except:
            return np.array([1.0] + [0.0] * order)
    
    def _assess_quality(self, audio, sr):
        """Assess audio quality for voice cloning"""
        try:
            # SNR estimation
            signal_power = np.mean(audio ** 2)
            noise_power = np.mean((audio - np.mean(audio)) ** 2) * 0.1
            snr = 10 * np.log10(signal_power / max(noise_power, 1e-10))
            
            # Clipping detection
            clipping_ratio = np.sum(np.abs(audio) > 0.95) / len(audio)
            
            # Dynamic range
            dynamic_range = np.max(np.abs(audio)) - np.min(np.abs(audio))
            
            if snr > 25 and clipping_ratio < 0.01 and dynamic_range > 0.1:
                return "excellent"
            elif snr > 15 and clipping_ratio < 0.05:
                return "good"
            elif snr > 10:
                return "fair"
            else:
                return "poor"
        except:
            return "unknown"
    
    def synthesize_enhanced_custom_voice(self, text: str, voice_profile: Dict, 
                                       output_path: str = None) -> str:
        """Enhanced custom voice synthesis with better quality"""
        print(f"🎯 Enhanced voice synthesis: '{text[:30]}...'")
        
        try:
            # Determine correct gender for synthesis
            is_female = voice_profile.get("is_female", False)
            gender = "indian_female" if is_female else "indian_male"
            
            print(f"🚨 GENDER DEBUG: is_female={is_female}, using {gender} voice")
            
            # Use pyttsx3 directly for base voice (avoid circular import)
            import pyttsx3
            from pydub import AudioSegment
            
            temp_base = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            temp_base.close()
            
            # Generate base audio with correct gender
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            
            # Select appropriate voice based on gender
            if is_female and len(voices) > 1:
                # Use female voice (usually index 1)
                engine.setProperty('voice', voices[1].id)
                print(f"🎭 Selected FEMALE voice: {voices[1].id}")
            elif len(voices) > 0:
                # Use male voice (usually index 0)  
                engine.setProperty('voice', voices[0].id)
                print(f"🎭 Selected MALE voice: {voices[0].id}")
            
            # Set speech properties
            engine.setProperty('rate', 180)
            engine.setProperty('volume', 0.9)
            
            # Generate audio
            engine.save_to_file(text, temp_base.name)
            engine.runAndWait()
            
            base_audio_path = temp_base.name
            
            # Load and enhance with user's voice characteristics
            enhanced_path = self._apply_voice_characteristics(
                base_audio_path, voice_profile, output_path
            )
            
            # Cleanup temp file
            os.unlink(temp_base.name)
            
            print("✅ Enhanced voice synthesis complete")
            return enhanced_path
            
        except Exception as e:
            print(f"⚠️ Enhanced synthesis failed: {e}")
            # Fallback to basic method
            return self._fallback_synthesis(text, voice_profile, output_path)
    
    def _apply_voice_characteristics(self, base_path: str, profile: Dict, 
                                   output_path: str = None) -> str:
        """Apply user voice characteristics to base audio"""
        
        if output_path is None:
            output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
        
        try:
            # Load base audio
            audio, sr = librosa.load(base_path, sr=profile.get("sr", 22050))
            
            # Apply voice characteristics
            modified_audio = self._apply_advanced_modifications(audio, sr, profile)
            
            # Save enhanced audio
            sf.write(output_path, modified_audio, sr)
            
            return output_path
            
        except Exception as e:
            print(f"⚠️ Voice characteristic application failed: {e}")
            # Return original if processing fails
            return base_path
    
    def _apply_advanced_modifications(self, audio, sr, profile):
        """Apply advanced voice modifications"""
        
        # Pitch adjustment (more natural)
        target_pitch = profile.get("pitch", {}).get("mean", 150)
        current_pitch = 150  # Approximate base pitch
        
        if target_pitch != current_pitch:
            # Gentle pitch shifting (max ±3 semitones)
            semitones = np.clip(librosa.hz_to_midi([target_pitch])[0] - 
                              librosa.hz_to_midi([current_pitch])[0], -3, 3)
            
            if abs(semitones) > 0.2:  # Only shift if significant difference
                audio = librosa.effects.pitch_shift(audio, sr=sr, n_steps=semitones)
        
        # Formant adjustment for voice timbre
        formants = profile.get("formants", {})
        if formants:
            audio = self._adjust_formants(audio, sr, formants)
        
        # Energy/volume matching
        target_energy = profile.get("energy", 0.1)
        current_energy = np.sqrt(np.mean(audio**2))
        
        if current_energy > 0:
            energy_ratio = np.clip(target_energy / current_energy, 0.5, 2.0)
            audio = audio * energy_ratio
        
        # Apply gentle filtering for voice quality
        audio = self._apply_voice_filter(audio, sr, profile)
        
        return audio
    
    def _adjust_formants(self, audio, sr, formants):
        """Adjust formants for voice timbre matching"""
        try:
            # Simple formant adjustment using spectral envelope modification
            stft = librosa.stft(audio, n_fft=2048, hop_length=512)
            magnitude = np.abs(stft)
            phase = np.angle(stft)
            
            # Apply gentle formant shifts
            f1_target = formants.get("f1", 700)
            f2_target = formants.get("f2", 1200)
            
            # Frequency bins
            freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
            
            # Gentle spectral envelope adjustment
            for i, freq in enumerate(freqs):
                if 200 < freq < 1000:  # F1 region
                    factor = min(1.2, max(0.8, f1_target / 700))
                    if i < len(magnitude):
                        magnitude[i] *= factor
                elif 1000 < freq < 2000:  # F2 region  
                    factor = min(1.2, max(0.8, f2_target / 1200))
                    if i < len(magnitude):
                        magnitude[i] *= factor
            
            # Reconstruct audio
            modified_stft = magnitude * np.exp(1j * phase)
            audio = librosa.istft(modified_stft, hop_length=512)
            
            return audio
        except:
            return audio  # Return original if formant adjustment fails
    
    def _apply_voice_filter(self, audio, sr, profile):
        """Apply gentle filtering for voice quality"""
        try:
            # Try scipy first
            try:
                from scipy import signal
                
                # Gentle high-pass filter to reduce muddiness
                sos = signal.butter(2, 100, btype='high', fs=sr, output='sos')
                audio = signal.sosfilt(sos, audio)
                
                # Gentle low-pass filter to reduce harshness
                sos = signal.butter(2, 8000, btype='low', fs=sr, output='sos')
                audio = signal.sosfilt(sos, audio)
                
            except ImportError:
                # Fallback: Simple filtering without scipy
                print("⚠️  Scipy not available, using basic filtering")
                
                # Basic high-pass filtering
                n_fft = 2048
                stft = librosa.stft(audio, n_fft=n_fft)
                freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
                
                # Gentle high-pass (reduce frequencies below 100 Hz)
                for i, freq in enumerate(freqs):
                    if freq < 100:
                        stft[i] *= max(0.1, freq / 100)
                    elif freq > 8000:  # Gentle low-pass
                        stft[i] *= max(0.1, 8000 / freq)
                
                audio = librosa.istft(stft)
            
            # Normalize
            if np.max(np.abs(audio)) > 0:
                audio = audio / np.max(np.abs(audio)) * 0.9
            
            return audio
        except Exception as e:
            print(f"⚠️  Voice filtering failed: {e}")
            return audio
    
    def _fallback_synthesis(self, text: str, voice_profile: Dict, output_path: str = None):
        """Fallback to basic synthesis if enhanced fails"""
        print("🔄 Using fallback synthesis method")
        
        try:
            import pyttsx3
            
            if output_path is None:
                output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
            
            engine = pyttsx3.init()
            
            # Set voice properties based on profile
            voices = engine.getProperty('voices')
            if voice_profile.get("is_female") and len(voices) > 1:
                engine.setProperty('voice', voices[1].id)
            elif len(voices) > 0:
                engine.setProperty('voice', voices[0].id)
            
            # Adjust rate and volume
            rate = int(200 * voice_profile.get("speech_rate", {}).get("mean", 1.0))
            engine.setProperty('rate', max(100, min(300, rate)))
            engine.setProperty('volume', min(1.0, voice_profile.get("energy", 0.8) * 2))
            
            # Save to file
            engine.save_to_file(text, output_path)
            engine.runAndWait()
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Fallback synthesis failed: {str(e)}")
