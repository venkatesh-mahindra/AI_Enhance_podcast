#!/usr/bin/env python
"""Test if custom voice generation works end-to-end"""

import json
import os

from podcast_generator import PodcastGenerator
from voice_cloner import VoiceCloner

# Setup
job_id = "f15dcd0b-0621-4d58-99bb-497c98310539"
profile_path = f"local_storage/{job_id}/profile.json"

print("Testing Custom Voice Generation End-to-End")
print("=" * 60)

# Step 1: Check if profile exists
print(f"\n1. Checking profile: {profile_path}")
if os.path.exists(profile_path):
    with open(profile_path, "r") as f:
        profile = json.load(f)
    print(f"   ✅ Profile found!")
    print(f"   Gender: {'Female' if profile.get('is_female') else 'Male'}")
    print(f"   Pitch: {profile.get('pitch', {}).get('mean', 0):.0f} Hz")
else:
    print(f"   ❌ Profile not found!")
    exit(1)

# Step 2: Check if voice file exists
voice_file = profile.get("audio_reference")
print(f"\n2. Checking voice file: {voice_file}")
if os.path.exists(voice_file):
    print(f"   ✅ Voice file found!")
else:
    print(f"   ❌ Voice file not found!")
    # Update path
    voice_files = [
        f for f in os.listdir("temp_uploads") if f.startswith(f"{job_id}_voice_")
    ]
    if voice_files:
        voice_file = os.path.join("temp_uploads", voice_files[0])
        profile["audio_reference"] = voice_file
        print(f"   ✅ Updated to: {voice_file}")

# Step 3: Test voice synthesis
print(f"\n3. Testing voice synthesis with custom voice...")
try:
    vc = VoiceCloner()
    test_text = "Hello, this is a test of the custom voice feature with Indian accent."
    output_path = "test_output_custom.wav"

    vc.synthesize_with_custom_voice(
        text=test_text, voice_profile=profile, language="en", output_path=output_path
    )

    if os.path.exists(output_path):
        size = os.path.getsize(output_path)
        print(f"   ✅ Audio generated: {output_path} ({size} bytes)")
        print(f"\n🎉 SUCCESS! Custom voice is working!")
        print(f"\nYou can play: {output_path}")
    else:
        print(f"   ❌ Audio file not created!")

except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback

    traceback.print_exc()
