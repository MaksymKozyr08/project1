"""
data_manager.py - Vocabulary Data Storage & Scale-Optimized Repository.

Handles loading, validating, caching, and querying vocabulary data from words.json.
Guarantees fast, memory-efficient loading suitable for 3,000+ words datasets.
"""

import json
import os
import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Set

from words_generator import generate_words_json

@dataclass
class Flashcard:
    prompt: str
    target: str
    direction: str  # 'EN->UA' or 'UA->EN'
    chapter: str
    original_pair: Dict[str, str]

class VocabularyRepository:
    """
    In-memory vocabulary repository designed for high performance with 3,000+ words.
    Uses indexed chapter dictionaries and lazy card deck generator.
    """

    def __init__(self, json_path: str = "words.json"):
        if not os.path.isabs(json_path):
            base_dir = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(base_dir, json_path)
        self.json_path = json_path
        self.chapters: Dict[str, List[Dict[str, str]]] = {}
        self.load_data()


    def load_data(self) -> None:
        """Loads vocabulary from JSON file. Auto-generates fallback template if missing."""
        if not os.path.exists(self.json_path):
            print(f"[VocabularyRepository] '{self.json_path}' not found. Generating fallback template...")
            generate_words_json(self.json_path)

        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if isinstance(data, dict):
                self.chapters = data
            elif isinstance(data, list):
                # Fallback if user provides a flat list of dicts: group into 8 synthetic chapters
                self.chapters = self._group_flat_list(data)
            else:
                raise ValueError("Invalid JSON format for vocabulary file.")

        except Exception as e:
            print(f"[VocabularyRepository] Error reading {self.json_path}: {e}. Re-generating fallback...")
            generate_words_json(self.json_path)
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self.chapters = json.load(f)

        # Ensure we have at least 8 chapters available
        self._ensure_eight_chapters()

    def _group_flat_list(self, words: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
        """Groups a flat list into 8 balanced chapters."""
        result: Dict[str, List[Dict[str, str]]] = {}
        num_chapters = 8
        chunk_size = max(1, len(words) // num_chapters)
        for i in range(num_chapters):
            ch_name = f"Chapter {i+1}"
            start_idx = i * chunk_size
            end_idx = (i + 1) * chunk_size if i < num_chapters - 1 else len(words)
            result[ch_name] = words[start_idx:end_idx]
        return result

    def _ensure_eight_chapters(self) -> None:
        """Guarantees that at least 8 chapter keys exist in the repository."""
        if len(self.chapters) < 8:
            for i in range(1, 9):
                key = f"Chapter {i}"
                if not any(k.startswith(f"Chapter {i}") for k in self.chapters):
                    self.chapters[key] = []

    def get_chapter_names(self) -> List[str]:
        """Returns sorted list of chapter names."""
        return list(self.chapters.keys())

    def get_chapter_counts(self) -> Dict[str, int]:
        """Returns word count per chapter."""
        return {ch: len(words) for ch, words in self.chapters.items()}

    def get_total_word_count(self) -> int:
        """Returns total count across all chapters."""
        return sum(len(words) for words in self.chapters.values())

    def create_session_deck(
        self,
        selected_chapters: Optional[List[str]],
        direction: str = "EN->UA",
        shuffle: bool = True,
        max_words: Optional[int] = None
    ) -> List[Flashcard]:
        """
        Creates a session deck of Flashcard objects for chosen chapters and practice direction.
        Direction: 'EN->UA' (Prompt: English, Target: Ukrainian)
                   'UA->EN' (Prompt: Ukrainian, Target: English)
        """
        raw_pool: List[Tuple[str, Dict[str, str]]] = []

        if not selected_chapters or "All Words" in selected_chapters:
            # Include all chapters
            for ch_name, words in self.chapters.items():
                for pair in words:
                    raw_pool.append((ch_name, pair))
        else:
            selected_set: Set[str] = set(selected_chapters)
            for ch_name in selected_set:
                if ch_name in self.chapters:
                    for pair in self.chapters[ch_name]:
                        raw_pool.append((ch_name, pair))

        if shuffle:
            random.shuffle(raw_pool)

        if max_words and max_words > 0:
            raw_pool = raw_pool[:max_words]

        deck: List[Flashcard] = []
        for ch_name, pair in raw_pool:
            en_val = pair.get("en", "").strip()
            ua_val = pair.get("ua", "").strip()

            if direction == "EN->UA":
                prompt, target = en_val, ua_val
            else:
                prompt, target = ua_val, en_val

            if prompt and target:
                deck.append(Flashcard(
                    prompt=prompt,
                    target=target,
                    direction=direction,
                    chapter=ch_name,
                    original_pair=pair
                ))

        return deck

if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    repo = VocabularyRepository("words.json")
    print("Chapters loaded:", repo.get_chapter_names())
    print("Counts:", repo.get_chapter_counts())
    print("Total words:", repo.get_total_word_count())
    deck = repo.create_session_deck(["Chapter 1: Basics & Nouns"], direction="EN->UA")
    print("Sample session deck size:", len(deck))
    if deck:
        print("First card:", deck[0])

