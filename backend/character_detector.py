"""
Character Detection & Gender Analysis Module
Detects different speakers/characters in text and assigns gender-appropriate voices
"""

import os
import re
from typing import Dict, List, Tuple

import spacy


class CharacterDetector:
    def __init__(self):
        """Initialize character detection tools"""
        # Load spaCy for NER (Named Entity Recognition)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            print(
                "⚠️  spaCy model not found. Run: python -m spacy download en_core_web_sm"
            )
            print("   Character detection will be limited.")
            self.nlp = None

        # Common dialogue patterns
        self.dialogue_patterns = [
            r'"([^"]+)"',  # Text in double quotes
            r"'([^']+)'",  # Text in single quotes
            r"([A-Z][a-z]+):\s*(.+?)(?=\n[A-Z][a-z]+:|$)",  # Name: dialogue format
            r'([A-Z][a-z]+)\s+said[,:]?\s*["\'](.+?)["\']',  # Name said "dialogue"
            r'([A-Z][a-z]+)\s+asked[,:]?\s*["\'](.+?)["\']',  # Name asked "dialogue"
        ]

        # Gender detection - common names database
        self.male_names = {
            "john",
            "michael",
            "david",
            "james",
            "robert",
            "william",
            "richard",
            "thomas",
            "charles",
            "daniel",
            "matthew",
            "mark",
            "donald",
            "paul",
            "george",
            "steven",
            "kenneth",
            "andrew",
            "brian",
            "edward",
            "kevin",
            "jason",
            "jeff",
            "ryan",
            "jacob",
            "nicholas",
            "eric",
            "jonathan",
            "peter",
            "alexander",
            "christopher",
            "samuel",
            "benjamin",
            "joseph",
            "raj",
            "amit",
            "rahul",
            "mohammed",
            "ali",
            "omar",
            "hassan",
            "ahmed",
        }

        self.female_names = {
            "mary",
            "jennifer",
            "linda",
            "patricia",
            "barbara",
            "elizabeth",
            "susan",
            "jessica",
            "sarah",
            "karen",
            "nancy",
            "margaret",
            "lisa",
            "betty",
            "dorothy",
            "sandra",
            "ashley",
            "kimberly",
            "donna",
            "emily",
            "michelle",
            "carol",
            "amanda",
            "melissa",
            "deborah",
            "stephanie",
            "rebecca",
            "laura",
            "sharon",
            "cynthia",
            "kathleen",
            "amy",
            "angela",
            "priya",
            "anjali",
            "pooja",
            "fatima",
            "aisha",
            "zainab",
            "maria",
        }

        # Gender indicators in text
        self.male_pronouns = {
            "he",
            "him",
            "his",
            "himself",
            "mr",
            "sir",
            "man",
            "boy",
            "father",
            "son",
            "brother",
            "uncle",
            "grandfather",
        }
        self.female_pronouns = {
            "she",
            "her",
            "hers",
            "herself",
            "mrs",
            "ms",
            "miss",
            "madam",
            "woman",
            "girl",
            "mother",
            "daughter",
            "sister",
            "aunt",
            "grandmother",
        }

    def detect_characters(self, text: str) -> List[Dict]:
        """
        Detect all characters/speakers in the text
        Returns list of characters with their detected gender
        """
        characters = {}

        if self.nlp is None:
            return []

        # Extract names using spaCy NER
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                name = ent.text
                if name not in characters:
                    # Detect gender for this character
                    gender = self.detect_gender(name, text)
                    characters[name] = {
                        "name": name,
                        "gender": gender,
                        "mentions": 1,
                        "dialogues": [],
                    }
                else:
                    characters[name]["mentions"] += 1

        # Also check for dialogue patterns
        for pattern in self.dialogue_patterns:
            matches = re.finditer(pattern, text, re.MULTILINE | re.DOTALL)
            for match in matches:
                if len(match.groups()) >= 2:
                    speaker = match.group(1).strip()
                    dialogue = (
                        match.group(2).strip()
                        if len(match.groups()) > 1
                        else match.group(1).strip()
                    )

                    if speaker and speaker[0].isupper():
                        if speaker not in characters:
                            gender = self.detect_gender(speaker, text)
                            characters[speaker] = {
                                "name": speaker,
                                "gender": gender,
                                "mentions": 1,
                                "dialogues": [dialogue],
                            }
                        else:
                            characters[speaker]["dialogues"].append(dialogue)

        return list(characters.values())

    def detect_gender(self, name: str, context: str = "") -> str:
        """
        Detect gender from name and context
        Returns: 'male', 'female', or 'neutral'
        """
        # Clean name
        first_name = name.split()[0].lower() if name else ""

        # Check against name databases
        if first_name in self.male_names:
            return "male"
        elif first_name in self.female_names:
            return "female"

        # Check context for pronouns
        if context:
            # Look for pronouns near the name
            context_lower = context.lower()
            name_lower = name.lower()

            # Find mentions of the name and check surrounding words
            name_positions = [
                m.start() for m in re.finditer(re.escape(name_lower), context_lower)
            ]

            male_count = 0
            female_count = 0

            for pos in name_positions:
                # Get surrounding context (200 chars before and after)
                start = max(0, pos - 200)
                end = min(len(context_lower), pos + 200)
                surrounding = context_lower[start:end]

                # Count gender-specific words
                for word in self.male_pronouns:
                    male_count += surrounding.count(word)
                for word in self.female_pronouns:
                    female_count += surrounding.count(word)

            if male_count > female_count:
                return "male"
            elif female_count > male_count:
                return "female"

        # Check title patterns
        if re.search(
            r"\b(mr|sir|lord)\b\.?\s*" + re.escape(name), context, re.IGNORECASE
        ):
            return "male"
        elif re.search(
            r"\b(mrs|ms|miss|lady)\b\.?\s*" + re.escape(name), context, re.IGNORECASE
        ):
            return "female"

        # Default to neutral if can't determine
        return "neutral"

    def extract_dialogues(self, text: str, characters: List[Dict]) -> List[Dict]:
        """
        Extract all dialogues and assign to characters
        Returns structured dialogue with speaker and text
        """
        dialogues = []

        # Pattern 1: Name: "dialogue"
        pattern1 = r'([A-Z][a-z]+):\s*["\']([^"\']+)["\']'
        matches = re.finditer(pattern1, text)
        for match in matches:
            speaker = match.group(1)
            dialogue = match.group(2)

            # Find character
            character = next((c for c in characters if c["name"] == speaker), None)
            if character:
                dialogues.append(
                    {
                        "speaker": speaker,
                        "gender": character["gender"],
                        "text": dialogue,
                        "position": match.start(),
                    }
                )

        # Pattern 2: "dialogue," Name said
        pattern2 = (
            r'["\']([^"\']+)["\'],?\s*([A-Z][a-z]+)\s+(?:said|asked|replied|answered)'
        )
        matches = re.finditer(pattern2, text)
        for match in matches:
            dialogue = match.group(1)
            speaker = match.group(2)

            character = next((c for c in characters if c["name"] == speaker), None)
            if character:
                dialogues.append(
                    {
                        "speaker": speaker,
                        "gender": character["gender"],
                        "text": dialogue,
                        "position": match.start(),
                    }
                )

        # Pattern 3: Name said, "dialogue"
        pattern3 = r'([A-Z][a-z]+)\s+(?:said|asked|replied|answered)[,:]?\s*["\']([^"\']+)["\']'
        matches = re.finditer(pattern3, text)
        for match in matches:
            speaker = match.group(1)
            dialogue = match.group(2)

            character = next((c for c in characters if c["name"] == speaker), None)
            if character:
                dialogues.append(
                    {
                        "speaker": speaker,
                        "gender": character["gender"],
                        "text": dialogue,
                        "position": match.start(),
                    }
                )

        # Sort by position in text
        dialogues.sort(key=lambda x: x["position"])

        return dialogues

    def create_multi_voice_script(self, text: str) -> List[Dict]:
        """
        Create a complete script with character assignments
        Returns structured script with voice assignments
        """
        # Detect characters
        characters = self.detect_characters(text)

        if not characters:
            # No characters detected, return as narrative
            return [
                {
                    "type": "narrative",
                    "speaker": "narrator",
                    "gender": "neutral",
                    "text": text,
                }
            ]

        # Extract dialogues
        dialogues = self.extract_dialogues(text, characters)

        if not dialogues:
            # No dialogue structure, return as narrative
            return [
                {
                    "type": "narrative",
                    "speaker": "narrator",
                    "gender": "neutral",
                    "text": text,
                }
            ]

        # Build script with narrative and dialogue
        script_segments = []
        last_pos = 0

        for dialogue in dialogues:
            # Add narrative before dialogue
            if dialogue["position"] > last_pos:
                narrative_text = text[last_pos : dialogue["position"]].strip()
                if narrative_text:
                    script_segments.append(
                        {
                            "type": "narrative",
                            "speaker": "narrator",
                            "gender": "neutral",
                            "text": narrative_text,
                        }
                    )

            # Add dialogue
            script_segments.append(
                {
                    "type": "dialogue",
                    "speaker": dialogue["speaker"],
                    "gender": dialogue["gender"],
                    "text": dialogue["text"],
                }
            )

            last_pos = dialogue["position"] + len(dialogue["text"])

        # Add remaining narrative
        if last_pos < len(text):
            narrative_text = text[last_pos:].strip()
            if narrative_text:
                script_segments.append(
                    {
                        "type": "narrative",
                        "speaker": "narrator",
                        "gender": "neutral",
                        "text": narrative_text,
                    }
                )

        return script_segments

    def assign_voices(
        self, script_segments: List[Dict], voice_set_config: Dict = None
    ) -> List[Dict]:
        """
        Assign voice types to script segments based on gender and voice set configuration
        """
        if voice_set_config is None:
            # Default voice configuration
            voice_set_config = {
                "male": ["male", "ai_neutral"],
                "female": ["female", "ai_energetic"],
                "narrator": "ai_neutral"
            }

        # Track voice assignment for each character
        character_voice_map = {}
        male_voice_index = 0
        female_voice_index = 0
        
        for segment in script_segments:
            speaker = segment.get("speaker", "unknown")
            gender = segment["gender"]
            
            # Assign voice based on character and gender
            if speaker == "narrator" or gender == "neutral":
                # Use narrator voice for narrative content
                narrator_voice = voice_set_config.get("narrator", "ai_neutral")
                segment["voice_type"] = narrator_voice
            elif speaker in character_voice_map:
                # Use previously assigned voice for this character
                segment["voice_type"] = character_voice_map[speaker]
            else:
                # Assign new voice for this character
                if gender == "male" and "male" in voice_set_config:
                    male_voices = voice_set_config["male"]
                    if male_voices:
                        voice = male_voices[male_voice_index % len(male_voices)]
                        character_voice_map[speaker] = voice
                        segment["voice_type"] = voice
                        male_voice_index += 1
                    else:
                        segment["voice_type"] = "male"  # fallback
                elif gender == "female" and "female" in voice_set_config:
                    female_voices = voice_set_config["female"]
                    if female_voices:
                        voice = female_voices[female_voice_index % len(female_voices)]
                        character_voice_map[speaker] = voice
                        segment["voice_type"] = voice
                        female_voice_index += 1
                    else:
                        segment["voice_type"] = "female"  # fallback
                else:
                    # Fallback for unknown genders
                    segment["voice_type"] = voice_set_config.get("narrator", "ai_neutral")

        # Log voice assignments for debugging
        print(f"🎭 Voice assignments:")
        for speaker, voice in character_voice_map.items():
            print(f"   {speaker}: {voice}")

        return script_segments

    def get_character_summary(self, characters: List[Dict]) -> Dict:
        """
        Get summary of detected characters
        """
        summary = {
            "total_characters": len(characters),
            "male_characters": sum(1 for c in characters if c["gender"] == "male"),
            "female_characters": sum(1 for c in characters if c["gender"] == "female"),
            "neutral_characters": sum(
                1 for c in characters if c["gender"] == "neutral"
            ),
            "characters": [
                {"name": c["name"], "gender": c["gender"], "mentions": c["mentions"]}
                for c in sorted(characters, key=lambda x: x["mentions"], reverse=True)
            ],
        }

        return summary
