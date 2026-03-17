"""
PDF Processor Tests
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pdf_processor import PDFProcessor


class TestPDFProcessor:
    def test_initialization(self):
        """Test PDFProcessor initialization"""
        processor = PDFProcessor()
        assert processor is not None
        assert "pdf" in processor.supported_formats


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
