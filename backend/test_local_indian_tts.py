"""
Test script for Local Indian TTS
Verifies that the local Indian TTS system works without Google API
"""

import os
import sys
from local_indian_tts import generate_local_indian_voice

def test_indian_voices():
    """Test both Indian male and female voices"""
    
    # Test text
    test_text = "Hello! This is a test of the local Indian text-to-speech system. It generates high-quality Indian accented speech without using any external APIs."
    
    # Test output directory
    test_dir = "test_local_tts_output"
    os.makedirs(test_dir, exist_ok=True)
    
    print("🇮🇳 Testing Local Indian TTS System")
    print("=" * 50)
    
    # Test Indian Male
    print("\n1. Testing Indian Male Voice...")
    male_output = os.path.join(test_dir, "test_indian_male.wav")
    try:
        result = generate_local_indian_voice(test_text, "indian_male", male_output)
        if os.path.exists(result):
            size = os.path.getsize(result)
            print(f"   ✅ Success! Generated: {result} ({size} bytes)")
        else:
            print(f"   ❌ Failed - File not created")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test Indian Female
    print("\n2. Testing Indian Female Voice...")
    female_output = os.path.join(test_dir, "test_indian_female.wav")
    try:
        result = generate_local_indian_voice(test_text, "indian_female", female_output)
        if os.path.exists(result):
            size = os.path.getsize(result)
            print(f"   ✅ Success! Generated: {result} ({size} bytes)")
        else:
            print(f"   ❌ Failed - File not created")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Test Complete!")
    print(f"📁 Audio files saved in: {os.path.abspath(test_dir)}")
    print("💰 No API costs incurred!")
    
    # Check if espeak is available
    print("\n🔍 System Check:")
    try:
        import subprocess
        result = subprocess.run(['espeak', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("   ✅ espeak is available - Using high-quality synthesis")
        else:
            print("   ⚠️  espeak not found - Using pyttsx3 fallback")
    except:
        print("   ⚠️  espeak not found - Using pyttsx3 fallback")
        print("   💡 Install espeak for better Indian accent: https://espeak.sourceforge.net/")

if __name__ == "__main__":
    test_indian_voices()
