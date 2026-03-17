"""
Test dialogue detection with clear dialogue format
"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from character_detector import CharacterDetector

def test_dialogue_detection():
    """Test if character detector can find dialogue in clear format"""
    
    print("="*60)
    print("🎭 TESTING DIALOGUE DETECTION")
    print("="*60)
    
    # Read test dialogue
    with open("test_dialogue_sample.txt", "r", encoding="utf-8") as f:
        test_text = f.read()
    
    print(f"📝 Test text:")
    print(f"{test_text[:200]}...")
    
    try:
        detector = CharacterDetector()
        
        # Detect characters
        print(f"\n🔍 Detecting characters...")
        characters = detector.detect_characters(test_text)
        
        print(f"\n👥 Characters found: {len(characters)}")
        for char in characters:
            name = char.get('name', 'Unknown')
            gender = char.get('gender', 'unknown')
            mentions = char.get('mentions', 0)
            dialogues = len(char.get('dialogues', []))
            print(f"   👤 {name} ({gender}) - {mentions} mentions, {dialogues} dialogues")
        
        # Extract dialogues
        print(f"\n💬 Extracting dialogues...")
        dialogues = detector.extract_dialogues(test_text, characters)
        
        print(f"\n📜 Dialogues found: {len(dialogues)}")
        for i, dialogue in enumerate(dialogues):
            speaker = dialogue.get('speaker', 'Unknown')
            gender = dialogue.get('gender', 'unknown')
            text = dialogue.get('text', '')[:50] + "..."
            print(f"   {i+1}. {speaker} ({gender}): {text}")
        
        # Test multi-voice script creation
        print(f"\n🎬 Creating multi-voice script...")
        script_segments = detector.create_multi_voice_script(test_text)
        
        print(f"\n📋 Script segments: {len(script_segments)}")
        for i, segment in enumerate(script_segments[:10]):  # Show first 10
            seg_type = segment.get('type', 'unknown')
            speaker = segment.get('speaker', 'narrator')
            gender = segment.get('gender', 'neutral')
            text = segment.get('text', '')[:40] + "..."
            print(f"   {i+1}. [{seg_type}] {speaker} ({gender}): {text}")
        
        # Check if we have dialogue segments
        dialogue_segments = [s for s in script_segments if s.get('type') == 'dialogue']
        narrative_segments = [s for s in script_segments if s.get('type') == 'narrative']
        
        print(f"\n📊 Segment Analysis:")
        print(f"   Dialogue segments: {len(dialogue_segments)}")
        print(f"   Narrative segments: {len(narrative_segments)}")
        
        if len(dialogue_segments) > 0:
            print(f"\n✅ SUCCESS! Dialogue detection working!")
            print(f"   - Found {len(characters)} characters")
            print(f"   - Extracted {len(dialogues)} dialogues")
            print(f"   - Created {len(dialogue_segments)} dialogue segments")
            return True
        else:
            print(f"\n❌ No dialogue segments found")
            return False
            
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_dialogue_detection()
    
    if success:
        print(f"\n🎉 Dialogue detection is working!")
        print(f"   Ready for multi-narrator testing!")
    else:
        print(f"\n⚠️  Dialogue detection needs improvement")
