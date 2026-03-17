#!/usr/bin/env python
"""Test voice profile creation with the fix"""

import json

from voice_cloner import VoiceCloner

vc = VoiceCloner()

# Test with the uploaded voice
voice_file = "temp_uploads/f15dcd0b-0621-4d58-99bb-497c98310539_voice_Ananya_Voice.ogg"
job_id = "f15dcd0b-0621-4d58-99bb-497c98310539"

print(f"Testing voice profile creation for: {voice_file}")
print("=" * 60)

try:
    profile = vc.create_profile(voice_file, job_id)

    print("\n✅ SUCCESS! Profile created")
    print("\nProfile details:")
    print(f"  Job ID: {profile.get('job_id')}")
    print(f"  Gender: {'Female' if profile.get('is_female') else 'Male'}")
    print(f"  Pitch: {profile.get('pitch', {}).get('mean', 0):.0f} Hz")
    print(f"  Speech Rate: {profile.get('speech_rate', {}).get('mean', 0):.2f}x")
    print(f"  Quality: {profile.get('analysis', {}).get('quality', 'unknown')}")
    print(f"  Duration: {profile.get('analysis', {}).get('duration', 0):.1f}s")

    # Save it
    import os

    local_dir = f"local_storage/{job_id}"
    os.makedirs(local_dir, exist_ok=True)

    with open(f"{local_dir}/profile.json", "w") as f:
        json.dump(profile, f, indent=2)

    print(f"\n✅ Profile saved to: {local_dir}/profile.json")
    print("\n🎉 Voice profile is ready! You can now generate podcast!")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback

    traceback.print_exc()
