#!/usr/bin/env python
"""Test script for male voice upload and synthesis"""

import json
import os

from voice_cloner import VoiceCloner

print("=" * 60)
print("MALE VOICE TESTING SCRIPT")
print("=" * 60)
print()

# Initialize voice cloner
vc = VoiceCloner()

# Find all voice files
voice_files = [f for f in os.listdir("temp_uploads") if "voice" in f]

if not voice_files:
    print("❌ No voice files found in temp_uploads!")
    print()
    print("Please upload a voice file through the web interface:")
    print("1. Go to http://localhost:3000")
    print("2. Upload PDF")
    print("3. Select 'Your Voice'")
    print("4. Upload your male friend's voice file")
    print()
    exit(1)

print(f"Found {len(voice_files)} voice file(s)")
print()

# Analyze each voice file
for idx, voice_file in enumerate(
    sorted(
        voice_files,
        key=lambda x: os.path.getmtime(os.path.join("temp_uploads", x)),
        reverse=True,
    )[:3]
):
    print(f"[{idx+1}] Analyzing: {voice_file}")
    print("-" * 60)

    file_path = os.path.join("temp_uploads", voice_file)

    # Check file size and modified time
    file_size = os.path.getsize(file_path)
    file_time = os.path.getmtime(file_path)

    print(f"  Size: {file_size/1024:.2f} KB")
    print(f"  Modified: {os.path.getmtime(file_path)}")

    # Analyze voice
    try:
        analysis = vc.analyze_voice(file_path)

        print(f"  Duration: {analysis['duration']:.1f} seconds")
        print(f"  Pitch: {analysis['pitch_mean']:.0f} Hz")
        print(f"  Quality: {analysis['quality']}")

        # Determine gender
        is_female = analysis["pitch_mean"] > 165
        gender = "Female" if is_female else "Male"
        print(f"  Gender: {gender}")

        # Create profile
        job_id = voice_file.split("_voice_")[0]
        profile = vc.create_profile(file_path, job_id)

        # Save profile
        local_dir = f"local_storage/{job_id}"
        os.makedirs(local_dir, exist_ok=True)

        with open(f"{local_dir}/profile.json", "w") as f:
            json.dump(profile, f, indent=2)

        print(f"  ✅ Profile saved!")

        # Test synthesis
        test_text = f"Hello! This is a test of the voice cloning feature. I am testing whether this sounds like a {gender.lower()} voice."
        output_path = f"test_voice_{idx+1}_{gender.lower()}.wav"

        print(f"  🎤 Generating test audio...")
        vc.synthesize_with_custom_voice(
            text=test_text,
            voice_profile=profile,
            language="en",
            output_path=output_path,
        )

        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"  ✅ Test audio generated: {output_path} ({size} bytes)")
            print(f"  🎧 Play this file to verify the voice!")

        print()

    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback

        traceback.print_exc()
        print()

print("=" * 60)
print("SUMMARY")
print("=" * 60)
print()
print("Generated test files:")
for i in range(1, 4):
    for gender in ["male", "female"]:
        file_name = f"test_voice_{i}_{gender}.wav"
        if os.path.exists(file_name):
            print(f"  ✅ {file_name}")

print()
print("To use a specific voice in the web app:")
print("1. Note the job_id from above")
print("2. Upload PDF in web app")
print("3. Select 'Your Voice'")
print("4. The system will use that voice profile!")
print()
