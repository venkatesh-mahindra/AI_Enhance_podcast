"""
PDF to Podcast Converter - Main Flask Application
Handles PDF upload, voice processing, and podcast generation with multi-narrator support
"""

import io
import json
import logging
import os  
import uuid
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
from datetime import datetime
from logging.handlers import RotatingFileHandler

import boto3
import numpy as np
import soundfile as sf
from botocore.exceptions import ClientError, NoCredentialsError
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from pydub import AudioSegment
from werkzeug.utils import secure_filename

# Environment variables already loaded above

# Import custom modules with error handling
try:
    from character_detector import CharacterDetector
    SPACY_AVAILABLE = True
    print(" Character detection available")
except Exception as e:
    print(f"  Character detection not available: {e}")
    SPACY_AVAILABLE = False
    class CharacterDetector:
        def __init__(self): pass
        def detect_characters(self, text): return []

try:
    from image_analyzer import ImageAnalyzer
    IMAGE_ANALYZER_AVAILABLE = True
    print(" Image analyzer available")
except Exception as e:
    print(f"  Image analyzer not available: {e}")
    IMAGE_ANALYZER_AVAILABLE = False
    class ImageAnalyzer:
        def __init__(self): pass

try:
    from pdf_processor import PDFProcessor
    PDF_PROCESSOR_AVAILABLE = True
    print(" PDF processor available")
except Exception as e:
    print(f"  PDF processor not available: {e}")
    PDF_PROCESSOR_AVAILABLE = False
    class PDFProcessor:
        def __init__(self): pass

try:
    from podcast_generator import PodcastGenerator
    PODCAST_GENERATOR_AVAILABLE = True
    print(" Podcast generator available")
except Exception as e:
    print(f"  Podcast generator not available: {e}")
    PODCAST_GENERATOR_AVAILABLE = False
    class PodcastGenerator:
        def __init__(self): pass

try:
    from voice_cloner import VoiceCloner
    VOICE_CLONER_AVAILABLE = True
    print(" Voice cloner available")
except Exception as e:
    print(f"  Voice cloner not available: {e}")
    VOICE_CLONER_AVAILABLE = False
    class VoiceCloner:
        def __init__(self): pass

app = Flask(__name__)
CORS(app)

# AWS S3 Configuration
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)

BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "pdf-podcast-bucket")
UPLOAD_FOLDER = "temp_uploads"
LOCAL_STORAGE = "local_storage"
ALLOWED_EXTENSIONS = {"pdf", "mp3", "wav", "ogg"}


# Determine S3 usage: explicit env or auto-disable if creds missing
def _has_aws_creds():
    return bool(os.getenv("AWS_ACCESS_KEY")) and bool(os.getenv("AWS_SECRET_KEY"))


USE_S3 = os.getenv("USE_S3", "").lower()
if USE_S3 in ("true", "1", "yes"):
    USE_S3 = True
elif USE_S3 in ("false", "0", "no"):
    USE_S3 = False
else:
    USE_S3 = _has_aws_creds()

# Initialize processors
pdf_processor = PDFProcessor()
image_analyzer = ImageAnalyzer()
podcast_generator = PodcastGenerator()
voice_cloner = VoiceCloner()
character_detector = CharacterDetector()

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(LOCAL_STORAGE, exist_ok=True)
os.makedirs("logs", exist_ok=True)
os.makedirs("default_voices", exist_ok=True)

# Configure application logging to files
log_formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

app_logger = app.logger
app_logger.setLevel(logging.INFO)

# Info/combined log
info_handler = RotatingFileHandler(
    "logs/app.log", maxBytes=5 * 1024 * 1024, backupCount=2
)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(log_formatter)
app_logger.addHandler(info_handler)

# Error log
error_handler = RotatingFileHandler(
    "logs/error.log", maxBytes=5 * 1024 * 1024, backupCount=2
)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(log_formatter)
app_logger.addHandler(error_handler)

# Ensure default voice placeholder WAVs exist
try:
    male_sample = "default_voices/male_sample.wav"
    female_sample = "default_voices/female_sample.wav"
    sample_rate = 22050
    silence = np.zeros(sample_rate, dtype="float32")
    if not os.path.exists(male_sample):
        sf.write(male_sample, silence, sample_rate)
        app.logger.info("Created placeholder default_voices/male_sample.wav")
    if not os.path.exists(female_sample):
        sf.write(female_sample, silence, sample_rate)
        app.logger.info("Created placeholder default_voices/female_sample.wav")
except Exception as e:
    app.logger.warning(f"Could not initialize default voice samples: {e}")


def allowed_file(filename):
    """Check if file extension is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/api/audio/<job_id>", methods=["GET"])
def get_local_audio(job_id):
    """Serve generated audio from local storage in dev mode.
    Use ?download=1 to force download.
    Use ?format=mp3 for MP3 conversion (requires ffmpeg).
    """
    try:
        # Check for both .wav and .mp3 files (handle legacy files)
        wav_path = os.path.join(LOCAL_STORAGE, job_id, "podcast.wav")
        mp3_path = os.path.join(LOCAL_STORAGE, job_id, "podcast.mp3")

        # Determine which file exists
        if os.path.exists(wav_path):
            audio_path = wav_path
            source_format = "wav"
        elif os.path.exists(mp3_path):
            audio_path = mp3_path
            source_format = "mp3"
        else:
            app.logger.error(
                f"Audio not found for job {job_id} in {os.path.join(LOCAL_STORAGE, job_id)}"
            )
            return (
                jsonify(
                    {"error": "Audio file not found. Please regenerate the podcast."}
                ),
                404,
            )

        as_attachment = request.args.get("download", "0") in ("1", "true", "yes")
        out_format = request.args.get("format", "").lower()

        # Handle MP3 request
        if out_format == "mp3":
            # If source is already MP3, just serve it
            if source_format == "mp3":
                app.logger.info(f"Serving existing MP3 for job {job_id}")
                return send_file(
                    audio_path,
                    mimetype="audio/mpeg",
                    as_attachment=as_attachment,
                    download_name="podcast.mp3",
                )

            # Source is WAV, try to convert to MP3
            try:
                app.logger.info(f"Attempting WAV to MP3 conversion for job {job_id}")
                wav_audio = AudioSegment.from_wav(audio_path)
                mp3_io = io.BytesIO()
                wav_audio.export(mp3_io, format="mp3", bitrate="192k")
                mp3_io.seek(0)

                app.logger.info(f"MP3 conversion successful for job {job_id}")
                return send_file(
                    mp3_io,
                    mimetype="audio/mpeg",
                    as_attachment=as_attachment,
                    download_name="podcast.mp3",
                )
            except FileNotFoundError as e:
                app.logger.warning(f"MP3 conversion failed - ffmpeg not found: {e}")
                app.logger.warning(
                    "Install ffmpeg from: https://ffmpeg.org/download.html"
                )
                # Return WAV with warning header
                response = send_file(
                    audio_path,
                    mimetype="audio/wav",
                    as_attachment=as_attachment,
                    download_name="podcast.wav",
                )
                response.headers[
                    "X-Conversion-Warning"
                ] = "MP3 conversion requires ffmpeg. Serving WAV instead."
                return response
            except Exception as e:
                app.logger.warning(f"MP3 conversion failed: {e}")
                # Return WAV as fallback
                response = send_file(
                    audio_path,
                    mimetype="audio/wav",
                    as_attachment=as_attachment,
                    download_name="podcast.wav",
                )
                response.headers[
                    "X-Conversion-Warning"
                ] = "MP3 conversion failed. Serving WAV instead."
                return response

        # Serve original file (WAV or MP3)
        if source_format == "wav":
            return send_file(
                audio_path,
                mimetype="audio/wav",
                as_attachment=as_attachment,
                download_name="podcast.wav",
            )
        else:  # source_format == 'mp3'
            return send_file(
                audio_path,
                mimetype="audio/mpeg",
                as_attachment=as_attachment,
                download_name="podcast.mp3",
            )
    except Exception as e:
        app.logger.error(f"Error serving local audio: {str(e)}")
        return jsonify({"error": "Failed to serve audio"}), 500


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return (
        jsonify(
            {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "service": "PDF to Podcast Converter",
            }
        ),
        200,
    )


@app.route("/api/synthesize-sample", methods=["POST"])
def synthesize_sample():
    """
    Generate a WAV sample for provided text and voice_type.
    Body: { text: str, voice_type: 'male'|'female'|'ai_neutral'|'ai_energetic', language?: str }
    Returns: audio/wav file
    """
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "text is required"}), 400
        text = data["text"]
        voice_type = data.get("voice_type", "ai_neutral")
        language = data.get("language", "en")

        job_id = str(uuid.uuid4())
        output_path = os.path.join(UPLOAD_FOLDER, f"{job_id}_sample.wav")

        voice_cloner.synthesize_with_default_voice(
            text=text, voice_type=voice_type, language=language, output_path=output_path
        )

        return send_file(
            output_path,
            mimetype="audio/wav",
            as_attachment=True,
            download_name="sample.wav",
        )
    except Exception as e:
        app.logger.error(f"Error synthesizing sample: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/voices", methods=["GET"])
def get_available_voices():
    """
    Get all available voice options
    Returns default voices (male, female, AI) and custom voice status
    """
    try:
        voices = voice_cloner.get_available_voices()
        return jsonify(voices), 200
    except Exception as e:
        app.logger.error(f"Error getting voices: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/upload-pdf", methods=["POST"])
def upload_pdf():
    """
    Upload PDF file and extract content
    Returns: job_id and extracted content preview
    """
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Only PDF allowed"}), 400

    try:
        s3_available = USE_S3
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, f"{job_id}_{filename}")

        # Save file temporarily
        file.save(file_path)

        # Upload to S3 (or skip in local mode)
        if s3_available:
            try:
                s3_key = f"pdfs/{job_id}/{filename}"
                s3_client.upload_file(file_path, BUCKET_NAME, s3_key)
            except (NoCredentialsError, ClientError) as e:
                app.logger.warning(
                    f"S3 unavailable, falling back to local storage: {e}"
                )
                s3_available = False

        # Process PDF
        extracted_data = pdf_processor.extract_content(file_path)

        # Save full content for later processing
        full_content = pdf_processor.extract_full_content(file_path)
        content_key = f"processed/{job_id}/content.json"

        # Convert PIL Images to serializable format
        for img in full_content.get("images", []):
            if "image" in img:
                del img["image"]  # Remove PIL image object for JSON serialization

        if s3_available:
            s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=content_key,
                Body=json.dumps(full_content, default=str),
                ContentType="application/json",
            )
        else:
            local_dir = os.path.join(LOCAL_STORAGE, job_id)
            os.makedirs(local_dir, exist_ok=True)
            with open(
                os.path.join(local_dir, "content.json"), "w", encoding="utf-8"
            ) as f:
                json.dump(full_content, f, default=str)

        # Save metadata to S3
        metadata = {
            "job_id": job_id,
            "filename": filename,
            "upload_time": datetime.now().isoformat(),
            "page_count": extracted_data["page_count"],
            "has_images": extracted_data["has_images"],
            "status": "uploaded",
        }

        if s3_available:
            s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=f"metadata/{job_id}/info.json",
                Body=json.dumps(metadata),
                ContentType="application/json",
            )
        else:
            local_dir = os.path.join(LOCAL_STORAGE, job_id)
            os.makedirs(local_dir, exist_ok=True)
            with open(os.path.join(local_dir, "info.json"), "w", encoding="utf-8") as f:
                json.dump(metadata, f)

        # Clean up local file
        os.remove(file_path)

        app.logger.info(f"PDF uploaded successfully: {job_id}")

        return (
            jsonify(
                {
                    "job_id": job_id,
                    "message": "PDF uploaded successfully",
                    "metadata": metadata,
                    "preview": extracted_data["preview"],
                }
            ),
            200,
        )

    except Exception as e:
        app.logger.error(f"Error uploading PDF: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/upload-voice", methods=["POST"])
def upload_voice():
    """
    Upload user's voice sample for cloning
    Expects: job_id and voice file (at least 10 seconds)
    """
    if "file" not in request.files or "job_id" not in request.form:
        return jsonify({"error": "Missing file or job_id"}), 400

    file = request.files["file"]
    job_id = request.form["job_id"]

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid audio format. Use MP3, WAV, or OGG"}), 400

    try:
        s3_available = USE_S3
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, f"{job_id}_voice_{filename}")
        file.save(file_path)

        # Analyze voice sample
        voice_analysis = voice_cloner.analyze_voice(file_path)

        if voice_analysis["duration"] < 10:
            os.remove(file_path)
            return (
                jsonify(
                    {"error": "Voice sample too short. Minimum 10 seconds required"}
                ),
                400,
            )

        # Upload to S3 (or skip in local mode)
        if s3_available:
            try:
                s3_key = f"voices/{job_id}/{filename}"
                s3_client.upload_file(file_path, BUCKET_NAME, s3_key)
            except (NoCredentialsError, ClientError) as e:
                app.logger.warning(
                    f"S3 unavailable, falling back to local storage: {e}"
                )
                s3_available = False

        # Create voice profile
        voice_profile = voice_cloner.create_profile(file_path, job_id)
        voice_profile["created_at"] = datetime.now().isoformat()
        voice_profile["audio_reference"] = file_path

        # Upload profile to S3
        if s3_available:
            profile_key = f"voices/{job_id}/profile.json"
            s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=profile_key,
                Body=json.dumps(voice_profile),
                ContentType="application/json",
            )
        else:
            local_dir = os.path.join(LOCAL_STORAGE, job_id)
            os.makedirs(local_dir, exist_ok=True)
            with open(
                os.path.join(local_dir, "profile.json"), "w", encoding="utf-8"
            ) as f:
                json.dump(voice_profile, f)

        # Keep local file for now (will be used during generation)
        # os.remove(file_path)

        app.logger.info(f"Voice uploaded successfully: {job_id}")

        return (
            jsonify(
                {
                    "message": "Voice uploaded successfully",
                    "job_id": job_id,
                    "voice_profile": voice_profile,
                }
            ),
            200,
        )

    except Exception as e:
        app.logger.error(f"Error uploading voice: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/analyze-characters", methods=["POST"])
def analyze_characters():
    """
    Analyze PDF for characters/speakers
    Returns: detected characters with gender identification
    """
    data = request.get_json()

    if "job_id" not in data:
        return jsonify({"error": "job_id required"}), 400

    job_id = data["job_id"]

    try:
        # Download processed content from S3
        content_key = f"processed/{job_id}/content.json"
        try:
            if USE_S3:
                content_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=content_key)
                content = json.loads(content_obj["Body"].read())
            else:
                local_path = os.path.join(LOCAL_STORAGE, job_id, "content.json")
                if not os.path.exists(local_path):
                    return (
                        jsonify(
                            {"error": "Content not found. Please upload PDF first."}
                        ),
                        404,
                    )
                with open(local_path, "r", encoding="utf-8") as f:
                    content = json.load(f)
        except Exception:
            return (
                jsonify({"error": "Content not found. Please upload PDF first."}),
                404,
            )

        # Extract text from content
        full_text = " ".join(
            [block["text"] for block in content.get("text_blocks", [])]
        )

        # Detect characters
        characters = character_detector.detect_characters(full_text)
        character_summary = character_detector.get_character_summary(characters)

        # Check if multi-narrator is beneficial
        has_dialogue = len(characters) >= 2

        app.logger.info(
            f"Characters analyzed: {job_id}, found {len(characters)} characters"
        )

        return (
            jsonify(
                {
                    "job_id": job_id,
                    "has_dialogue": has_dialogue,
                    "character_summary": character_summary,
                    "recommendation": "multi_narrator"
                    if has_dialogue
                    else "single_narrator",
                }
            ),
            200,
        )

    except Exception as e:
        app.logger.error(f"Error analyzing characters: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/generate-podcast", methods=["POST"])
def generate_podcast():
    """
    Generate podcast from PDF with voice selection
    Expects: job_id, language, voice_type, enable_multi_narrator (optional)
    """
    data = request.get_json()

    if "job_id" not in data:
        return jsonify({"error": "job_id required"}), 400

    job_id = data["job_id"]
    language = data.get("language", "en")
    voice_type = data.get("voice_type", "ai_neutral")
    enable_multi_narrator = data.get("enable_multi_narrator", True)
    multi_narrator_voice_set = data.get("multi_narrator_voice_set", None)
    use_custom_voice = voice_type == "custom"

    try:
        app.logger.info(
            f"Starting podcast generation: {job_id}, language={language}, voice={voice_type}"
        )

        # Load processed content (S3 or local)
        content_key = f"processed/{job_id}/content.json"
        if USE_S3:
            content_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=content_key)
            content = json.loads(content_obj["Body"].read())
        else:
            local_path = os.path.join(LOCAL_STORAGE, job_id, "content.json")
            if not os.path.exists(local_path):
                return (
                    jsonify({"error": "Content not found. Please upload PDF first."}),
                    404,
                )
            with open(local_path, "r", encoding="utf-8") as f:
                content = json.load(f)

        # Analyze diagrams and images (if any)
        # Note: Images were removed during upload for JSON serialization
        # In production, you'd download and process them here

        # Configure voice set for multi-narrator
        voice_set_config = None
        if enable_multi_narrator and multi_narrator_voice_set:
            # Voice set configurations matching frontend MULTI_NARRATOR_VOICE_SETS
            voice_sets = {
                'diverse_professional': {
                    'male': ['indian_male', 'male', 'ai_neutral'],
                    'female': ['indian_female', 'female', 'ai_energetic'],
                    'narrator': 'indian_male'
                },
                'all_indian_free': {
                    'male': ['indian_male'],
                    'female': ['indian_female'],
                    'narrator': 'indian_male'
                },
                'all_us_professional': {
                    'male': ['male', 'ai_neutral'],
                    'female': ['female', 'ai_energetic'],
                    'narrator': 'female'
                },
                'mixed_variety': {
                    'male': ['indian_male', 'male', 'ai_neutral'],
                    'female': ['indian_female', 'female', 'ai_energetic'],
                    'narrator': 'ai_neutral'
                }
            }
            voice_set_config = voice_sets.get(multi_narrator_voice_set, voice_sets['diverse_professional'])
            
            print(f"🎭 Using voice set: {multi_narrator_voice_set}")
            print(f"   Male voices: {voice_set_config.get('male', [])}")
            print(f"   Female voices: {voice_set_config.get('female', [])}")
            print(f"   Narrator voice: {voice_set_config.get('narrator', 'ai_neutral')}")

        # Generate podcast script (returns dict with type info)
        script_data = podcast_generator.create_script(
            content, language, enable_multi_narrator, voice_set_config
        )

        # Check if multi-narrator was detected
        is_multi_narrator = script_data.get("type") == "multi_narrator"
        character_info = (
            script_data.get("characters", {}) if is_multi_narrator else None
        )

        app.logger.info(f"Script created: multi_narrator={is_multi_narrator}")

        # Get voice profile if custom voice requested
        voice_profile = None
        if use_custom_voice:
            try:
                if USE_S3:
                    profile_key = f"voices/{job_id}/profile.json"
                    profile_obj = s3_client.get_object(
                        Bucket=BUCKET_NAME, Key=profile_key
                    )
                    voice_profile = json.loads(profile_obj["Body"].read())
                else:
                    local_profile = os.path.join(LOCAL_STORAGE, job_id, "profile.json")
                    if os.path.exists(local_profile):
                        with open(local_profile, "r", encoding="utf-8") as f:
                            voice_profile = json.load(f)

                # Get the local voice file path
                voice_files = [
                    f
                    for f in os.listdir(UPLOAD_FOLDER)
                    if f.startswith(f"{job_id}_voice_")
                ]
                if voice_files:
                    voice_profile["audio_reference"] = os.path.join(
                        UPLOAD_FOLDER, voice_files[0]
                    )

            except Exception as ve:
                app.logger.warning(f"Voice profile not found: {str(ve)}")
                return (
                    jsonify(
                        {"error": "Voice profile not found. Please upload voice first."}
                    ),
                    400,
                )

        # Generate audio with selected voice (handles both single and multi-narrator)
        audio_path = podcast_generator.generate_audio(
            script_data,
            language,
            voice_profile=voice_profile,
            job_id=job_id,
            voice_type=voice_type,
        )

        # Upload to S3 or expose local URL
        if USE_S3:
            audio_key = f"podcasts/{job_id}/podcast.mp3"
            s3_client.upload_file(audio_path, BUCKET_NAME, audio_key)
            audio_url = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": BUCKET_NAME, "Key": audio_key},
                ExpiresIn=3600,
            )
        else:
            local_dir = os.path.join(LOCAL_STORAGE, job_id)
            os.makedirs(local_dir, exist_ok=True)
            local_audio = os.path.join(local_dir, "podcast.wav")
            # Move/copy generated file to local storage
            try:
                if os.path.abspath(audio_path) != os.path.abspath(local_audio):
                    import shutil

                    shutil.copy2(audio_path, local_audio)
            except Exception as e:
                app.logger.warning(f"Failed to copy audio to local storage: {e}")
            audio_url = f"/api/audio/{job_id}"

        # Update metadata
        metadata_key = f"metadata/{job_id}/info.json"
        if USE_S3:
            metadata_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=metadata_key)
            metadata = json.loads(metadata_obj["Body"].read())
            metadata["status"] = "completed"
            metadata["completed_at"] = datetime.now().isoformat()
            metadata["podcast_url"] = audio_key
            metadata["language"] = language
            metadata["voice_type"] = voice_type
            metadata["is_multi_narrator"] = is_multi_narrator
            s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=metadata_key,
                Body=json.dumps(metadata),
                ContentType="application/json",
            )
        else:
            local_dir = os.path.join(LOCAL_STORAGE, job_id)
            os.makedirs(local_dir, exist_ok=True)
            local_meta = os.path.join(local_dir, "info.json")
            metadata = {}
            if os.path.exists(local_meta):
                try:
                    with open(local_meta, "r", encoding="utf-8") as f:
                        metadata = json.load(f)
                except Exception:
                    metadata = {}
            metadata.update(
                {
                    "status": "completed",
                    "completed_at": datetime.now().isoformat(),
                    "podcast_url": audio_url,
                    "language": language,
                    "voice_type": voice_type,
                    "is_multi_narrator": is_multi_narrator,
                }
            )
            with open(local_meta, "w", encoding="utf-8") as f:
                json.dump(metadata, f)

        # Clean up local file
        if USE_S3 and os.path.exists(audio_path):
            os.remove(audio_path)

        app.logger.info(f"Podcast generated successfully: {job_id}")

        return (
            jsonify(
                {
                    "message": "Podcast generated successfully",
                    "job_id": job_id,
                    "audio_url": audio_url,
                    "duration": podcast_generator.get_duration(audio_path)
                    if os.path.exists(audio_path)
                    else 0,
                    "is_multi_narrator": is_multi_narrator,
                    "characters": character_info,
                    "script_preview": script_data.get("script", "")[:500],
                }
            ),
            200,
        )

    except Exception as e:
        app.logger.error(f"Error generating podcast: {str(e)}")

        # Update metadata with error
        try:
            metadata_key = f"metadata/{job_id}/info.json"
            metadata_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=metadata_key)
            metadata = json.loads(metadata_obj["Body"].read())

            metadata["status"] = "failed"
            metadata["error"] = str(e)
            metadata["failed_at"] = datetime.now().isoformat()

            s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=metadata_key,
                Body=json.dumps(metadata),
                ContentType="application/json",
            )
        except:
            pass

        return jsonify({"error": str(e)}), 500


@app.route("/api/job-status/<job_id>", methods=["GET"])
def get_job_status(job_id):
    """Get status of a processing job"""
    try:
        # Load metadata and determine status
        if USE_S3:
            metadata_key = f"metadata/{job_id}/info.json"
            metadata_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=metadata_key)
            metadata = json.loads(metadata_obj["Body"].read())
            # Check if podcast exists
            podcast_key = f"podcasts/{job_id}/podcast.mp3"
            try:
                s3_client.head_object(Bucket=BUCKET_NAME, Key=podcast_key)
                status = "completed"
                podcast_url = s3_client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": BUCKET_NAME, "Key": podcast_key},
                    ExpiresIn=3600,
                )
            except Exception:
                status = metadata.get("status", "processing")
                podcast_url = None
        else:
            local_dir = os.path.join(LOCAL_STORAGE, job_id)
            local_meta = os.path.join(local_dir, "info.json")
            if not os.path.exists(local_meta):
                return jsonify({"error": "Job not found"}), 404
            with open(local_meta, "r", encoding="utf-8") as f:
                metadata = json.load(f)
            local_audio = os.path.join(local_dir, "podcast.wav")
            if os.path.exists(local_audio):
                status = "completed"
                podcast_url = f"/api/audio/{job_id}"
            else:
                status = metadata.get("status", "processing")
                podcast_url = None

        return (
            jsonify(
                {
                    "job_id": job_id,
                    "status": status,
                    "metadata": metadata,
                    "podcast_url": podcast_url,
                }
            ),
            200,
        )

    except Exception as e:
        app.logger.error(f"Error getting job status: {str(e)}")
        return jsonify({"error": "Job not found"}), 404


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    app.logger.error(f"Internal server error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    print("=" * 60)
    print("🎙️  PDF to Podcast Converter - Backend Server")
    print("=" * 60)
    print(f"📡 Starting server...")
    print(f"🔗 API URL: http://localhost:5000/api")
    print(f"💚 Health: http://localhost:5000/api/health")
    print("=" * 60)

    app.run(debug=os.getenv("FLASK_DEBUG", "True") == "True", host="0.0.0.0", port=5000)
