"""
app.py - Unified Desktop GUI Application for Vocabulary Flashcard Drilling.

Self-contained application containing data models, repository, diff evaluator,
and desktop GUI (with CustomTkinter and automatic Tkinter fallback support).
"""

import json
import os
import random
import difflib
import sys
import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Set, cast

# Safe import of customtkinter with automatic fallback to standard tkinter
try:
    import customtkinter as ctk
    HAS_CUSTOMTKINTER = True
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
except ImportError:
    HAS_CUSTOMTKINTER = False
    print("\n" + "=" * 70)
    print(" NOTICE: 'customtkinter' module is not installed.")
    print(" To enable the modern styled dark theme interface, please run:")
    print("     pip install customtkinter")
    print(" Falling back to standard Tkinter interface...")
    print("=" * 70 + "\n")

    def _resolve_master(master):
        if hasattr(master, "scrollable_frame"):
            return master.scrollable_frame
        return master

    class CTkFallback(tk.Tk):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.configure(bg="#181825")

    class CTkFrameFallback(tk.Frame):
        def __init__(self, master=None, **kwargs):
            master = _resolve_master(master)
            fg_color = kwargs.pop("fg_color", None)
            kwargs.pop("corner_radius", None)
            border_width = kwargs.pop("border_width", None)
            border_color = kwargs.pop("border_color", None)
            if fg_color is not None:
                if fg_color == "transparent":
                    bg = getattr(master, "cget", lambda x: "#181825")("bg") if master else "#181825"
                    kwargs["bg"] = bg
                else:
                    kwargs["bg"] = fg_color
            if border_width is not None:
                kwargs["bd"] = border_width
                kwargs["relief"] = "solid"
            if border_color is not None and "highlightbackground" not in kwargs:
                kwargs["highlightbackground"] = border_color
                kwargs["highlightthickness"] = 1
            super().__init__(master, **kwargs)

        def configure(self, **kwargs):
            fg_color = kwargs.pop("fg_color", None)
            kwargs.pop("corner_radius", None)
            kwargs.pop("border_width", None)
            kwargs.pop("border_color", None)
            if fg_color is not None:
                if fg_color == "transparent":
                    kwargs["bg"] = getattr(self.master, "cget", lambda x: "#181825")("bg")
                else:
                    kwargs["bg"] = fg_color
            if kwargs:
                super().configure(**kwargs)

    class CTkLabelFallback(tk.Label):
        def __init__(self, master=None, **kwargs):
            master = _resolve_master(master)
            text_color = kwargs.pop("text_color", None)
            fg_color = kwargs.pop("fg_color", None)
            kwargs.pop("font", None)
            if text_color:
                kwargs["fg"] = text_color
            if fg_color and fg_color != "transparent":
                kwargs["bg"] = fg_color
            elif "bg" not in kwargs:
                kwargs["bg"] = getattr(master, "cget", lambda x: "#181825")("bg") if master else "#181825"
            super().__init__(master, **kwargs)

        def configure(self, **kwargs):
            text_color = kwargs.pop("text_color", None)
            fg_color = kwargs.pop("fg_color", None)
            kwargs.pop("font", None)
            if text_color:
                kwargs["fg"] = text_color
            if fg_color:
                kwargs["bg"] = fg_color if fg_color != "transparent" else getattr(self.master, "cget", lambda x: "#181825")("bg")
            if kwargs:
                super().configure(**kwargs)

    class CTkButtonFallback(tk.Button):
        def __init__(self, master=None, **kwargs):
            master = _resolve_master(master)
            fg_color = kwargs.pop("fg_color", None)
            hover_color = kwargs.pop("hover_color", None)
            text_color = kwargs.pop("text_color", None)
            kwargs.pop("corner_radius", None)
            kwargs.pop("font", None)
            if fg_color:
                kwargs["bg"] = fg_color
                kwargs["activebackground"] = hover_color if hover_color else fg_color
            if text_color:
                kwargs["fg"] = text_color
                kwargs["activeforeground"] = text_color
            kwargs.setdefault("relief", "flat")
            kwargs.setdefault("bd", 0)
            kwargs.setdefault("pady", 6)
            kwargs.setdefault("padx", 12)
            super().__init__(master, **kwargs)

        def configure(self, **kwargs):
            fg_color = kwargs.pop("fg_color", None)
            hover_color = kwargs.pop("hover_color", None)
            text_color = kwargs.pop("text_color", None)
            kwargs.pop("corner_radius", None)
            kwargs.pop("font", None)
            if fg_color:
                kwargs["bg"] = fg_color
                if hover_color:
                    kwargs["activebackground"] = hover_color
            if text_color:
                kwargs["fg"] = text_color
            if kwargs:
                super().configure(**kwargs)

    class CTkEntryFallback(tk.Entry):
        def __init__(self, master=None, **kwargs):
            master = _resolve_master(master)
            kwargs.pop("placeholder_text", None)
            fg_color = kwargs.pop("fg_color", None)
            kwargs.pop("corner_radius", None)
            kwargs.pop("font", None)
            border_width = kwargs.pop("border_width", None)
            border_color = kwargs.pop("border_color", None)
            if fg_color:
                kwargs["bg"] = fg_color
                kwargs["insertbackground"] = "#cdd6f4"
                kwargs["fg"] = "#cdd6f4"
            if border_width:
                kwargs["bd"] = border_width
                kwargs["relief"] = "solid"
            if border_color:
                kwargs["highlightbackground"] = border_color
                kwargs["highlightcolor"] = border_color
                kwargs["highlightthickness"] = 1
            super().__init__(master, **kwargs)

        def configure(self, **kwargs):
            kwargs.pop("placeholder_text", None)
            fg_color = kwargs.pop("fg_color", None)
            kwargs.pop("corner_radius", None)
            kwargs.pop("font", None)
            kwargs.pop("border_width", None)
            border_color = kwargs.pop("border_color", None)
            if fg_color:
                kwargs["bg"] = fg_color
            if border_color:
                kwargs["highlightbackground"] = border_color
                kwargs["highlightcolor"] = border_color
            if kwargs:
                super().configure(**kwargs)

    class CTkCheckBoxFallback(tk.Checkbutton):
        def __init__(self, master=None, **kwargs):
            master = _resolve_master(master)
            text_color = kwargs.pop("text_color", None)
            kwargs.pop("fg_color", None)
            kwargs.pop("hover_color", None)
            kwargs.pop("font", None)
            if text_color:
                kwargs["fg"] = text_color
            bg = getattr(master, "cget", lambda x: "#181825")("bg") if master else "#181825"
            kwargs.setdefault("bg", bg)
            kwargs.setdefault("activebackground", bg)
            kwargs.setdefault("activeforeground", text_color or "#cdd6f4")
            kwargs.setdefault("selectcolor", "#313244")
            super().__init__(master, **kwargs)

        def configure(self, **kwargs):
            text_color = kwargs.pop("text_color", None)
            kwargs.pop("fg_color", None)
            kwargs.pop("hover_color", None)
            kwargs.pop("font", None)
            if text_color:
                kwargs["fg"] = text_color
            if kwargs:
                super().configure(**kwargs)

    class CTkProgressBarFallback(ttk.Progressbar):
        def __init__(self, master=None, **kwargs):
            master = _resolve_master(master)
            kwargs.pop("height", None)
            kwargs.pop("corner_radius", None)
            kwargs.pop("progress_color", None)
            kwargs.pop("fg_color", None)
            super().__init__(master, maximum=100, **kwargs)

        def set(self, val: float):
            self["value"] = float(val) * 100

    class CTkSegmentedButtonFallback(tk.Frame):
        def __init__(self, master=None, values=None, variable=None, command=None, **kwargs):
            master = _resolve_master(master)
            bg = getattr(master, "cget", lambda x: "#181825")("bg") if master else "#181825"
            kwargs.pop("selected_color", None)
            kwargs.pop("selected_hover_color", None)
            kwargs.pop("font", None)
            super().__init__(master, bg=bg)
            self.values = values or []
            self.variable = variable or tk.StringVar(value=self.values[0] if self.values else "")
            self.command = command
            self.buttons = {}
            for val in self.values:
                btn = tk.Button(
                    self, text=val, command=lambda v=val: self.set(v),
                    bg="#313244", fg="#cdd6f4", activebackground="#45475a", activeforeground="#cdd6f4",
                    relief="flat", bd=0, padx=10, pady=5
                )
                btn.pack(side="left", fill="x", expand=True, padx=2, pady=2)
                self.buttons[val] = btn
            self._update_styles()

        def set(self, value):
            self.variable.set(value)
            self._update_styles()
            if self.command:
                self.command(value)

        def get(self):
            return self.variable.get()

        def _update_styles(self):
            curr = self.variable.get()
            for val, btn in self.buttons.items():
                if val == curr:
                    btn.configure(bg="#89b4fa", fg="#11111b")
                else:
                    btn.configure(bg="#313244", fg="#cdd6f4")

        def configure(self, **kwargs):
            pass

    class CTkScrollableFrameFallback(tk.Frame):
        def __init__(self, master=None, **kwargs):
            master = _resolve_master(master)
            kwargs.pop("fg_color", None)
            height = kwargs.pop("height", 200)
            bg = getattr(master, "cget", lambda x: "#181825")("bg") if master else "#181825"
            super().__init__(master, bg=bg)
            canvas = tk.Canvas(self, bg=bg, highlightthickness=0, height=height)
            scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
            self.scrollable_frame = tk.Frame(canvas, bg=bg)

            self.scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

    class CTkModuleShim:
        CTk = CTkFallback
        CTkFrame = CTkFrameFallback
        CTkLabel = CTkLabelFallback
        CTkButton = CTkButtonFallback
        CTkEntry = CTkEntryFallback
        CTkCheckBox = CTkCheckBoxFallback
        CTkProgressBar = CTkProgressBarFallback
        CTkSegmentedButton = CTkSegmentedButtonFallback
        CTkScrollableFrame = CTkScrollableFrameFallback
        StringVar = tk.StringVar
        BooleanVar = tk.BooleanVar

        @staticmethod
        def CTkFont(family="Segoe UI", size=12, weight="normal"):
            return (family, size, weight)

        @staticmethod
        def set_appearance_mode(mode):
            pass

        @staticmethod
        def set_default_color_theme(theme):
            pass

    ctk = CTkModuleShim()


# ============================================================================
# 1. DIFF EVALUATION ENGINE & DATA MODELS
# ============================================================================

@dataclass
class Segment:
    text: str
    tag: str  # 'correct', 'wrong', 'missing', 'placeholder'


@dataclass
class DiffResult:
    is_exact: bool
    user_input_raw: str
    target_word_raw: str
    user_segments: List[Segment]
    target_segments: List[Segment]
    accuracy_ratio: float  # 0.0 to 1.0 similarity score
    missing_count: int


def evaluate_answer(user_input: str, target_word: str) -> DiffResult:
    """
    Evaluates user input against target word with character-level alignment.
    Returns DiffResult containing tagged character segments for user input and target word.
    Includes '_' placeholders when user input is shorter than target word.
    """
    user_clean = user_input.strip()
    target_clean = target_word.strip()

    user_norm = user_clean.lower()
    target_norm = target_clean.lower()

    is_exact = (user_norm == target_norm)

    matcher = difflib.SequenceMatcher(None, user_norm, target_norm)
    ratio = matcher.ratio()

    user_segments: List[Segment] = []
    target_segments: List[Segment] = []
    missing_count = 0

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        user_part = user_clean[i1:i2]
        target_part = target_clean[j1:j2]

        if tag == 'equal':
            if user_part:
                user_segments.append(Segment(text=user_part, tag='correct'))
            if target_part:
                target_segments.append(Segment(text=target_part, tag='correct'))
        elif tag == 'replace':
            if user_part:
                user_segments.append(Segment(text=user_part, tag='wrong'))
            if target_part:
                target_segments.append(Segment(text=target_part, tag='missing'))
                missing_count += len(target_part)
        elif tag == 'delete':  # extra characters typed by user
            if user_part:
                user_segments.append(Segment(text=user_part, tag='wrong'))
        elif tag == 'insert':  # missing characters in user input
            if target_part:
                placeholders = " _ " * len(target_part)
                user_segments.append(Segment(text=placeholders, tag='placeholder'))
                target_segments.append(Segment(text=target_part, tag='missing'))
                missing_count += len(target_part)

    return DiffResult(
        is_exact=is_exact,
        user_input_raw=user_clean,
        target_word_raw=target_clean,
        user_segments=user_segments,
        target_segments=target_segments,
        accuracy_ratio=ratio,
        missing_count=missing_count
    )


# ============================================================================
# 2. VOCABULARY DATA REPOSITORY & GENERATOR
# ============================================================================

DEFAULT_VOCABULARY: Dict[str, List[Dict[str, str]]] = {
    "Chapter 1: Basics & Nouns": [
        {"en": "apple", "ua": "яблуко"},
        {"en": "book", "ua": "книга"},
        {"en": "house", "ua": "будинок"},
        {"en": "water", "ua": "вода"},
        {"en": "sun", "ua": "сонце"},
        {"en": "friend", "ua": "друг"},
        {"en": "family", "ua": "сім'я"},
        {"en": "city", "ua": "місто"},
        {"en": "road", "ua": "дорога"},
        {"en": "tree", "ua": "дерево"}
    ],
    "Chapter 2: Verbs & Actions": [
        {"en": "to allow", "ua": "дозволяти"},
        {"en": "to maintain", "ua": "підтримувати"},
        {"en": "to uncover", "ua": "виявляти"},
        {"en": "to retrieve", "ua": "вилучати"},
        {"en": "to exceed", "ua": "перевищувати"},
        {"en": "to represent", "ua": "представляти"},
        {"en": "to differ", "ua": "відрізнятися"},
        {"en": "to enable", "ua": "включати"},
        {"en": "to validate", "ua": "перевіряти"},
        {"en": "to perform", "ua": "виконувати"}
    ],
    "Chapter 3: Adjectives & Descriptions": [
        {"en": "relational", "ua": "реляційний"},
        {"en": "related", "ua": "пов'язаний"},
        {"en": "particular", "ua": "особливий"},
        {"en": "precise", "ua": "точний"},
        {"en": "handy", "ua": "зручний"},
        {"en": "arbitrary", "ua": "довільний"},
        {"en": "ongoing", "ua": "поточний"},
        {"en": "pre-defined", "ua": "заздалегідь визначений"},
        {"en": "opposed", "ua": "протилежний"},
        {"en": "complete", "ua": "повний"}
    ],
    "Chapter 4: Database Concepts": [
        {"en": "durability", "ua": "довговічність"},
        {"en": "scalability", "ua": "масштабованість"},
        {"en": "consistency", "ua": "послідовність"},
        {"en": "integrity", "ua": "цілісність"},
        {"en": "sharding", "ua": "шарування"},
        {"en": "backup", "ua": "резервна копія"},
        {"en": "recovery", "ua": "відновлення"},
        {"en": "rows", "ua": "рядки"},
        {"en": "capabilities", "ua": "можливості"},
        {"en": "completeness", "ua": "повнота"}
    ],
    "Chapter 5: Security & Compliance": [
        {"en": "confidentiality", "ua": "конфіденційність"},
        {"en": "availability", "ua": "доступність"},
        {"en": "authenticity", "ua": "автентичність"},
        {"en": "accountability", "ua": "відповідальність"},
        {"en": "reliability", "ua": "надійність"},
        {"en": "maintainability", "ua": "підтримуваність"},
        {"en": "security", "ua": "безпека"},
        {"en": "validation", "ua": "перевірка"},
        {"en": "compliance", "ua": "дотримання"},
        {"en": "permission", "ua": "дозвіл"}
    ],
    "Chapter 6: System & Infrastructure": [
        {"en": "disaster", "ua": "збій"},
        {"en": "instruction", "ua": "інструкція"},
        {"en": "variable", "ua": "змінна"},
        {"en": "complexity", "ua": "складність"},
        {"en": "performance", "ua": "продуктивність"},
        {"en": "characteristics", "ua": "характеристики"},
        {"en": "features", "ua": "особливості"},
        {"en": "relationships", "ua": "відносини"},
        {"en": "invention", "ua": "винахід"},
        {"en": "introduced", "ua": "введений"}
    ],
    "Chapter 7: Business & Communication": [
        {"en": "agreement", "ua": "угода"},
        {"en": "opportunity", "ua": "можливість"},
        {"en": "challenge", "ua": "виклик"},
        {"en": "solution", "ua": "рішення"},
        {"en": "development", "ua": "розробка"},
        {"en": "management", "ua": "управління"},
        {"en": "resource", "ua": "ресурс"},
        {"en": "objective", "ua": "мета"},
        {"en": "strategy", "ua": "стратегія"},
        {"en": "feedback", "ua": "зворотний зв'язок"}
    ],
    "Chapter 8: Advanced Phrases": [
        {"en": "ongoing field", "ua": "галузь, що розвивається"},
        {"en": "disaster recovery", "ua": "аварійне відновлення"},
        {"en": "data integrity", "ua": "цілісність даних"},
        {"en": "high availability", "ua": "висока доступність"},
        {"en": "scalability requirements", "ua": "вимоги до масштабованості"},
        {"en": "security compliance", "ua": "дотримання безпеки"},
        {"en": "performance optimization", "ua": "оптимізація продуктивності"},
        {"en": "pre-defined structure", "ua": "заздалегідь визначена структура"},
        {"en": "key features", "ua": "ключові особливості"},
        {"en": "arbitrary value", "ua": "довільне значення"}
    ]
}


def load_extra_words_from_txt(txt_path: str) -> List[Dict[str, str]]:
    """Loads English-Ukrainian word pairs from a text file formatted as 'en-ua'."""
    extra = []
    if os.path.exists(txt_path):
        try:
            with open(txt_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if '-' in line:
                        parts = line.split('-', 1)
                        en = parts[0].strip()
                        ua = parts[1].strip()
                        if en and ua:
                            extra.append({"en": en, "ua": ua})
        except Exception as e:
            print(f"Notice: could not parse extra words from {txt_path}: {e}")
    return extra


def generate_words_json(output_path: str = "words.json", source_txt: str = None) -> Dict[str, List[Dict[str, str]]]:
    """Generates words.json with 8 chapters, augmenting with source_txt if available."""
    if not os.path.isabs(output_path):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_dir, output_path)
    data = {k: list(v) for k, v in DEFAULT_VOCABULARY.items()}

    if source_txt and os.path.exists(source_txt):
        extra_words = load_extra_words_from_txt(source_txt)
        if extra_words:
            chapter_keys = list(data.keys())
            for idx, word in enumerate(extra_words):
                chapter_key = chapter_keys[idx % len(chapter_keys)]
                if not any(w['en'].lower() == word['en'].lower() for w in data[chapter_key]):
                    data[chapter_key].append(word)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return data


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
                self.chapters = self._group_flat_list(data)
            else:
                raise ValueError("Invalid JSON format for vocabulary file.")

        except Exception as e:
            print(f"[VocabularyRepository] Error reading {self.json_path}: {e}. Re-generating fallback...")
            generate_words_json(self.json_path)
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self.chapters = json.load(f)

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


# ============================================================================
# 3. GUI COMPONENTS & WIDGETS
# ============================================================================

class DiffFeedbackWidget(ctk.CTkFrame):
    """
    Custom widget displaying character-level diff highlighting using tk.Text widgets.
    Per-character color coding:
      - Green (#2ecc71) for matching characters.
      - Red (#e74c3c) for incorrect/extra characters.
      - Amber (#f59e0b) for missing/expected characters in correct word.
      - Muted Gray (#7f8c8d) for placeholders ('_').
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#1e1e2e", corner_radius=12, border_width=1, border_color="#313244")

        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold")
        )
        self.status_label.pack(anchor="w", padx=16, pady=(12, 6))

        self.user_row = ctk.CTkFrame(self, fg_color="transparent")
        self.user_row.pack(fill="x", padx=16, pady=4)

        self.user_lbl = ctk.CTkLabel(
            self.user_row,
            text="Your Guess:",
            width=120,
            anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#a6adc8"
        )
        self.user_lbl.pack(side="left")

        self.user_text = tk.Text(
            self.user_row,
            height=1.4,
            bg="#181825",
            fg="#cdd6f4",
            relief="flat",
            bd=0,
            highlightthickness=0,
            font=("Segoe UI", 15, "bold"),
            wrap="none"
        )
        self.user_text.pack(side="left", fill="x", expand=True)

        self.target_row = ctk.CTkFrame(self, fg_color="transparent")
        self.target_row.pack(fill="x", padx=16, pady=4)

        self.target_lbl = ctk.CTkLabel(
            self.target_row,
            text="Correct Target:",
            width=120,
            anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#a6adc8"
        )
        self.target_lbl.pack(side="left")

        self.target_text = tk.Text(
            self.target_row,
            height=1.4,
            bg="#181825",
            fg="#cdd6f4",
            relief="flat",
            bd=0,
            highlightthickness=0,
            font=("Segoe UI", 15, "bold"),
            wrap="none"
        )
        self.target_text.pack(side="left", fill="x", expand=True)

        for text_w in (self.user_text, self.target_text):
            text_w.tag_config("correct", foreground="#2ecc71", font=("Segoe UI", 15, "bold"))
            text_w.tag_config("wrong", foreground="#e74c3c", font=("Segoe UI", 15, "bold"))
            text_w.tag_config("missing", foreground="#f59e0b", font=("Segoe UI", 15, "bold", "underline"))
            text_w.tag_config("placeholder", foreground="#7f8c8d", font=("Segoe UI", 15, "bold"))

        self.legend_lbl = ctk.CTkLabel(
            self,
            text="🟢 Correct  |  🔴 Wrong  |  🟡 Missing  |  ⚪ Placeholder (_)",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#6c7086"
        )
        self.legend_lbl.pack(anchor="e", padx=16, pady=(4, 10))

    def display_diff(self, res: DiffResult, attempt_num: int = 1, is_revealed: bool = False) -> None:
        """Renders character diff segments into text widgets."""
        if is_revealed:
            self.status_label.configure(
                text="💡 Solution Revealed:",
                text_color="#f59e0b"
            )
            self.target_lbl.configure(text="Correct Target:")
        elif res.is_exact:
            self.status_label.configure(
                text=f"✓ Perfect! Correct on Attempt #{attempt_num}",
                text_color="#2ecc71"
            )
            self.target_lbl.configure(text="Correct Target:")
        else:
            self.status_label.configure(
                text=f"✕ Keep Trying! Attempt #{attempt_num} - Character Feedback:",
                text_color="#e74c3c"
            )
            self.target_lbl.configure(text="Correct Letters:")

        self.user_text.config(state="normal")
        self.user_text.delete("1.0", "end")
        if not res.user_segments:
            self.user_text.insert("end", "(empty input)", "wrong")
        else:
            for seg in res.user_segments:
                self.user_text.insert("end", seg.text, seg.tag)
        self.user_text.config(state="disabled")

        self.target_text.config(state="normal")
        self.target_text.delete("1.0", "end")
        for seg in res.target_segments:
            if not is_revealed and not res.is_exact and seg.tag in ('missing', 'wrong'):
                masked_text = "_" * len(seg.text)
                self.target_text.insert("end", masked_text, "placeholder")
            else:
                self.target_text.insert("end", seg.text, seg.tag)
        self.target_text.config(state="disabled")


class StartMenuFrame(ctk.CTkFrame):
    """Start Menu Frame for direction & chapter scope selection."""

    def __init__(self, master, repository: VocabularyRepository, on_start_callback):
        super().__init__(master, fg_color="transparent")
        self.repo = repository
        self.on_start_callback = on_start_callback

        self.selected_chapters: Dict[str, ctk.BooleanVar] = {}
        self.direction_var = ctk.StringVar(value="EN->UA")
        self.size_var = ctk.StringVar(value="All")
        self.shuffle_var = ctk.BooleanVar(value=True)

        self.size_seg: ctk.CTkSegmentedButton
        self.start_btn: ctk.CTkButton

        self._build_ui()

    def _build_ui(self):
        content_box = ctk.CTkFrame(self, fg_color="#1e1e2e", corner_radius=16, border_width=1, border_color="#313244")
        content_box.pack(fill="both", expand=True, padx=30, pady=20)

        title_lbl = ctk.CTkLabel(
            content_box,
            text="VocabDrill",
            font=ctk.CTkFont(family="Segoe UI", size=32, weight="bold"),
            text_color="#89b4fa"
        )
        title_lbl.pack(pady=(20, 2))

        subtitle_lbl = ctk.CTkLabel(
            content_box,
            text="Multi-Attempt Vocabulary Drilling with Character-Level Feedback",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color="#a6adc8"
        )
        subtitle_lbl.pack(pady=(0, 20))

        options_grid = ctk.CTkFrame(content_box, fg_color="transparent")
        options_grid.pack(fill="both", expand=True, padx=25, pady=5)

        # Column 1: Direction & Session Settings
        left_col = ctk.CTkFrame(
            options_grid, fg_color="#181825", corner_radius=12, border_width=1, border_color="#313244"
        )
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=5)

        sec1_lbl = ctk.CTkLabel(
            left_col,
            text="1. PRACTICE DIRECTION",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color="#cdd6f4"
        )
        sec1_lbl.pack(anchor="w", padx=16, pady=(16, 10))

        dir_seg = ctk.CTkSegmentedButton(
            left_col,
            values=["English ➔ Ukrainian", "Ukrainian ➔ English"],
            variable=self.direction_var,
            selected_color="#89b4fa",
            selected_hover_color="#b4befe",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        )
        dir_seg.set("English ➔ Ukrainian")
        dir_seg.pack(fill="x", padx=16, pady=5)

        sec_limit_lbl = ctk.CTkLabel(
            left_col,
            text="2. SESSION SIZE",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color="#cdd6f4"
        )
        sec_limit_lbl.pack(anchor="w", padx=16, pady=(20, 10))

        self.size_seg = ctk.CTkSegmentedButton(
            left_col,
            values=["10 Cards", "20 Cards", "50 Cards", "All Words"],
            font=ctk.CTkFont(family="Segoe UI", size=12)
        )
        self.size_seg.set("All Words")
        self.size_seg.pack(fill="x", padx=16, pady=5)

        shuffle_chk = ctk.CTkCheckBox(
            left_col,
            text="Randomize card order",
            variable=self.shuffle_var,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#bac2de"
        )
        shuffle_chk.pack(anchor="w", padx=16, pady=(20, 10))

        # Column 2: Scope & Chapters Selection
        right_col = ctk.CTkFrame(
            options_grid, fg_color="#181825", corner_radius=12, border_width=1, border_color="#313244"
        )
        right_col.pack(side="right", fill="both", expand=True, padx=(10, 0), pady=5)

        sec2_header = ctk.CTkFrame(right_col, fg_color="transparent")
        sec2_header.pack(fill="x", padx=16, pady=(16, 5))

        sec2_lbl = ctk.CTkLabel(
            sec2_header,
            text="3. CHAPTER SCOPE SELECTION",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color="#cdd6f4"
        )
        sec2_lbl.pack(side="left")

        btn_box = ctk.CTkFrame(sec2_header, fg_color="transparent")
        btn_box.pack(side="right")

        btn_all = ctk.CTkButton(
            btn_box,
            text="All",
            width=45,
            height=24,
            fg_color="#313244",
            hover_color="#45475a",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            command=self.select_all_chapters
        )
        btn_all.pack(side="left", padx=2)

        btn_none = ctk.CTkButton(
            btn_box,
            text="None",
            width=45,
            height=24,
            fg_color="#313244",
            hover_color="#45475a",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            command=self.deselect_all_chapters
        )
        btn_none.pack(side="left", padx=2)

        chapters_scroll = ctk.CTkScrollableFrame(right_col, fg_color="transparent", height=200)
        chapters_scroll.pack(fill="both", expand=True, padx=12, pady=5)

        chapter_counts = self.repo.get_chapter_counts()
        for ch_name, count in chapter_counts.items():
            var = ctk.BooleanVar(value=True)
            self.selected_chapters[ch_name] = var

            chk = ctk.CTkCheckBox(
                chapters_scroll,
                text=f"{ch_name}  ({count} words)",
                variable=var,
                command=self.update_start_button_state,
                font=ctk.CTkFont(family="Segoe UI", size=13),
                text_color="#cdd6f4"
            )
            chk.pack(anchor="w", padx=8, pady=6)

        self.start_btn = ctk.CTkButton(
            content_box,
            text="🚀 Start Practice",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            fg_color="#a6e3a1",
            hover_color="#94e2d5",
            text_color="#11111b",
            height=50,
            corner_radius=12,
            command=self._on_start_clicked
        )
        self.start_btn.pack(fill="x", padx=25, pady=(15, 20))

        self.update_start_button_state()

    def select_all_chapters(self):
        for var in self.selected_chapters.values():
            var.set(True)
        self.update_start_button_state()

    def deselect_all_chapters(self):
        for var in self.selected_chapters.values():
            var.set(False)
        self.update_start_button_state()

    def update_start_button_state(self):
        chosen = [ch for ch, var in self.selected_chapters.items() if var.get()]
        counts = self.repo.get_chapter_counts()
        total_selected = sum(counts[ch] for ch in chosen if ch in counts)

        if total_selected == 0:
            self.start_btn.configure(
                state="disabled",
                text="Select At Least 1 Chapter to Start",
                fg_color="#45475a"
            )
        else:
            self.start_btn.configure(
                state="normal",
                text=f"🚀 Start Practice ({total_selected} Words Available)",
                fg_color="#a6e3a1",
                text_color="#11111b"
            )

    def _on_start_clicked(self):
        chosen_ch = [ch for ch, var in self.selected_chapters.items() if var.get()]
        dir_val = "EN->UA" if "English" in self.direction_var.get() else "UA->EN"

        size_str = self.size_seg.get()
        max_w = None
        if "10" in size_str:
            max_w = 10
        elif "20" in size_str:
            max_w = 20
        elif "50" in size_str:
            max_w = 50

        deck = self.repo.create_session_deck(
            selected_chapters=chosen_ch,
            direction=dir_val,
            shuffle=self.shuffle_var.get(),
            max_words=max_w
        )

        self.on_start_callback(deck)


class FlashcardFrame(ctk.CTkFrame):
    """Multi-Attempt Flashcard Practice Screen."""

    def __init__(self, master, on_back_callback):
        super().__init__(master, fg_color="transparent")
        self.on_back_callback = on_back_callback

        self.deck: List[Flashcard] = []
        self.current_idx: int = 0
        self.correct_count: int = 0
        self.incorrect_count: int = 0
        self.skipped_count: int = 0

        self.card_attempts: int = 0
        self.card_revealed: bool = False
        self.is_auto_advancing: bool = False
        self.current_card: Optional[Flashcard] = None

        self.chapter_badge: ctk.CTkLabel
        self.correct_badge: ctk.CTkLabel
        self.incorrect_badge: ctk.CTkLabel
        self.accuracy_badge: ctk.CTkLabel
        self.card_count_lbl: ctk.CTkLabel
        self.progress_bar: ctk.CTkProgressBar
        self.lang_pill: ctk.CTkLabel
        self.prompt_lbl: ctk.CTkLabel
        self.entry: ctk.CTkEntry
        self.giveup_btn: ctk.CTkButton
        self.skip_btn: ctk.CTkButton
        self.action_btn: ctk.CTkButton
        self.diff_widget: DiffFeedbackWidget

        self._build_ui()

    def _build_ui(self):
        hud_bar = ctk.CTkFrame(self, fg_color="#1e1e2e", corner_radius=12, border_width=1, border_color="#313244")
        hud_bar.pack(fill="x", padx=20, pady=(15, 10))

        back_btn = ctk.CTkButton(
            hud_bar,
            text="⬅ Menu",
            width=80,
            height=32,
            fg_color="#313244",
            hover_color="#45475a",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=self._on_back_clicked
        )
        back_btn.pack(side="left", padx=12, pady=10)

        self.chapter_badge = ctk.CTkLabel(
            hud_bar,
            text="Chapter",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#a6adc8"
        )
        self.chapter_badge.pack(side="left", padx=10)

        score_box = ctk.CTkFrame(hud_bar, fg_color="transparent")
        score_box.pack(side="right", padx=12)

        self.correct_badge = ctk.CTkLabel(
            score_box, text="✓ 0",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#2ecc71"
        )
        self.correct_badge.pack(side="left", padx=8)

        self.incorrect_badge = ctk.CTkLabel(
            score_box, text="✕ 0",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#e74c3c"
        )
        self.incorrect_badge.pack(side="left", padx=8)

        self.accuracy_badge = ctk.CTkLabel(
            score_box, text="🎯 0%",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#89b4fa"
        )
        self.accuracy_badge.pack(side="left", padx=8)

        prog_box = ctk.CTkFrame(self, fg_color="transparent")
        prog_box.pack(fill="x", padx=25, pady=(2, 10))

        self.card_count_lbl = ctk.CTkLabel(
            prog_box, text="Card 0 / 0",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#cdd6f4"
        )
        self.card_count_lbl.pack(side="left", padx=(0, 10))

        self.progress_bar = ctk.CTkProgressBar(
            prog_box, height=10, corner_radius=5,
            progress_color="#89b4fa", fg_color="#313244"
        )
        self.progress_bar.pack(side="left", fill="x", expand=True)
        self.progress_bar.set(0)

        card_container = ctk.CTkFrame(self, fg_color="#181825", corner_radius=16, border_width=1, border_color="#313244")
        card_container.pack(fill="both", expand=True, padx=20, pady=5)

        self.lang_pill = ctk.CTkLabel(
            card_container, text="ENGLISH PROMPT",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#89b4fa"
        )
        self.lang_pill.pack(pady=(16, 2))

        self.prompt_lbl = ctk.CTkLabel(
            card_container, text="Target Word",
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color="#cdd6f4"
        )
        self.prompt_lbl.pack(pady=(5, 15))

        entry_frame = ctk.CTkFrame(card_container, fg_color="transparent")
        entry_frame.pack(fill="x", padx=40, pady=5)

        self.entry = ctk.CTkEntry(
            entry_frame,
            placeholder_text="Type answer and press Enter...",
            height=50,
            font=ctk.CTkFont(family="Segoe UI", size=18),
            corner_radius=10,
            border_width=2,
            border_color="#45475a",
            fg_color="#1e1e2e"
        )
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", self._on_enter_pressed)

        controls_box = ctk.CTkFrame(card_container, fg_color="transparent")
        controls_box.pack(fill="x", padx=40, pady=10)

        self.giveup_btn = ctk.CTkButton(
            controls_box,
            text="💡 Reveal Solution",
            width=140, height=40,
            fg_color="#d97706", hover_color="#f59e0b",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            command=self._on_giveup_clicked
        )
        self.giveup_btn.pack(side="left", padx=(0, 10))

        self.skip_btn = ctk.CTkButton(
            controls_box, text="Skip Card ➔",
            width=110, height=40,
            fg_color="#313244", hover_color="#45475a",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            command=self._on_skip_clicked
        )
        self.skip_btn.pack(side="left")

        self.action_btn = ctk.CTkButton(
            controls_box, text="Check Answer ↵",
            height=40,
            fg_color="#89b4fa", hover_color="#b4befe",
            text_color="#11111b",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            command=self._on_action_clicked
        )
        self.action_btn.pack(side="right", fill="x", expand=True, padx=(15, 0))

        self.diff_widget = DiffFeedbackWidget(card_container)

    def start_session(self, deck: List[Flashcard]):
        """Initializes a new practice session with the provided deck."""
        self.deck = deck
        self.current_idx = 0
        self.correct_count = 0
        self.incorrect_count = 0
        self.skipped_count = 0

        self.diff_widget.pack_forget()

        if not self.deck:
            self._on_back_clicked()
            return

        self._load_current_card()

    def _load_current_card(self):
        if self.current_idx >= len(self.deck):
            self._finish_session()
            return

        self.card_attempts = 0
        self.card_revealed = False
        self.is_auto_advancing = False
        self.current_card = self.deck[self.current_idx]

        self.entry.delete(0, "end")
        self.entry.configure(state="normal", border_color="#45475a")
        self.diff_widget.pack_forget()
        self.entry.focus_set()

        dir_text = "TRANSLATE TO UKRAINIAN" if self.current_card.direction == "EN->UA" else "TRANSLATE TO ENGLISH"
        self.lang_pill.configure(text=dir_text)
        self.prompt_lbl.configure(text=self.current_card.prompt)
        self.chapter_badge.configure(text=self.current_card.chapter)

        total = len(self.deck)
        current_num = self.current_idx + 1
        self.card_count_lbl.configure(text=f"Card {current_num} / {total}")
        self.progress_bar.set(current_num / total)

        self._update_score_hud()

        self.giveup_btn.configure(state="normal")
        self.skip_btn.configure(state="normal")
        self.action_btn.configure(
            text="Check Answer ↵",
            fg_color="#89b4fa",
            text_color="#11111b",
            state="normal"
        )

    def _update_score_hud(self):
        self.correct_badge.configure(text=f"✓ {self.correct_count}")
        self.incorrect_badge.configure(text=f"✕ {self.incorrect_count}")

        total_answered = self.correct_count + self.incorrect_count
        acc = int((self.correct_count / total_answered) * 100) if total_answered > 0 else 0
        self.accuracy_badge.configure(text=f"🎯 {acc}%")

    def _on_enter_pressed(self, event=None):
        self._on_action_clicked()

    def _on_action_clicked(self):
        if self.is_auto_advancing:
            return

        if self.card_revealed:
            self._advance_to_next_card()
            return

        user_input = self.entry.get()
        if not self.current_card:
            return

        self.card_attempts += 1
        res = evaluate_answer(user_input, self.current_card.target)

        self.diff_widget.display_diff(res, attempt_num=self.card_attempts)
        self.diff_widget.pack(fill="x", padx=20, pady=(5, 15))

        if res.is_exact:
            self.correct_count += 1
            self._update_score_hud()

            self.entry.configure(border_color="#2ecc71", state="disabled")
            self.action_btn.configure(
                text="✓ Correct! Advancing...",
                fg_color="#2ecc71",
                text_color="#11111b",
                state="disabled"
            )

            self.is_auto_advancing = True
            self.after(750, self._advance_to_next_card)
        else:
            self.entry.configure(border_color="#e74c3c")
            self.entry.focus_set()

    def _on_giveup_clicked(self):
        if not self.current_card or self.card_revealed:
            return

        self.card_revealed = True
        self.incorrect_count += 1
        self._update_score_hud()

        user_input = self.entry.get()
        res = evaluate_answer(user_input, self.current_card.target)
        self.diff_widget.display_diff(res, is_revealed=True)
        self.diff_widget.pack(fill="x", padx=20, pady=(5, 15))

        self.entry.configure(border_color="#f59e0b", state="disabled")
        self.action_btn.configure(
            text="Next Card ➔ (Press Enter)",
            fg_color="#f59e0b",
            text_color="#11111b",
            state="normal"
        )
        self.action_btn.focus_set()

    def _on_skip_clicked(self):
        self.skipped_count += 1
        self._advance_to_next_card()

    def _advance_to_next_card(self):
        self.current_idx += 1
        self._load_current_card()

    def _on_back_clicked(self):
        self.on_back_callback()

    def _finish_session(self):
        app_instance = cast("VocabDrillApp", self.winfo_toplevel())
        app_instance.show_summary(
            total=len(self.deck),
            correct=self.correct_count,
            incorrect=self.incorrect_count,
            skipped=self.skipped_count
        )


class SummaryFrame(ctk.CTkFrame):
    """Session summary frame showing final statistics and options to restart or menu."""

    def __init__(self, master, on_menu_callback, on_restart_callback):
        super().__init__(master, fg_color="transparent")
        self.on_menu_callback = on_menu_callback
        self.on_restart_callback = on_restart_callback

        self.acc_lbl: ctk.CTkLabel
        self.details_lbl: ctk.CTkLabel

        self._build_ui()

    def _build_ui(self):
        box = ctk.CTkFrame(self, fg_color="#1e1e2e", corner_radius=16, border_width=1, border_color="#313244")
        box.pack(fill="both", expand=True, padx=40, pady=30)

        title = ctk.CTkLabel(
            box,
            text="🎉 Practice Session Complete!",
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color="#a6e3a1"
        )
        title.pack(pady=(30, 10))

        self.acc_lbl = ctk.CTkLabel(
            box,
            text="Accuracy: 0%",
            font=ctk.CTkFont(family="Segoe UI", size=36, weight="bold"),
            text_color="#89b4fa"
        )
        self.acc_lbl.pack(pady=10)

        stats_grid = ctk.CTkFrame(box, fg_color="#181825", corner_radius=12)
        stats_grid.pack(fill="x", padx=50, pady=15)

        self.details_lbl = ctk.CTkLabel(
            stats_grid,
            text="Total Cards: 0  |  Correct: 0  |  Incorrect: 0  |  Skipped: 0",
            font=ctk.CTkFont(family="Segoe UI", size=15),
            text_color="#cdd6f4"
        )
        self.details_lbl.pack(pady=16)

        btn_row = ctk.CTkFrame(box, fg_color="transparent")
        btn_row.pack(pady=(20, 30))

        btn_menu = ctk.CTkButton(
            btn_row,
            text="Main Menu",
            width=140,
            height=45,
            fg_color="#313244",
            hover_color="#45475a",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            command=self.on_menu_callback
        )
        btn_menu.pack(side="left", padx=10)

        btn_again = ctk.CTkButton(
            btn_row,
            text="Practice Again",
            width=160,
            height=45,
            fg_color="#a6e3a1",
            hover_color="#94e2d5",
            text_color="#11111b",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            command=self.on_restart_callback
        )
        btn_again.pack(side="left", padx=10)

    def set_summary(self, total: int, correct: int, incorrect: int, skipped: int):
        answered = correct + incorrect
        acc = int((correct / answered) * 100) if answered > 0 else 0

        self.acc_lbl.configure(text=f"Accuracy: {acc}%")
        self.details_lbl.configure(
            text=f"Total Cards: {total}   |   ✓ Correct: {correct}   |   ✕ Incorrect: {incorrect}   |   ⏭ Skipped: {skipped}"
        )


class VocabDrillApp(ctk.CTk):
    """Main Application Window."""

    def __init__(self):
        super().__init__()

        self.title("VocabDrill - Multi-Attempt Vocabulary Drilling")
        self.geometry("960x700")
        self.minsize(880, 620)

        self.repository = VocabularyRepository("words.json")
        self.last_deck: List[Flashcard] = []

        self.start_menu_frame: StartMenuFrame
        self.flashcard_frame: FlashcardFrame
        self.summary_frame: SummaryFrame

        self._build_views()
        self.show_start_menu()

    def _build_views(self):
        self.start_menu_frame = StartMenuFrame(
            self,
            repository=self.repository,
            on_start_callback=self.start_practice
        )

        self.flashcard_frame = FlashcardFrame(
            self,
            on_back_callback=self.show_start_menu
        )

        self.summary_frame = SummaryFrame(
            self,
            on_menu_callback=self.show_start_menu,
            on_restart_callback=self.restart_practice
        )

    def show_start_menu(self):
        self.flashcard_frame.pack_forget()
        self.summary_frame.pack_forget()
        self.start_menu_frame.pack(fill="both", expand=True)

    def start_practice(self, deck: List[Flashcard]):
        self.last_deck = deck
        self.start_menu_frame.pack_forget()
        self.summary_frame.pack_forget()
        self.flashcard_frame.pack(fill="both", expand=True)
        self.flashcard_frame.start_session(deck)

    def restart_practice(self):
        if self.last_deck:
            self.start_practice(list(self.last_deck))
        else:
            self.show_start_menu()

    def show_summary(self, total: int, correct: int, incorrect: int, skipped: int):
        self.flashcard_frame.pack_forget()
        self.start_menu_frame.pack_forget()
        self.summary_frame.set_summary(total, correct, incorrect, skipped)
        self.summary_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = VocabDrillApp()
    app.mainloop()
