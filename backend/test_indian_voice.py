#!/usr/bin/env python
"""Test Indian accent voice synthesis"""

import os

from voice_cloner import VoiceCloner

# Create test directory
os.makedirs("test_output", exist_ok=True)

voice_cloner = VoiceCloner()

test_text = "Hello, this is a test of the Indian English accent voice synthesis system. Welcome to our podcast!"

print("Testing Indian Accent Voices...")
print("=" * 60)

# Test Indian Male
print("\nTesting Indian Male voice...")
output_path = "test_output/test_indian_male.wav"
try:
    result = voice_cloner.synthesize_with_indian_voice(
        text=test_text, voice_type="indian_male", language="en", output_path=output_path
    )
    print(f"✓ Generated: {output_path}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test Indian Female
print("\nTesting Indian Female voice...")
output_path = "test_output/test_indian_female.wav"
try:
    result = voice_cloner.synthesize_with_indian_voice(
        text=test_text,
        voice_type="indian_female",
        language="en",
        output_path=output_path,
    )
    print(f"✓ Generated: {output_path}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 60)
print("Test complete! Check test_output/ folder for audio files.")
print("Listen to them to verify the Indian accent is present!")
