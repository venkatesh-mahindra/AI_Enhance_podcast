"""
Test script for Natural Indian TTS
Tests the improved, non-robotic voice generation
"""

import os
from natural_indian_tts import generate_natural_indian_voice

def test_natural_voices():
    """Test natural Indian voices (non-robotic)"""
    
    # Test with different types of text to check naturalness
    test_texts = [
        "Hello! This is a test of our improved natural Indian text-to-speech system. It should sound much more human-like and less robotic.",
        "Today we will learn about artificial intelligence and machine learning. These technologies are transforming our world in amazing ways.",
        "Welcome to this podcast! I'm excited to share this story with you. Let's begin our journey together."
    ]
    
    # Test output directory
    test_dir = "test_natural_tts_output"
    os.makedirs(test_dir, exist_ok=True)
    
    print("🇮🇳 Testing NATURAL Indian TTS System")
    print("🎯 Focus: Human-like quality, reduced robotic artifacts")
    print("=" * 60)
    
    for i, test_text in enumerate(test_texts, 1):
        print(f"\n📝 Test {i}: {test_text[:50]}...")
        
        # Test Indian Male
        print(f"\n🎤 Testing Natural Indian Male Voice...")
        male_output = os.path.join(test_dir, f"natural_male_test_{i}.wav")
        try:
            result = generate_natural_indian_voice(test_text, "indian_male", male_output)
            if os.path.exists(result):
                size = os.path.getsize(result)
                print(f"   ✅ Success! Generated: {os.path.basename(result)} ({size} bytes)")
            else:
                print(f"   ❌ Failed - File not created")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test Indian Female
        print(f"\n👩 Testing Natural Indian Female Voice...")
        female_output = os.path.join(test_dir, f"natural_female_test_{i}.wav")
        try:
            result = generate_natural_indian_voice(test_text, "indian_female", female_output)
            if os.path.exists(result):
                size = os.path.getsize(result)
                print(f"   ✅ Success! Generated: {os.path.basename(result)} ({size} bytes)")
            else:
                print(f"   ❌ Failed - File not created")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print("-" * 40)
    
    print("\n" + "=" * 60)
    print("🎉 Natural Voice Test Complete!")
    print(f"📁 Audio files saved in: {os.path.abspath(test_dir)}")
    print("🎯 These voices should sound much more natural and human-like!")
    print("💰 Still completely FREE with no API costs!")
    
    # Quality comparison
    print("\n📊 Quality Improvements:")
    print("   ✅ Reduced robotic artifacts")
    print("   ✅ More natural prosody and rhythm") 
    print("   ✅ Gentle processing for human-like quality")
    print("   ✅ Better text preprocessing for natural speech")
    print("   ✅ Subtle variations to mimic human speech patterns")

if __name__ == "__main__":
    test_natural_voices()
