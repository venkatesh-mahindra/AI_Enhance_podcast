"""
URGENT DEBUG: Check why custom voice is still robotic
"""

from voice_cloner import VoiceCloner
import tempfile
import librosa
import numpy as np

def debug_voice_processing():
    print("🚨 URGENT VOICE DEBUG")
    print("=" * 60)
    
    try:
        # Initialize voice cloner
        vc = VoiceCloner()
        
        # Check enhanced cloner availability
        has_enhanced = hasattr(vc, 'enhanced_cloner') and vc.enhanced_cloner is not None
        print(f"📊 Enhanced cloner available: {has_enhanced}")
        
        # Create a test female voice profile (simulating your voice)
        test_female_profile = {
            "duration": 20.0,
            "pitch": {"mean": 200, "std": 15},  # Typical female pitch
            "pitch_mean": 200,  # Female range
            "energy": 0.15,
            "is_female": True,  # This should trigger female voice
            "quality": "good",
            "enhanced": True,  # This should trigger enhanced processing
            "sample_rate": 22050
        }
        
        print(f"🔍 Test profile - is_female: {test_female_profile['is_female']}")
        print(f"🔍 Test profile - enhanced: {test_female_profile['enhanced']}")
        print(f"🔍 Test profile - pitch: {test_female_profile['pitch_mean']} Hz")
        
        # Test voice synthesis
        test_text = "Hello, this is a test of the enhanced female voice cloning system."
        
        print(f"\n🎙️ Testing synthesis with female profile...")
        
        # Create temp output file
        temp_output = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_output.close()
        
        try:
            # This should trigger enhanced female voice synthesis
            result_path = vc.synthesize_with_custom_voice(
                test_text, 
                test_female_profile, 
                "en", 
                temp_output.name
            )
            
            print(f"✅ Synthesis completed: {result_path}")
            
            # Check what actually happened in the logs above
            print("\n🔍 CHECK BACKEND CONSOLE LOGS ABOVE FOR:")
            print("   - '🔬 Using enhanced voice analysis...'")
            print("   - '🌟 Using enhanced custom voice synthesis...'") 
            print("   - '🚨 GENDER DEBUG: is_female=True'")
            print("   - '🎭 Selected FEMALE voice'")
            
        except Exception as e:
            print(f"❌ Synthesis failed: {e}")
        
        # Check Hz recording recommendations
        print(f"\n🎙️ VOICE RECORDING RECOMMENDATIONS:")
        print(f"   📊 Female voice Hz range: 165-300 Hz (fundamental frequency)")
        print(f"   🎤 Recording sample rate: 44,100 Hz (CD quality)")
        print(f"   ⏱️ Duration: 15-30 seconds")
        print(f"   🔊 Quality: Clear, no background noise")
        print(f"   📝 Content: Natural speech with emotion variation")
        
        # Pitch analysis recommendations
        print(f"\n🔬 PITCH ANALYSIS FOR YOUR VOICE:")
        print(f"   🎯 Target: Record at your natural speaking pitch")
        print(f"   📈 Detection threshold: >= 165 Hz = Female")
        print(f"   🎵 Female range: 165-300 Hz typically") 
        print(f"   🎶 Your pitch should be detected automatically")
        
        print(f"\n🚨 IF STILL ROBOTIC, CHECK:")
        print(f"   1. Backend logs show 'Enhanced voice synthesis'")
        print(f"   2. Voice upload shows 'enhanced: true' in analysis")
        print(f"   3. Gender detection shows 'Female' correctly")
        print(f"   4. No fallback to basic Indian TTS")
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")

if __name__ == "__main__":
    debug_voice_processing()
