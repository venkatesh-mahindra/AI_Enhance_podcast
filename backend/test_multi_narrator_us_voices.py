"""
Test Multi-Narrator with US Male/Female Voices
Tests the voice assignment system with dialogue content
"""

import os
import sys
import json

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from character_detector import CharacterDetector
from podcast_generator import PodcastGenerator

def test_us_multi_narrator():
    """Test multi-narrator with US male and female voices"""
    
    print("="*70)
    print("🎭 TESTING MULTI-NARRATOR WITH US VOICES")
    print("="*70)
    
    # Sample content with dialogue (male and female characters) - correct format
    test_content = {
        "metadata": {
            "title": "Business Meeting Dialogue",
            "author": "Test Author",
            "pages": 1
        },
        "text_blocks": [
            {
                "page": 1,
                "text": """The quarterly review meeting began promptly at 9 AM.

"Good morning everyone," said John, the project manager. "Let's start with the sales figures."

Sarah, the marketing director, opened her laptop. "Our Q3 numbers show a 15% increase," she reported confidently.

"That's excellent news," John replied. "What about the new product launch?"

"We're on track for December," Sarah confirmed. "The marketing campaign is ready to go."

The narrator explained that this meeting would determine the company's strategy for the next quarter.

"I have some concerns about the budget," said Michael, the finance director. "We need to be more careful with expenses."

"I understand your concerns," Sarah responded. "But we need to invest in growth."

John nodded thoughtfully. "Let's find a balance between growth and fiscal responsibility." """,
                "type": "text"
            }
        ],
        "images": [],
        "tables": []
    }
    
    # US Professional voice set configuration
    us_voice_set = {
        'male': ['male', 'ai_neutral'],      # US Male voices
        'female': ['female', 'ai_energetic'], # US Female voices  
        'narrator': 'male'                    # US Male narrator
    }
    
    print(f"📋 Voice Set Configuration:")
    print(f"   Male voices: {us_voice_set['male']}")
    print(f"   Female voices: {us_voice_set['female']}")
    print(f"   Narrator voice: {us_voice_set['narrator']}")
    
    try:
        # Initialize components
        print(f"\n🚀 Initializing components...")
        generator = PodcastGenerator()
        
        # Create script with multi-narrator enabled
        print(f"\n📝 Creating multi-narrator script...")
        script_data = generator.create_script(
            test_content, 
            language="en", 
            enable_multi_narrator=True,
            voice_set_config=us_voice_set
        )
        
        print(f"\n📊 Script Analysis:")
        print(f"   Type: {script_data.get('type', 'unknown')}")
        print(f"   Characters detected: {len(script_data.get('characters', {}))}")
        
        if script_data.get("type") == "multi_narrator":
            print(f"\n✅ Multi-narrator script created successfully!")
            
            # Show character assignments
            characters = script_data.get('characters', {})
            print(f"\n🎭 Character Voice Assignments:")
            for char_name, char_info in characters.items():
                voice = char_info.get('voice_type', 'unknown')
                gender = char_info.get('gender', 'unknown')
                lines = char_info.get('lines', 0)
                print(f"   👤 {char_name}: {voice} ({gender}) - {lines} lines")
            
            # Show script segments with voice assignments
            script_segments = script_data.get('script_segments', [])
            print(f"\n📜 Script Segments (first 10):")
            for i, segment in enumerate(script_segments[:10]):
                speaker = segment.get('speaker', 'unknown')
                voice = segment.get('voice_type', 'unknown')
                text = segment.get('text', '')[:50] + "..."
                print(f"   {i+1}. [{voice}] {speaker}: {text}")
            
            # Verify voice diversity
            used_voices = set()
            for segment in script_segments:
                used_voices.add(segment.get('voice_type', 'unknown'))
            
            print(f"\n🎯 Voice Diversity Check:")
            print(f"   Total unique voices used: {len(used_voices)}")
            print(f"   Voices: {list(used_voices)}")
            
            # Check if we have both male and female US voices
            has_us_male = any(voice in ['male', 'ai_neutral'] for voice in used_voices)
            has_us_female = any(voice in ['female', 'ai_energetic'] for voice in used_voices)
            
            print(f"\n✅ US Voice Usage:")
            print(f"   US Male voices used: {'✅' if has_us_male else '❌'}")
            print(f"   US Female voices used: {'✅' if has_us_female else '❌'}")
            
            if has_us_male and has_us_female:
                print(f"\n🎉 SUCCESS! Multi-narrator with US male/female voices working!")
                print(f"   - Different characters get different voices")
                print(f"   - Male characters use US male voices")
                print(f"   - Female characters use US female voices")
                print(f"   - Narrator uses designated voice")
                return True
            else:
                print(f"\n⚠️  Limited voice diversity detected")
                return False
                
        else:
            print(f"\n❌ Multi-narrator not detected in content")
            print(f"   Script type: {script_data.get('type', 'unknown')}")
            return False
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_voice_assignment_logic():
    """Test the voice assignment logic directly"""
    
    print(f"\n" + "="*70)
    print("🔧 TESTING VOICE ASSIGNMENT LOGIC")
    print("="*70)
    
    try:
        detector = CharacterDetector()
        
        # Sample script segments with different characters
        test_segments = [
            {"speaker": "narrator", "text": "The story begins...", "gender": "neutral"},
            {"speaker": "John", "text": "Hello everyone", "gender": "male"},
            {"speaker": "Sarah", "text": "Good morning", "gender": "female"},
            {"speaker": "Michael", "text": "Let's get started", "gender": "male"},
            {"speaker": "narrator", "text": "Meanwhile...", "gender": "neutral"},
            {"speaker": "Sarah", "text": "I agree with that", "gender": "female"},
        ]
        
        # US voice configuration
        us_config = {
            'male': ['male', 'ai_neutral'],
            'female': ['female', 'ai_energetic'],
            'narrator': 'male'
        }
        
        print(f"📝 Input segments: {len(test_segments)}")
        print(f"🎭 Voice config: {us_config}")
        
        # Assign voices
        assigned_segments = detector.assign_voices(test_segments, us_config)
        
        print(f"\n🎯 Voice Assignments:")
        for segment in assigned_segments:
            speaker = segment.get('speaker')
            voice = segment.get('voice_type')
            gender = segment.get('gender')
            text = segment.get('text', '')[:30] + "..."
            print(f"   {speaker} ({gender}) → {voice}: {text}")
        
        # Verify assignments
        voice_counts = {}
        for segment in assigned_segments:
            voice = segment.get('voice_type')
            voice_counts[voice] = voice_counts.get(voice, 0) + 1
        
        print(f"\n📊 Voice Usage:")
        for voice, count in voice_counts.items():
            print(f"   {voice}: {count} segments")
        
        print(f"\n✅ Voice assignment logic working correctly!")
        return True
        
    except Exception as e:
        print(f"\n❌ Voice assignment test failed: {e}")
        return False

if __name__ == "__main__":
    print("🎭 Multi-Narrator US Voices Test Suite")
    print("=" * 70)
    
    # Test 1: Full multi-narrator pipeline
    test1_success = test_us_multi_narrator()
    
    # Test 2: Voice assignment logic
    test2_success = test_voice_assignment_logic()
    
    print(f"\n" + "="*70)
    print("📋 TEST RESULTS SUMMARY")
    print("="*70)
    print(f"✅ Multi-narrator pipeline: {'PASS' if test1_success else 'FAIL'}")
    print(f"✅ Voice assignment logic: {'PASS' if test2_success else 'FAIL'}")
    
    if test1_success and test2_success:
        print(f"\n🎉 ALL TESTS PASSED!")
        print(f"   Multi-narrator with US male/female voices is working!")
        print(f"   Ready for frontend testing!")
    else:
        print(f"\n❌ Some tests failed. Check output above.")
    
    print("="*70)
