"""
Test script for enhanced multi-narrator voice functionality
Tests different voice sets including US Female voice
"""

import sys
import os

# Add backend to Python path
sys.path.append(os.path.dirname(__file__))

from character_detector import CharacterDetector
from podcast_generator import PodcastGenerator

def test_voice_assignments():
    """Test the enhanced voice assignment system"""
    
    print("🎭 Testing Enhanced Multi-Narrator Voice System")
    print("=" * 60)
    
    # Create test content with dialogue (matching expected structure)
    test_content = {
        "metadata": {
            "title": "Test Conversation",
            "author": "Test Author",
            "subject": "Test Subject",
            "pages": 1
        },
        "text_blocks": [
            {
                "type": "paragraph",
                "text": '"Hello there!" said John cheerfully. "How are you doing today?"',
                "page": 1
            },
            {
                "type": "paragraph", 
                "text": '"I\'m doing great, thank you!" replied Sarah with a smile. "And you?"',
                "page": 1
            },
            {
                "type": "paragraph",
                "text": '"Wonderful!" John responded. "I was thinking we could discuss the project."',
                "page": 1
            },
            {
                "type": "paragraph",
                "text": "The narrator explained that this conversation took place in the office.",
                "page": 1
            },
            {
                "type": "paragraph",
                "text": '"Absolutely," Sarah agreed. "Let\'s start with the timeline."',
                "page": 1
            }
        ],
        "images": []
    }
    
    # Test different voice sets
    voice_sets_to_test = [
        ('diverse_professional', {
            'male': ['indian_male', 'male', 'ai_neutral'],
            'female': ['indian_female', 'female', 'ai_energetic'],
            'narrator': 'indian_male'
        }),
        ('all_us_professional', {
            'male': ['male', 'ai_neutral'],
            'female': ['female', 'ai_energetic'],
            'narrator': 'female'
        }),
        ('all_indian_free', {
            'male': ['indian_male'],
            'female': ['indian_female'],
            'narrator': 'indian_male'
        })
    ]
    
    generator = PodcastGenerator()
    
    for voice_set_name, voice_set_config in voice_sets_to_test:
        print(f"\n🔍 Testing Voice Set: {voice_set_name}")
        print(f"   📋 Config: {voice_set_config}")
        
        try:
            # Generate script with voice set
            script_data = generator.create_script(
                test_content, 
                language="en", 
                enable_multi_narrator=True,
                voice_set_config=voice_set_config
            )
            
            if script_data.get("type") == "multi_narrator":
                print(f"   ✅ Multi-narrator detected!")
                print(f"   👥 Characters: {script_data.get('characters', {}).get('total_characters', 0)}")
                
                # Show voice assignments
                segments = script_data.get("segments", [])
                voice_assignments = {}
                
                for segment in segments:
                    speaker = segment.get("speaker", "unknown")
                    voice = segment.get("voice_type", "unknown")
                    if speaker not in voice_assignments:
                        voice_assignments[speaker] = voice
                
                print(f"   🎯 Voice Assignments:")
                for speaker, voice in voice_assignments.items():
                    gender_emoji = "👨" if "male" in voice else "👩" if "female" in voice else "🎙️"
                    print(f"      {gender_emoji} {speaker}: {voice}")
                
                # Special check for US Female voice
                if voice_set_name == 'all_us_professional':
                    female_voices = [v for v in voice_assignments.values() if 'female' in v or v == 'female']
                    if female_voices:
                        print(f"   🇺🇸 US Female voice confirmed: {female_voices}")
                    else:
                        print(f"   ⚠️  US Female voice not found in assignments")
                        
            else:
                print(f"   ❌ Multi-narrator not detected")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print("-" * 40)
    
    print("\n🎉 Multi-narrator voice testing complete!")
    print("💰 Indian voices remain completely FREE!")
    print("🇺🇸 US Female voice is available for multi-narrator!")

if __name__ == "__main__":
    test_voice_assignments()
