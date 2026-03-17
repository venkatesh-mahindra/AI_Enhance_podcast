"""
Podcast Generator Module
Creates podcast script from PDF content and generates audio with multi-narrator support
"""

import os
import tempfile
from typing import Dict, List

import librosa

from character_detector import CharacterDetector
from voice_cloner import VoiceCloner


class PodcastGenerator:
    def __init__(self):
        """Initialize podcast generation tools"""
        self.voice_cloner = VoiceCloner()
        self.character_detector = CharacterDetector()

    def create_script(
        self, content: Dict, language: str = "en", enable_multi_narrator: bool = True, voice_set_config: Dict = None
    ) -> Dict:
        """
        Create engaging podcast script from PDF content
        Includes narration for images and diagrams
        Returns script with multi-narrator segments if detected
        """
        script_parts = []
        full_text = ""

        # Introduction
        title = content["metadata"].get("title", "this document")
        intro = self._generate_intro(title, language)
        script_parts.append(intro)

        # Process content chronologically
        current_page = 0

        for block in content["text_blocks"]:
            # Page transition
            if block["page"] != current_page:
                current_page = block["page"]
                if current_page > 1:
                    transition = self._get_transition_phrase(language)
                    script_parts.append(transition)

            # Add text content
            if block["type"] == "heading":
                text = self._format_heading(block["text"], language)
                script_parts.append(text)
                full_text += text + " "
            elif block["type"] == "paragraph":
                # Convert to natural speech
                natural_text = self._make_conversational(block["text"], language)
                script_parts.append(natural_text)
                full_text += natural_text + " "
            elif block["type"] == "list_item":
                text = self._format_list_item(block["text"], language)
                script_parts.append(text)
                full_text += text + " "

            # Check for images at this position
            page_images = [
                img for img in content["images"] if img["page"] == block["page"]
            ]

            for img in page_images:
                if "podcast_description" in img:
                    script_parts.append(img["podcast_description"])

        # Conclusion
        conclusion = self._generate_conclusion(language)
        script_parts.append(conclusion)

        # Join all parts for character detection
        full_script = "\n\n".join(script_parts)

        # Detect characters and create multi-narrator script if enabled
        if enable_multi_narrator:
            characters = self.character_detector.detect_characters(full_text)

            if characters and len(characters) >= 2:
                # Multi-narrator content detected
                script_segments = self.character_detector.create_multi_voice_script(
                    full_script
                )
                script_segments = self.character_detector.assign_voices(script_segments, voice_set_config)

                character_summary = self.character_detector.get_character_summary(
                    characters
                )

                return {
                    "type": "multi_narrator",
                    "script": full_script,
                    "segments": script_segments,
                    "characters": character_summary,
                    "language": language,
                }

        # Single narrator (default)
        return {"type": "single_narrator", "script": full_script, "language": language}

    def _generate_intro(self, title: str, language: str) -> str:
        """Generate engaging introduction"""
        intros = {
            "en": f"Welcome! Today we're exploring {title}. Let's dive in and discover what this document has to share with us.",
            "es": f"¡Bienvenidos! Hoy exploraremos {title}. Vamos a sumergirnos y descubrir qué tiene para compartir este documento.",
            "fr": f"Bienvenue! Aujourd'hui, nous explorons {title}. Plongeons et découvrons ce que ce document a à partager.",
            "de": f"Willkommen! Heute erkunden wir {title}. Lassen Sie uns eintauchen und entdecken, was dieses Dokument zu bieten hat.",
        }
        return intros.get(language, intros["en"])

    def _generate_conclusion(self, language: str) -> str:
        """Generate conclusion"""
        conclusions = {
            "en": "That brings us to the end of this document. Thank you for listening!",
            "es": "Esto nos lleva al final de este documento. ¡Gracias por escuchar!",
            "fr": "Cela nous amène à la fin de ce document. Merci d'avoir écouté!",
            "de": "Das bringt uns zum Ende dieses Dokuments. Vielen Dank fürs Zuhören!",
        }
        return conclusions.get(language, conclusions["en"])

    def _get_transition_phrase(self, language: str) -> str:
        """Get page transition phrase"""
        transitions = {
            "en": "Moving forward,",
            "es": "Continuando,",
            "fr": "En continuant,",
            "de": "Weiter geht's,",
        }
        return transitions.get(language, transitions["en"])

    def _format_heading(self, text: str, language: str) -> str:
        """Format heading for natural speech"""
        prefixes = {
            "en": "Now, let's talk about:",
            "es": "Ahora, hablemos de:",
            "fr": "Maintenant, parlons de:",
            "de": "Jetzt sprechen wir über:",
        }
        prefix = prefixes.get(language, prefixes["en"])
        return f"{prefix} {text}"

    def _format_list_item(self, text: str, language: str) -> str:
        """Format list item for natural speech"""
        # Remove bullet points and numbers
        clean_text = text.lstrip("•-*0123456789. ")
        return clean_text

    def _make_conversational(self, text: str, language: str) -> str:
        """
        Convert formal text to conversational speech
        """
        # Remove multiple spaces
        text = " ".join(text.split())

        # Add pauses for better listening (using punctuation)
        text = text.replace(". ", ". ")

        return text

    def generate_audio(
        self,
        script_data: Dict,
        language: str = "en",
        voice_profile: Dict = None,
        job_id: str = None,
        voice_type: str = "ai_neutral",
    ) -> str:
        """
        Generate audio from script with voice selection
        Supports: single narrator, multi-narrator, custom voice
        """
        try:
            # Create temporary directory for segments
            temp_dir = tempfile.mkdtemp()

            # Check if multi-narrator
            if (
                isinstance(script_data, dict)
                and script_data.get("type") == "multi_narrator"
            ):
                # Multi-narrator mode
                audio_files = self._generate_multi_narrator_audio(
                    script_data=script_data, language=language, temp_dir=temp_dir
                )
            else:
                # Single narrator mode
                script = (
                    script_data
                    if isinstance(script_data, str)
                    else script_data.get("script", "")
                )
                segments = self._split_script(script)

                # Check if custom voice should be used
                if voice_profile and voice_type == "custom":
                    print(f"🎤 Using CUSTOM voice for podcast generation")
                    audio_files = self._synthesize_with_custom_voice(
                        segments, voice_profile, language, temp_dir
                    )
                else:
                    audio_files = self._synthesize_with_default_voice(
                        segments, voice_type, language, temp_dir
                    )

            # Concatenate all segments (write WAV for broad compatibility)
            output_path = os.path.join(temp_dir, f"{job_id}_podcast.wav")
            final_audio = self.voice_cloner.concatenate_audio(
                audio_files=audio_files, output_path=output_path, pause_duration=0.7
            )

            return final_audio

        except Exception as e:
            raise Exception(f"Error generating audio: {str(e)}")

    def _generate_multi_narrator_audio(
        self, script_data: Dict, language: str, temp_dir: str
    ) -> List[str]:
        """
        Generate audio with multiple narrators/voices
        """
        audio_files = []
        segments = script_data.get("segments", [])

        print(f"🎭 Generating multi-narrator podcast with {len(segments)} segments")
        print(
            f"📊 Characters detected: {script_data.get('characters', {}).get('total_characters', 0)}"
        )

        for idx, segment in enumerate(segments):
            text = segment["text"]
            voice_type = segment["voice_type"]
            speaker = segment.get("speaker", "narrator")

            print(f"  Segment {idx+1}/{len(segments)}: {speaker} ({voice_type})")

            output_path = f"{temp_dir}/segment_{idx:04d}.wav"

            # Generate with appropriate voice
            self.voice_cloner.synthesize_with_default_voice(
                text=text,
                voice_type=voice_type,
                language=language,
                output_path=output_path,
            )

            audio_files.append(output_path)

        return audio_files

    def _split_script(self, script: str) -> List[str]:
        """
        Split script into segments suitable for TTS
        Each segment should be 1-3 sentences
        """
        # Split by paragraphs first
        paragraphs = script.split("\n\n")

        segments = []
        for para in paragraphs:
            if len(para) < 500:
                segments.append(para)
            else:
                # Split long paragraphs by sentences
                sentences = para.split(". ")
                current_segment = ""

                for sentence in sentences:
                    if len(current_segment) + len(sentence) < 500:
                        current_segment += sentence + ". "
                    else:
                        if current_segment:
                            segments.append(current_segment.strip())
                        current_segment = sentence + ". "

                if current_segment:
                    segments.append(current_segment.strip())

        return [s for s in segments if s.strip()]

    def _synthesize_with_custom_voice(
        self, segments: List[str], voice_profile: Dict, language: str, output_dir: str
    ) -> List[str]:
        """
        Synthesize audio using uploaded custom voice profile
        """
        output_files = []

        print(f"🎙️ Generating podcast with custom voice ({len(segments)} segments)")

        for idx, segment in enumerate(segments):
            output_path = f"{output_dir}/segment_{idx:04d}.wav"

            self.voice_cloner.synthesize_with_custom_voice(
                text=segment,
                voice_profile=voice_profile,
                language=language,
                output_path=output_path,
            )

            output_files.append(output_path)

            if (idx + 1) % 5 == 0:
                print(f"   Progress: {idx+1}/{len(segments)} segments completed")

        return output_files

    def _synthesize_with_default_voice(
        self, segments: List[str], voice_type: str, language: str, output_dir: str
    ) -> List[str]:
        """
        Synthesize audio using selected default voice (male, female, AI)
        """
        output_files = []

        for idx, segment in enumerate(segments):
            output_path = f"{output_dir}/segment_{idx:04d}.wav"

            self.voice_cloner.synthesize_with_default_voice(
                text=segment,
                voice_type=voice_type,
                language=language,
                output_path=output_path,
            )

            output_files.append(output_path)

        return output_files

    def get_duration(self, audio_path: str) -> float:
        """Get audio duration in seconds"""
        try:
            if not os.path.exists(audio_path):
                return 0.0
            audio, sr = librosa.load(audio_path, sr=None)
            duration = librosa.get_duration(y=audio, sr=sr)
            return float(duration)
        except:
            return 0.0
