"""
Test Coqui XTTS with user's audio file
"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

def test_coqui_cloning():
    """Test Coqui XTTS voice cloning with user's audio"""
    
    print("="*70)
    print("🧪 TESTING COQUI XTTS VOICE CLONING")
    print("="*70)
    
    # User's audio file
    audio_file = r"C:\Users\ASUS\Downloads\wani_sir (online-audio-converter (mp3cut.net).mp3"
    
    # Test text
    test_text = "Hello, this is a test of voice cloning using Coqui XTTS. The system is completely free and runs locally without any API costs."
    
    print(f"\n📁 Audio file: {audio_file}")
    print(f"📝 Test text: {test_text[:60]}...")
    
    # Check if file exists
    if not os.path.exists(audio_file):
        print(f"\n❌ ERROR: Audio file not found!")
        print(f"   Path: {audio_file}")
        return False
    
    print(f"✅ Audio file found! Size: {os.path.getsize(audio_file) / 1024:.1f} KB")
    
    # Try to import and initialize Coqui XTTS
    try:
        print("\n🚀 Initializing Coqui XTTS...")
        from coqui_xtts_cloner import CoquiXTTSCloner
        
        cloner = CoquiXTTSCloner()
        print("✅ Coqui XTTS initialized successfully!")
        
    except ImportError as e:
        print(f"\n❌ Failed to import Coqui XTTS: {e}")
        print("   Install with: pip install TTS")
        return False
    except Exception as e:
        print(f"\n❌ Failed to initialize Coqui XTTS: {e}")
        return False
    
    # Test voice cloning
    try:
        print("\n🎙️ Starting voice cloning...")
        output_file = "test_wani_sir_cloned.wav"
        
        result = cloner.clone_voice(
            text=test_text,
            reference_audio_path=audio_file,
            output_path=output_file,
            language="en"
        )
        
        if result and os.path.exists(result):
            print("\n" + "="*70)
            print("🎉 SUCCESS! VOICE CLONING WORKS!")
            print("="*70)
            print(f"✅ Output file: {result}")
            print(f"📊 File size: {os.path.getsize(result) / 1024:.1f} KB")
            print(f"💰 Cost: ₹0 (completely free)")
            print("\n💡 Play the audio file to verify quality!")
            print("="*70)
            return True
        else:
            print("\n❌ Voice cloning failed - no output generated")
            return False
            
    except Exception as e:
        print(f"\n❌ Voice cloning failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n🎯 Coqui XTTS Voice Cloning Test")
    print("   Testing with: wani_sir audio file\n")
    
    success = test_coqui_cloning()
    
    if success:
        print("\n✅ TEST PASSED - Coqui XTTS is working!")
        sys.exit(0)
    else:
        print("\n❌ TEST FAILED - Check errors above")
        sys.exit(1)
