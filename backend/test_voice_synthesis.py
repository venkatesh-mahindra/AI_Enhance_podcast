#!/usr/bin/env python
"""Test voice synthesis with different voice types"""

import os

from voice_cloner import VoiceCloner

# Create test directory
os.makedirs("test_output", exist_ok=True)

voice_cloner = VoiceCloner()

test_text = "Hello, this is a test of the voice synthesis system."

voice_types = ["male", "female", "ai_neutral", "ai_energetic"]

print("Testing Voice Synthesis...")
print("=" * 60)

for voice_type in voice_types:
    print(f"\nTesting {voice_type}...")
    output_path = f"test_output/test_{voice_type}.wav"

    try:
        result = voice_cloner.synthesize_with_default_voice(
            text=test_text,
            voice_type=voice_type,
            language="en",
            output_path=output_path,
        )
        print(f"✓ Generated: {output_path}")
    except Exception as e:
        print(f"✗ Error: {e}")

print("\n" + "=" * 60)
print("Test complete! Check test_output/ folder for audio files.")
