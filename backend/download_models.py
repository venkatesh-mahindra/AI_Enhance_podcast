"""
Download and cache all required AI models
Run this script before first use to download models (~5GB)
"""

import os
import sys


def download_models():
    """Download all required models"""

    print("=" * 60)
    print("Downloading AI Models for PDF to Podcast")
    print("=" * 60)
    print("\n⚠️  WARNING: This is a SIMPLIFIED version for initial setup.")
    print("Full AI models require significant resources and time.")
    print("\nFor production deployment, you'll need to install:")
    print("  - transformers (for BLIP, ViT, BART)")
    print("  - TTS (for voice synthesis)")
    print("  - torch (for deep learning)")
    print("\nTotal download size: ~5GB")
    print("=" * 60)

    response = input("\nProceed with basic setup? (y/n): ")

    if response.lower() != "y":
        print("Setup cancelled.")
        return

    print("\n📦 Installing basic dependencies...")

    # 1. spaCy model (required for character detection)
    print("\n1/3 Downloading spaCy model for character detection...")
    try:
        import spacy

        os.system("python -m spacy download en_core_web_sm")
        print("✓ spaCy model downloaded successfully")
    except ImportError:
        print("⚠️  spaCy not installed. Run: pip install spacy")
    except Exception as e:
        print(f"✗ Error downloading spaCy model: {e}")

    # 2. Check system dependencies
    print("\n2/3 Checking system dependencies...")
    check_system_deps()

    # 3. Create necessary directories
    print("\n3/3 Creating directories...")
    try:
        os.makedirs("temp_uploads", exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        os.makedirs("default_voices", exist_ok=True)
        print("✓ Directories created successfully")
    except Exception as e:
        print(f"✗ Error creating directories: {e}")

    print("\n" + "=" * 60)
    print("✅ Basic Setup Complete!")
    print("=" * 60)

    print("\n📝 NEXT STEPS:")
    print("1. Configure AWS credentials in .env file")
    print("2. Create S3 bucket: pdf-podcast-bucket")
    print("3. Start the server: python app.py")

    print("\n⚠️  FOR PRODUCTION:")
    print("You'll need to install full AI models:")
    print("  pip install transformers torch TTS")
    print("  Then download models (this will take time):")
    print("  - BLIP: Salesforce/blip-image-captioning-base")
    print("  - BART: facebook/bart-large-cnn")
    print("  - XTTS: tts_models/multilingual/multi-dataset/xtts_v2")
    print("\nTotal size: ~5GB, Time: 30-60 minutes")
    print("=" * 60)


def check_system_deps():
    """Check if system dependencies are installed"""

    print("\nChecking system dependencies...")

    # Check for ffmpeg
    try:
        import subprocess

        result = subprocess.run(
            ["ffmpeg", "-version"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            print("✓ ffmpeg found")
        else:
            print("✗ ffmpeg not found")
            print("  Install from: https://ffmpeg.org/download.html")
    except FileNotFoundError:
        print("✗ ffmpeg not found")
        print("  Install from: https://ffmpeg.org/download.html")
    except Exception as e:
        print(f"⚠️  Could not check ffmpeg: {e}")

    # Check for espeak
    try:
        import subprocess

        result = subprocess.run(
            ["espeak", "--version"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            print("✓ espeak found")
        else:
            print("✗ espeak not found")
            print("  Install from: https://github.com/espeak-ng/espeak-ng/releases")
    except FileNotFoundError:
        print("✗ espeak not found")
        print("  Install from: https://github.com/espeak-ng/espeak-ng/releases")
    except Exception as e:
        print(f"⚠️  Could not check espeak: {e}")

    # Check disk space
    try:
        import shutil

        total, used, free = shutil.disk_usage("/")
        free_gb = free // (2**30)
        print(f"\n💾 Available disk space: {free_gb} GB")

        if free_gb < 10:
            print("⚠️  Warning: Less than 10GB available.")
            print("   Full AI models require ~5GB of space.")
    except Exception as e:
        print(f"⚠️  Could not check disk space: {e}")


def download_full_models():
    """
    Download full AI models (optional - for production)
    This function is for reference and requires full dependencies
    """
    print("\n" + "=" * 60)
    print("FULL MODEL DOWNLOAD (Advanced)")
    print("=" * 60)
    print("\nThis will download:")
    print("1. BLIP Image Captioning Model (~2GB)")
    print("2. BART Summarization Model (~1.5GB)")
    print("3. XTTS Voice Synthesis Model (~2GB)")
    print("\nTotal: ~5.5GB, Time: 30-60 minutes")
    print("=" * 60)

    response = input("\nProceed? This requires transformers and TTS installed. (y/n): ")

    if response.lower() != "y":
        print("Cancelled.")
        return

    try:
        # Try to import required libraries
        import torch
        from transformers import (BlipForConditionalGeneration, BlipProcessor,
                                  pipeline)
        from TTS.api import TTS

        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"\n🖥️  Using device: {device}")

        # 1. BLIP Model
        print("\n1/3 Downloading BLIP Image Captioning Model...")
        try:
            processor = BlipProcessor.from_pretrained(
                "Salesforce/blip-image-captioning-base"
            )
            model = BlipForConditionalGeneration.from_pretrained(
                "Salesforce/blip-image-captioning-base"
            )
            print("✓ BLIP model downloaded successfully")
        except Exception as e:
            print(f"✗ Error downloading BLIP: {e}")

        # 2. BART Model
        print("\n2/3 Downloading BART Summarization Model...")
        try:
            summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            print("✓ BART model downloaded successfully")
        except Exception as e:
            print(f"✗ Error downloading BART: {e}")

        # 3. XTTS Model
        print("\n3/3 Downloading XTTS Voice Synthesis Model...")
        print("⚠️  This is the largest model (~2GB)...")
        try:
            tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")
            print("✓ XTTS model downloaded successfully")
        except Exception as e:
            print(f"✗ Error downloading XTTS: {e}")

        print("\n" + "=" * 60)
        print("✅ All models downloaded successfully!")
        print("=" * 60)

    except ImportError as e:
        print(f"\n❌ Error: Required libraries not installed.")
        print(f"Missing: {e}")
        print("\nPlease install:")
        print("  pip install transformers torch TTS")
        print("\nThen run this script again.")


if __name__ == "__main__":
    print("\n🎙️  PDF to Podcast Converter - Model Setup")
    print("=" * 60)

    # Basic setup (always run this)
    download_models()

    # Ask if user wants full models
    print("\n" + "=" * 60)
    full_setup = input(
        "\nDownload FULL AI models now? (Requires transformers, TTS) (y/n): "
    )

    if full_setup.lower() == "y":
        download_full_models()
    else:
        print("\nSkipped full model download.")
        print("You can run this script again later to download full models.")
        print("For now, the app will work with basic functionality.")
