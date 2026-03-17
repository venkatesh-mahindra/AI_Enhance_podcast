"""
API Testing Suite for PDF to Podcast Converter
Run with: pytest tests/test_api.py -v
"""

import os
import sys

import pytest

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app as flask_app


@pytest.fixture
def app():
    """Create Flask app for testing"""
    flask_app.config["TESTING"] = True
    yield flask_app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


class TestHealthCheck:
    """Test health check endpoint"""

    def test_health_endpoint(self, client):
        """Test that health endpoint returns 200"""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.get_json()
        assert "status" in data
        assert data["status"] == "healthy"


class TestVoices:
    """Test voice endpoints"""

    def test_get_voices(self, client):
        """Test getting available voices"""
        response = client.get("/api/voices")
        assert response.status_code == 200
        data = response.get_json()
        assert "default_voices" in data
        assert "custom_voice_supported" in data


class TestPDFUpload:
    """Test PDF upload functionality"""

    def test_upload_pdf_no_file(self, client):
        """Test PDF upload with no file"""
        response = client.post("/api/upload-pdf")
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data


class TestJobStatus:
    """Test job status endpoint"""

    def test_get_job_status_invalid_id(self, client):
        """Test getting status for invalid job_id"""
        response = client.get("/api/job-status/invalid-job-id-12345")
        assert response.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
