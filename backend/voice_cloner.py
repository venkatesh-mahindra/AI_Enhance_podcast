"""
Voice Cloner Module
Analyzes user voice and creates voice profile for TTS
Note: Simplified version without Coqui TTS for initial setup
"""

import json
import os
from typing import Dict

import librosa
import numpy as np

# Import Coqui XTTS voice cloning (FREE & Self-Hosted - PRIMARY METHOD)
try:
    from coqui_xtts_cloner import CoquiXTTSCloner
    COQUI_XTTS_AVAILABLE = True
    print("✅ Coqui XTTS Voice Cloner available (FREE - ₹0 forever)")
except ImportError as e:
    print(f"⚠️  Coqui XTTS not available: {e}")
    print("   Install with: pip install TTS")
    COQUI_XTTS_AVAILABLE = False


class VoiceCloner:
    def __init__(self):
        """Initialize voice cloner with FREE Coqui XTTS"""
        self.device = "cpu"
        
        # Initialize Coqui XTTS cloner (FREE - Primary method)
        if COQUI_XTTS_AVAILABLE:
            try:
                self.coqui_cloner = CoquiXTTSCloner()
                print("🎙️ Coqui XTTS voice cloning initialized (FREE - ₹0 forever)")
            except Exception as e:
                print(f"⚠️  Coqui XTTS initialization failed: {e}")
                self.coqui_cloner = None
        else:
            self.coqui_cloner = None

        # Default voice options
        self.default_voices = {
            "indian_male": {
                "name": "Indian Male",
                "description": "Indian English accent - Male voice",
                "sample_path": None,
                "type": "indian",
                "accent": "co.in",
            },
            "indian_female": {
                "name": "Indian Female",
                "description": "Indian English accent - Female voice",
                "sample_path": None,
                "type": "indian",
                "accent": "co.in",
            },
            "male": {
                "name": "Professional Male (US)",
                "description": "Deep, authoritative voice - US accent",
                "sample_path": "default_voices/male_sample.wav",
                "type": "default",
            },
            "female": {
                "name": "Professional Female (US)",
                "description": "Clear, engaging voice - US accent",
                "sample_path": "default_voices/female_sample.wav",
                "type": "default",
            },
            "ai_neutral": {
                "name": "AI Neutral (US)",
                "description": "Modern AI-generated voice - US accent",
                "sample_path": None,
                "type": "ai",
            },
            "ai_energetic": {
                "name": "AI Energetic (US)",
                "description": "Upbeat, enthusiastic AI voice - US accent",
                "sample_path": None,
                "type": "ai",
            },
        }

        # Supported languages
        self.supported_languages = [
            "en",
            "es",
            "fr",
            "de",
            "it",
            "pt",
            "pl",
            "tr",
            "ru",
            "nl",
            "cs",
            "ar",
            "zh-cn",
            "ja",
            "hu",
            "ko",
        ]

        print("⚠️  VoiceCloner initialized in basic mode")
        print("   For full TTS functionality, install: TTS, phonemizer")

    def analyze_voice(self, audio_path: str) -> Dict:
        """
        Analyze voice sample for quality and characteristics using basic analysis
        """
        # Use basic analysis (enhanced_cloner removed)
        try:
            print("🔬 Using basic voice analysis...")
            # Load audio
            audio, sr = librosa.load(audio_path, sr=22050)

            # Calculate duration
            duration = librosa.get_duration(y=audio, sr=sr)

            # Extract basic features
            pitch = librosa.yin(audio, fmin=50, fmax=500)
            pitch_mean = np.nanmean(pitch)
            pitch_std = np.nanstd(pitch)

            # Energy/volume
            rms = librosa.feature.rms(y=audio)[0]
            energy_mean = np.mean(rms)

            # Spectral features
            spectral_centroids = librosa.feature.spectral_centroid(y=audio, sr=sr)[0]
            spectral_mean = np.mean(spectral_centroids)

            # Check audio quality
            signal_to_noise = self._estimate_snr(audio)
            quality = (
                "good"
                if signal_to_noise > 20
                else "fair"
                if signal_to_noise > 10
                else "poor"
            )

            # Improved gender detection (more accurate threshold)
            is_female = pitch_mean >= 165 if not np.isnan(pitch_mean) else False
            
            print(f"🔍 Basic gender analysis: pitch={pitch_mean:.1f}Hz -> {'Female' if is_female else 'Male'}")

            basic_profile = {
                "duration": float(duration),
                "pitch": {"mean": float(pitch_mean) if not np.isnan(pitch_mean) else 150},
                "pitch_mean": float(pitch_mean) if not np.isnan(pitch_mean) else 150,
                "pitch_std": float(pitch_std) if not np.isnan(pitch_std) else 20,
                "energy": float(energy_mean),
                "spectral_centroid": float(spectral_mean),
                "quality": quality,
                "sample_rate": sr,
                "is_female": is_female,
                "enhanced": False
            }
            
            print(f"✅ Basic analysis complete - Quality: {quality}")
            return basic_profile

        except Exception as e:
            raise Exception(f"Error analyzing voice: {str(e)}")

    def _estimate_snr(self, audio: np.ndarray) -> float:
        """Estimate signal-to-noise ratio"""
        try:
            signal_power = np.mean(audio**2)
            noise_power = np.var(audio)

            if noise_power == 0:
                return 100.0

            snr = 10 * np.log10(signal_power / noise_power)
            return float(snr)

        except:
            return 0.0

    def create_profile(self, audio_path: str, job_id: str) -> Dict:
        """
        Create voice profile for cloning with detailed characteristics
        """
        try:
            # Load and analyze audio
            audio, sr = librosa.load(audio_path, sr=22050)
            duration = librosa.get_duration(y=audio, sr=sr)

            # Pitch analysis
            pitch = librosa.yin(audio, fmin=50, fmax=500)
            pitch_mean = np.nanmean(pitch[pitch > 0])  # Only valid pitches
            pitch_std = np.nanstd(pitch[pitch > 0])

            # Determine gender based on pitch (rough estimate)
            is_female = pitch_mean > 165 if not np.isnan(pitch_mean) else False

            # Energy/volume
            rms = librosa.feature.rms(y=audio)[0]
            energy_mean = np.mean(rms)
            energy_std = np.std(rms)

            # Speech rate estimation (simpler method to avoid scipy compatibility issues)
            # Estimate from zero crossing rate which correlates with speech speed
            zcr = librosa.feature.zero_crossing_rate(audio)[0]
            speech_rate = np.mean(zcr) * 10.0  # Normalize to roughly 1.0 = normal
            speech_rate = max(0.5, min(2.0, speech_rate))  # Clamp to reasonable range

            # Spectral features
            spectral_centroids = librosa.feature.spectral_centroid(y=audio, sr=sr)[0]
            spectral_mean = np.mean(spectral_centroids)

            # Quality check
            signal_to_noise = self._estimate_snr(audio)
            quality = (
                "good"
                if signal_to_noise > 20
                else "fair"
                if signal_to_noise > 10
                else "poor"
            )

            print(f"   📊 Voice Analysis:")
            print(
                f"      Gender: {'Female' if is_female else 'Male'} (pitch: {pitch_mean:.0f} Hz)"
            )
            print(f"      Duration: {duration:.1f}s")
            print(f"      Speech Rate: {speech_rate:.2f}x")
            print(f"      Quality: {quality}")

            # Create properly structured profile (convert numpy types to Python types for JSON)
            profile = {
                "job_id": job_id,
                "audio_reference": audio_path,
                "is_female": bool(is_female),  # Convert numpy.bool_ to Python bool
                "pitch": {
                    "mean": float(pitch_mean) if not np.isnan(pitch_mean) else 150.0,
                    "std": float(pitch_std) if not np.isnan(pitch_std) else 20.0,
                },
                "energy": {"mean": float(energy_mean), "std": float(energy_std)},
                "speech_rate": {
                    "mean": float(speech_rate) if not np.isnan(speech_rate) else 1.0
                },
                "spectral_centroid": float(spectral_mean),
                "analysis": {
                    "duration": float(duration),
                    "quality": quality,
                    "sample_rate": int(sr),  # Convert to Python int
                    "signal_to_noise": float(signal_to_noise),
                },
                "model": "voice_matching_v2",
            }

            return profile

        except Exception as e:
            raise Exception(f"Error creating voice profile: {str(e)}")

    def synthesize_with_true_voice_cloning(
        self,
        text: str,
        voice_profile: Dict,
        language: str = "en",
        output_path: str = None,
    ) -> str:
        """
        TRUE VOICE CLONING using Coqui TTS (if available).
        This uses the uploaded voice to actually clone the voice!
        Falls back to advanced matching if TTS not available.
        """
        print(f"🎤 TRUE VOICE CLONING: '{text[:50]}...'")

        # Try to use Coqui TTS for real voice cloning
        try:
            import os

            import torch
            from TTS.api import TTS

            voice_file = voice_profile.get("audio_reference")
            if not voice_file or not os.path.exists(voice_file):
                raise Exception("Voice reference file not found")

            print(f"   🚀 Using Coqui TTS for TRUE voice cloning...")
            print(f"   📁 Voice sample: {os.path.basename(voice_file)}")

            # Initialize TTS with voice cloning model
            tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

            # Generate with voice cloning
            tts.tts_to_file(
                text=text, speaker_wav=voice_file, language="en", file_path=output_path
            )

            print(f"   ✅ TRUE voice clone generated!")
            print(f"   🎉 This is using the ACTUAL uploaded voice!")
            return output_path

        except ImportError:
            print(
                f"   ℹ️  Coqui TTS not installed - using advanced voice matching instead"
            )
            print(f"   💡 Install TTS for TRUE voice cloning: pip install TTS torch")
            # Fall through to advanced matching
        except Exception as e:
            print(f"   ⚠️  Voice cloning failed: {e}")
            print(f"   ℹ️  Falling back to advanced voice matching...")
            # Fall through to advanced matching

        # Fallback: Advanced voice matching
        return self._synthesize_with_voice_matching(
            text, voice_profile, language, output_path
        )

    def _synthesize_with_voice_matching(
        self,
        text: str,
        voice_profile: Dict,
        language: str = "en",
        output_path: str = None,
    ) -> str:
        """
        Advanced voice matching (fallback when TRUE cloning not available).
        Uses gTTS + aggressive pitch/tone/energy matching.
        """
        print(f"🎵 Advanced voice matching: '{text[:50]}...'")

        # Extract voice characteristics from profile
        pitch = voice_profile.get("pitch", {}).get("mean", 150)
        energy = voice_profile.get("energy", {}).get("mean", 0.01)
        is_female = voice_profile.get("is_female", False)
        speech_rate = voice_profile.get("speech_rate", {}).get("mean", 1.0)

        target_pitch = pitch

        print(
            f"   📊 Target voice: {'Female' if is_female else 'Male'}, pitch={pitch:.0f} Hz, rate={speech_rate:.2f}x"
        )

        try:
            import tempfile

            import soundfile as sf
            from gtts import gTTS
            from pydub import AudioSegment

            # Use Indian English for better quality (change to 'com' for US if needed)
            tld = "co.in"  # Indian accent by default

            # Generate with gTTS (better quality than pyttsx3)
            print(f"   🔊 Generating base audio with gTTS...")
            tts = gTTS(text=text, lang="en", tld=tld, slow=False)

            # Save to temporary MP3 file
            temp_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(temp_mp3.name)
            temp_mp3.close()

            # Convert MP3 to WAV and process
            print(f"   🎵 Applying voice matching...")
            audio = AudioSegment.from_mp3(temp_mp3.name)

            # Export to temp WAV for processing
            temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            audio.export(temp_wav.name, format="wav")
            temp_wav.close()

            # Load with librosa for advanced processing
            y, sr = librosa.load(temp_wav.name, sr=22050)

            # Calculate pitch shift needed
            current_pitch = self._estimate_pitch(temp_wav.name)

            if current_pitch > 0 and target_pitch > 0:
                import math

                # Calculate semitones difference (more aggressive)
                semitones = 12.0 * math.log2(target_pitch / current_pitch)
                # Allow wider range for better matching
                semitones = max(-12.0, min(12.0, semitones))

                print(f"   📊 Applying pitch shift: {semitones:.1f} semitones")
                print(
                    f"      Current: {current_pitch:.0f} Hz → Target: {target_pitch:.0f} Hz"
                )

                # Apply pitch shift
                if abs(semitones) > 0.3:
                    y = librosa.effects.pitch_shift(y, sr=sr, n_steps=semitones)

                # Time stretch to match speech rate
                if speech_rate > 0.5 and speech_rate < 2.0:
                    stretch_factor = 1.0 / speech_rate
                    stretch_factor = max(0.8, min(1.3, stretch_factor))
                    if abs(stretch_factor - 1.0) > 0.05:
                        print(f"   ⏱️  Applying time stretch: {stretch_factor:.2f}x")
                        y = librosa.effects.time_stretch(y, rate=stretch_factor)

                # Match energy/volume more aggressively
                current_energy = np.sqrt(np.mean(y**2))
                if current_energy > 0 and energy > 0:
                    scale_factor = energy / current_energy
                    scale_factor = max(0.5, min(5.0, scale_factor))
                    y = y * scale_factor
                    print(f"   🔊 Volume adjusted: {scale_factor:.2f}x")

                # Write final audio
                sf.write(output_path, y, sr)
                print(f"   ✅ Custom voice generated and matched!")
            else:
                # Fallback: just save the gTTS output
                audio.export(output_path, format="wav")
                print(f"   ⚠️  Using gTTS output without pitch matching")

            # Clean up temp files
            import os

            try:
                os.remove(temp_mp3.name)
                os.remove(temp_wav.name)
            except:
                pass

            return output_path

        except Exception as e:
            print(f"   ❌ Voice matching failed: {e}")
            print(f"   Falling back to Indian voice...")
            # Fallback to Indian voice
            try:
                return self.synthesize_with_indian_voice(
                    text, "indian_male", language, output_path
                )
            except:
                # Ultimate fallback: write a short tone
                import soundfile as sf

                sr = 22050
                t = np.linspace(0, 0.5, int(sr * 0.5), endpoint=False)
                tone = 0.2 * np.sin(2 * np.pi * 440 * t)
                sf.write(output_path, tone.astype(np.float32), sr)
                print(f"   ⚠️  Fallback tone generated")
                return output_path

    def synthesize_with_custom_voice(
        self,
        text: str,
        voice_profile: Dict,
        language: str = "en",
        output_path: str = None,
    ) -> str:
        """
        Main entry point for custom voice synthesis using FREE Coqui XTTS.
        ₹0 cost forever - completely self-hosted.
        """
        print(f"🎙️ Custom voice synthesis: '{text[:50]}...'")
        print(f"💚 Using FREE Coqui XTTS (₹0 forever)")
        
        # Use Coqui XTTS voice cloning (FREE - Primary method)
        if self.coqui_cloner and voice_profile.get("audio_reference"):
            try:
                print("🚀 Using Coqui XTTS voice cloning (FREE)...")
                result = self.coqui_cloner.clone_voice(
                    text=text,
                    reference_audio_path=voice_profile["audio_reference"],
                    output_path=output_path,
                    language=language
                )
                if result and os.path.exists(result):
                    print("✅ Coqui XTTS voice cloning successful!")
                    print("💰 Cost: ₹0 (self-hosted)")
                    return result
                else:
                    print("⚠️  Coqui XTTS returned invalid result")
            except Exception as e:
                print(f"❌ Coqui XTTS cloning failed: {e}")
                print("🔄 Falling back to basic voice cloning...")
        
        # Fallback to basic voice cloning if Coqui XTTS not available
        print("⚠️  Coqui XTTS not available, using basic fallback...")
        return self.synthesize_with_true_voice_cloning(
            text, voice_profile, language, output_path
        )

    def synthesize_with_indian_voice(
        self, text: str, voice_type: str, language: str = "en", output_path: str = None
    ) -> str:
        """
        Generate speech with Indian English accent using LOCAL TTS (no API costs).
        Supports indian_male and indian_female voice types.
        """
        print(f"🇮🇳 Synthesizing with LOCAL Indian accent: '{text[:50]}...'")
        print(f"   💰 Using LOCAL TTS - No Google API costs!")
        
        try:
            # Import our NATURAL Indian TTS module (non-robotic)
            from natural_indian_tts import generate_natural_indian_voice
            
            # Generate using natural TTS (less robotic)
            result_path = generate_natural_indian_voice(text, voice_type, output_path)
            
            print(f"   ✅ Local Indian voice generated successfully!")
            print(f"   🎉 Zero API costs - completely offline!")
            return result_path

        except ImportError as e:
            print(f"   ❌ Local Indian TTS module not found: {e}")
            print(f"   🔄 Falling back to basic pyttsx3...")
            return self._fallback_to_basic_tts(text, voice_type, output_path)
        except Exception as e:
            print(f"   ⚠️  Local Indian TTS failed: {e}")
            print(f"   🔄 Falling back to basic TTS...")
            return self._fallback_to_basic_tts(text, voice_type, output_path)
    
    def _fallback_to_basic_tts(self, text: str, voice_type: str, output_path: str) -> str:
        """Fallback TTS using pyttsx3 with basic Indian accent simulation"""
        try:
            import pyttsx3
            import soundfile as sf
            
            print(f"   🔧 Using pyttsx3 with Indian accent simulation...")
            
            engine = pyttsx3.init()
            
            # Select appropriate voice
            voices = engine.getProperty('voices')
            selected_voice = None
            
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
            
            # Adjust rate for Indian speaking pattern
            rate = engine.getProperty('rate')
            if "female" in voice_type:
                engine.setProperty('rate', int(rate * 0.95))  # Slightly slower for female
            else:
                engine.setProperty('rate', int(rate * 0.90))  # Slower for male
            
            # Create temporary file
            import tempfile
            temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            temp_wav.close()
            
            # Generate speech
            engine.save_to_file(text, temp_wav.name)
            engine.runAndWait()
            
            # Apply basic pitch adjustment to simulate Indian accent
            y, sr = librosa.load(temp_wav.name, sr=22050)
            
            if "female" in voice_type:
                # Female: slightly higher pitch
                y = librosa.effects.pitch_shift(y, sr=sr, n_steps=1.5)
            else:
                # Male: slightly lower pitch
                y = librosa.effects.pitch_shift(y, sr=sr, n_steps=-2.0)
            
            # Save final audio
            sf.write(output_path, y, sr)
            
            # Clean up
            import os
            os.remove(temp_wav.name)
            
            print(f"   ✅ Basic Indian accent simulation completed!")
            return output_path
            
        except Exception as e:
            print(f"   ❌ Fallback TTS also failed: {e}")
            # Ultimate fallback: create a tone
            import soundfile as sf

            sr = 22050
            t = np.linspace(0, 0.5, int(sr * 0.5), endpoint=False)
            tone = 0.2 * np.sin(2 * np.pi * 440 * t)
            sf.write(output_path, tone.astype(np.float32), sr)
            print(f"   ⚠️  Fallback tone generated")
            return output_path

    def synthesize_with_default_voice(
        self, text: str, voice_type: str, language: str = "en", output_path: str = None
    ) -> str:
        """
        Generate speech with default voice using pyttsx3 on Windows (offline).
        Routes to Indian voice synthesis if Indian accent is selected.
        Falls back to a short audible tone if synthesis fails.
        """
        # Check if Indian voice is requested
        if voice_type in ["indian_male", "indian_female"]:
            return self.synthesize_with_indian_voice(
                text, voice_type, language, output_path
            )

        print(f"🔊 Synthesizing: '{text[:50]}...' with {voice_type} voice")
        try:
            import pyttsx3

            engine = pyttsx3.init()

            # Try to select a male/female voice if requested
            requested = voice_type.lower()
            selected_voice_id = None

            # Map AI voice types to base genders for system voice selection
            voice_gender_map = {
                "male": "male",
                "female": "female",
                "ai_neutral": "neutral",  # Will pick first available or male as fallback
                "ai_energetic": "female",  # More energetic = typically female voice
                "custom": "male",  # Default for custom
            }

            target_gender = voice_gender_map.get(requested, "male")

            try:
                voices = engine.getProperty("voices")
                male_voice = None
                female_voice = None

                # Identify available voices
                for v in voices:
                    name = (getattr(v, "name", "") or "").lower()
                    vid = (getattr(v, "id", "") or "").lower()
                    tags = " ".join([name, vid])

                    if (
                        "female" in tags
                        or "zira" in tags
                        or "susan" in tags
                        or "eva" in tags
                    ):
                        female_voice = v.id
                    elif "male" in tags or "david" in tags or "george" in tags:
                        male_voice = v.id

                # Select voice based on target gender
                if target_gender == "female" and female_voice:
                    selected_voice_id = female_voice
                elif target_gender == "male" and male_voice:
                    selected_voice_id = male_voice
                elif target_gender == "neutral":
                    # For neutral, prefer female voice if available, otherwise male
                    selected_voice_id = female_voice if female_voice else male_voice
                else:
                    # Fallback
                    selected_voice_id = male_voice if male_voice else female_voice

            except Exception as e:
                print(f"Error selecting voice: {e}")
                pass

            # Apply base voice selection if found
            if selected_voice_id:
                engine.setProperty("voice", selected_voice_id)

            # Base speaking rate
            try:
                rate = engine.getProperty("rate")
                if isinstance(rate, int):
                    base_rate = max(140, min(190, rate))
                else:
                    base_rate = 170
            except Exception:
                base_rate = 170

            # Per-voice adjustments (pyttsx3 level)
            requested = voice_type.lower()
            if requested == "ai_energetic":
                engine.setProperty("rate", int(base_rate * 1.15))
            elif requested == "ai_neutral":
                engine.setProperty("rate", int(base_rate))
            elif requested == "female":
                engine.setProperty("rate", int(base_rate * 1.05))
            else:  # male/default
                engine.setProperty("rate", int(base_rate))

            # Synthesize to file (WAV)
            engine.save_to_file(text, output_path)
            engine.runAndWait()

            # Post-process for clearer differentiation if engine voices are limited
            try:
                if requested == "female":
                    # If a reference sample exists, try to match its pitch
                    sample_path = os.path.join(os.path.dirname(__file__), "sample.wav")
                    semitones = 3.0
                    stretch = 1.05
                    try:
                        if os.path.exists(sample_path):
                            target_pitch = self._estimate_pitch(sample_path)
                            current_pitch = self._estimate_pitch(output_path)
                            if target_pitch > 0 and current_pitch > 0:
                                import math

                                semitones = 12.0 * math.log2(
                                    target_pitch / current_pitch
                                )
                                # Clamp to reasonable range
                                semitones = max(-6.0, min(6.0, semitones))
                                stretch = 1.05
                    except Exception:
                        pass
                    self._postprocess_audio(
                        output_path, semitones=semitones, time_stretch=stretch
                    )
                elif requested == "male":
                    # Slightly lower pitch
                    self._postprocess_audio(
                        output_path, semitones=-1.5, time_stretch=1.0
                    )
                elif requested == "ai_energetic":
                    # Higher pitch and faster
                    self._postprocess_audio(
                        output_path, semitones=2.0, time_stretch=1.12
                    )
                elif requested == "ai_neutral":
                    # Neutral minor normalization (no change)
                    pass
            except Exception:
                # If post-processing fails, keep original
                pass

            return output_path
        except Exception as e:
            # Fallback: write a short tone so file is not silent
            import soundfile as sf

            sr = 22050
            t = np.linspace(0, 0.5, int(sr * 0.5), endpoint=False)
            tone = 0.2 * np.sin(2 * np.pi * 440 * t)
            sf.write(output_path, tone.astype(np.float32), sr)
            return output_path

    def get_available_voices(self) -> Dict:
        """Get all available voice options"""
        return {
            "default_voices": self.default_voices,
            "custom_voice_supported": True,
            "languages": self.supported_languages,
        }

    def get_supported_languages(self) -> list:
        """Return list of supported languages"""
        return self.supported_languages

    def concatenate_audio(
        self, audio_files: list, output_path: str, pause_duration: float = 0.5
    ) -> str:
        """
        Concatenate multiple audio files with pauses
        """
        try:
            import soundfile as sf

            combined_audio = []
            sample_rate = None

            for audio_file in audio_files:
                audio, sr = librosa.load(audio_file, sr=None)

                if sample_rate is None:
                    sample_rate = sr
                elif sr != sample_rate:
                    audio = librosa.resample(audio, orig_sr=sr, target_sr=sample_rate)

                combined_audio.append(audio)

                # Add pause
                pause_samples = int(pause_duration * sample_rate)
                combined_audio.append(np.zeros(pause_samples))

            # Concatenate all
            final_audio = np.concatenate(combined_audio)

            # Save
            sf.write(output_path, final_audio, sample_rate)

            return output_path

        except Exception as e:
            raise Exception(f"Error concatenating audio: {str(e)}")

    def _postprocess_audio(
        self, file_path: str, semitones: float = 0.0, time_stretch: float = 1.0
    ) -> None:
        """Apply simple pitch/time modifications to differentiate voices."""
        import soundfile as sf

        # Load
        y, sr = librosa.load(file_path, sr=None)
        if semitones != 0.0:
            try:
                y = librosa.effects.pitch_shift(y, sr=sr, n_steps=semitones)
            except Exception:
                pass
        if time_stretch and abs(time_stretch - 1.0) > 1e-3:
            try:
                y = librosa.effects.time_stretch(y, rate=time_stretch)
            except Exception:
                pass
        # Write back
        sf.write(file_path, y, sr)

    def _estimate_pitch(self, file_path: str) -> float:
        """Estimate fundamental frequency using librosa.yin median (in Hz)."""
        try:
            y, sr = librosa.load(file_path, sr=22050)
            f0 = librosa.yin(y, fmin=50, fmax=500)
            f0 = f0[np.isfinite(f0)]
            if f0.size == 0:
                return 0.0
            return float(np.median(f0))
        except Exception:
            return 0.0
