"""
Celery Configuration for Asynchronous Task Processing
Handles long-running podcast generation tasks
"""

import os

from celery import Celery
from dotenv import load_dotenv
from kombu import Queue

load_dotenv()

# Initialize Celery
celery = Celery(
    "pdf_podcast",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
)

# Celery Configuration
celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # Task settings
    task_track_started=True,
    task_time_limit=1800,  # 30 minutes max
    task_soft_time_limit=1500,  # 25 minutes soft limit
    # Worker settings
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=50,
    # Result backend settings
    result_expires=3600,  # Results expire after 1 hour
    result_persistent=True,
    # Queue configuration
    task_default_queue="default",
    task_queues=(
        Queue("default", routing_key="task.#"),
        Queue("podcast_generation", routing_key="podcast.#"),
        Queue("voice_processing", routing_key="voice.#"),
    ),
    # Retry settings
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)

import json
from datetime import datetime

import boto3

from character_detector import CharacterDetector
from image_analyzer import ImageAnalyzer
# Import task modules
from pdf_processor import PDFProcessor
from podcast_generator import PodcastGenerator
from voice_cloner import VoiceCloner

# AWS S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)

BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "pdf-podcast-bucket")


@celery.task(bind=True, name="pdf_podcast.process_pdf")
def process_pdf_task(self, job_id, pdf_path):
    """
    Async task to process PDF
    """
    try:
        self.update_state(state="PROCESSING", meta={"status": "Extracting PDF content"})

        processor = PDFProcessor()
        content = processor.extract_full_content(pdf_path)

        # Upload processed content to S3
        content_key = f"processed/{job_id}/content.json"

        # Remove PIL images before JSON serialization
        for img in content.get("images", []):
            if "image" in img:
                del img["image"]

        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=content_key,
            Body=json.dumps(content, default=str),
            ContentType="application/json",
        )

        return {
            "status": "completed",
            "job_id": job_id,
            "page_count": content["metadata"]["page_count"],
            "has_images": len(content["images"]) > 0,
        }

    except Exception as e:
        self.update_state(state="FAILURE", meta={"error": str(e)})
        raise


@celery.task(bind=True, name="pdf_podcast.generate_podcast", queue="podcast_generation")
def generate_podcast_task(
    self, job_id, language="en", voice_type="ai_neutral", enable_multi_narrator=True
):
    """
    Async task to generate podcast
    This is a long-running task
    Supports: male, female, ai_neutral, ai_energetic, custom voices
    """
    try:
        # Update status
        self.update_state(
            state="PROCESSING", meta={"status": "Loading PDF content", "progress": 10}
        )

        # Download processed content from S3
        content_key = f"processed/{job_id}/content.json"
        content_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=content_key)
        content = json.loads(content_obj["Body"].read())

        # Initialize processors
        image_analyzer = ImageAnalyzer()
        podcast_generator = PodcastGenerator()
        voice_cloner = VoiceCloner()
        character_detector = CharacterDetector()

        # Analyze images
        self.update_state(
            state="PROCESSING",
            meta={"status": "Analyzing images and diagrams", "progress": 30},
        )

        if content["images"]:
            for idx, img_data in enumerate(content["images"]):
                description = image_analyzer.analyze_image(img_data)
                content["images"][idx]["description"] = description

                # Update progress
                progress = 30 + (20 * (idx + 1) / len(content["images"]))
                self.update_state(
                    state="PROCESSING",
                    meta={
                        "status": f'Analyzed image {idx + 1}/{len(content["images"])}',
                        "progress": progress,
                    },
                )

        # Generate script
        self.update_state(
            state="PROCESSING",
            meta={"status": "Creating podcast script", "progress": 50},
        )
        script_data = podcast_generator.create_script(
            content, language, enable_multi_narrator
        )

        # Check if multi-narrator was detected
        is_multi_narrator = script_data.get("type") == "multi_narrator"
        character_info = (
            script_data.get("characters", {}) if is_multi_narrator else None
        )

        # Get voice profile if custom voice requested
        voice_profile = None
        if voice_type == "custom":
            self.update_state(
                state="PROCESSING",
                meta={"status": "Loading custom voice profile", "progress": 60},
            )
            try:
                profile_key = f"voices/{job_id}/profile.json"
                profile_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=profile_key)
                voice_profile = json.loads(profile_obj["Body"].read())
            except:
                # If custom voice not found, fallback to AI neutral
                voice_type = "ai_neutral"

        # Generate audio with selected voice
        voice_name = {
            "male": "Professional Male",
            "female": "Professional Female",
            "ai_neutral": "AI Neutral",
            "ai_energetic": "AI Energetic",
            "custom": "Your Voice",
        }.get(voice_type, "AI Neutral")

        self.update_state(
            state="PROCESSING",
            meta={
                "status": f"Generating audio with {voice_name} voice (this may take a while)",
                "progress": 70,
            },
        )

        audio_path = podcast_generator.generate_audio(
            script=script_data,
            language=language,
            voice_profile=voice_profile,
            job_id=job_id,
            voice_type=voice_type,
        )

        # Upload to S3
        self.update_state(
            state="PROCESSING", meta={"status": "Uploading podcast", "progress": 90}
        )

        audio_key = f"podcasts/{job_id}/podcast.mp3"
        s3_client.upload_file(audio_path, BUCKET_NAME, audio_key)

        # Generate presigned URL
        audio_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": audio_key},
            ExpiresIn=3600,
        )

        # Update metadata
        metadata_key = f"metadata/{job_id}/info.json"
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

        # Clean up local file
        import os as os_module

        if os_module.path.exists(audio_path):
            os_module.remove(audio_path)

        return {
            "status": "completed",
            "job_id": job_id,
            "audio_url": audio_url,
            "progress": 100,
            "is_multi_narrator": is_multi_narrator,
            "characters": character_info,
        }

    except Exception as e:
        self.update_state(state="FAILURE", meta={"error": str(e), "progress": 0})

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

        raise


@celery.task(bind=True, name="pdf_podcast.process_voice", queue="voice_processing")
def process_voice_task(self, job_id, voice_path):
    """
    Async task to process voice sample
    """
    try:
        self.update_state(state="PROCESSING", meta={"status": "Analyzing voice sample"})

        voice_cloner = VoiceCloner()

        # Analyze voice
        analysis = voice_cloner.analyze_voice(voice_path)

        if analysis["duration"] < 10:
            raise ValueError("Voice sample too short. Minimum 10 seconds required")

        # Create profile
        voice_profile = voice_cloner.create_profile(voice_path, job_id)
        voice_profile["created_at"] = datetime.now().isoformat()

        # Upload to S3
        voice_key = f"voices/{job_id}/sample.wav"
        s3_client.upload_file(voice_path, BUCKET_NAME, voice_key)

        # Save profile
        profile_key = f"voices/{job_id}/profile.json"
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=profile_key,
            Body=json.dumps(voice_profile),
            ContentType="application/json",
        )

        return {"status": "completed", "job_id": job_id, "voice_profile": voice_profile}

    except Exception as e:
        self.update_state(state="FAILURE", meta={"error": str(e)})
        raise


# Celery beat schedule for periodic tasks (optional)
celery.conf.beat_schedule = {
    "cleanup-old-files": {
        "task": "pdf_podcast.cleanup_old_files",
        "schedule": 86400.0,  # Run daily
    },
}


@celery.task(name="pdf_podcast.cleanup_old_files")
def cleanup_old_files_task():
    """
    Clean up files older than 7 days
    """
    try:
        from datetime import timedelta

        cutoff_date = datetime.now() - timedelta(days=7)

        # List and delete old objects from S3
        paginator = s3_client.get_paginator("list_objects_v2")

        for prefix in ["pdfs/", "voices/", "podcasts/", "processed/"]:
            for page in paginator.paginate(Bucket=BUCKET_NAME, Prefix=prefix):
                if "Contents" not in page:
                    continue

                for obj in page["Contents"]:
                    if obj["LastModified"].replace(tzinfo=None) < cutoff_date:
                        s3_client.delete_object(Bucket=BUCKET_NAME, Key=obj["Key"])
                        print(f"Deleted old file: {obj['Key']}")

        return {"status": "completed", "cleaned_at": datetime.now().isoformat()}

    except Exception as e:
        return {"status": "failed", "error": str(e)}


if __name__ == "__main__":
    celery.start()
