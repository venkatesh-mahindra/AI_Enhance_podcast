"""
Character Detector Tests
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from character_detector import CharacterDetector


class TestCharacterDetector:
    def test_initialization(self):
        """Test CharacterDetector initialization"""
        detector = CharacterDetector()
        assert detector is not None

    def test_gender_detection_male(self):
        """Test male name detection"""
        detector = CharacterDetector()
        gender = detector.detect_gender("John", "John said hello.")
        assert gender in ["male", "neutral"]

    def test_gender_detection_female(self):
        """Test female name detection"""
        detector = CharacterDetector()
        gender = detector.detect_gender("Mary", "Mary said hello.")
        assert gender in ["female", "neutral"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
