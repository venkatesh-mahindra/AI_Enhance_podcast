"""
PDF to Podcast Converter - Main Flask Application (Temporary - Handle spacy errors)
"""

import io
import json
import logging
import os
import uuid
from datetime import datetime
from logging.handlers import RotatingFileHandler

import boto3
import numpy as np
import soundfile as sf
from botocore.exceptions import ClientError, NoCredentialsError
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

# Load environment variables
load_dotenv()

# Import custom modules with error handling
try:
    from character_detector import CharacterDetector
    from image_analyzer import ImageAnalyzer
    from pdf_processor import PDFProcessor
    from podcast_generator import PodcastGenerator
    SPACY_AVAILABLE = True
    print("✅ SpaCy and character detection available")
except Exception as e:
    print(f"⚠️  SpaCy/Character detection not available: {e}")
    SPACY_AVAILABLE = False
    # Create dummy classes
    class CharacterDetector:
        def __init__(self): pass
        def detect_characters(self, text): return []
    class ImageAnalyzer:
        def __init__(self): pass
    class PDFProcessor:
        def __init__(self): pass
    class PodcastGenerator:
        def __init__(self): pass

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
USE_S3 = os.getenv("USE_S3", "false").lower() == "true"
BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "pdf-podcast-bucket")
LOCAL_STORAGE = os.getenv("LOCAL_STORAGE", "storage")

# Initialize processors
if SPACY_AVAILABLE:
    pdf_processor = PDFProcessor()
    character_detector = CharacterDetector()
    image_analyzer = ImageAnalyzer()
    podcast_generator = PodcastGenerator()
    print("✅ All processors initialized successfully")
else:
    pdf_processor = PDFProcessor()
    character_detector = CharacterDetector()
    image_analyzer = ImageAnalyzer()
    podcast_generator = PodcastGenerator()
    print("⚠️  Running in limited mode without character detection")

# Setup logging
if not os.path.exists("logs"):
    os.makedirs("logs")

file_handler = RotatingFileHandler("logs/app.log", maxBytes=10240, backupCount=10)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info("PDF to Podcast Converter startup")

# S3 client (optional)
s3_client = None
if USE_S3:
    try:
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )
        print("✅ S3 client initialized")
    except Exception as e:
        print(f"⚠️  S3 client initialization failed: {e}")
        USE_S3 = False

@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "spacy_available": SPACY_AVAILABLE,
        "s3_enabled": USE_S3,
        "timestamp": datetime.now().isoformat()
    })

@app.route("/api/voices", methods=["GET"])
def get_available_voices():
    """Get available voice options"""
    voices = {
        "indian_male": "Natural Indian Male (FREE)",
        "indian_female": "Natural Indian Female (FREE)", 
        "male": "Professional Male (US)",
        "female": "Professional Female (US)",
        "ai_neutral": "AI Neutral (US)",
        "ai_energetic": "AI Energetic (US)",
        "custom": "Custom Voice"
    }
    return jsonify({"voices": voices})

if __name__ == "__main__":
    # Create storage directory if using local storage
    if not USE_S3 and not os.path.exists(LOCAL_STORAGE):
        os.makedirs(LOCAL_STORAGE)

    print("\n🚀 Starting PDF to Podcast Converter Backend...")
    print(f"   📁 Storage: {'S3' if USE_S3 else 'Local'}")
    print(f"   🎭 Character Detection: {'✅ Enabled' if SPACY_AVAILABLE else '⚠️  Limited'}")
    print(f"   🌐 Server: http://127.0.0.1:5000")
    print(f"   📊 Health: http://127.0.0.1:5000/api/health")
    
    app.run(host="127.0.0.1", port=5000, debug=True)
