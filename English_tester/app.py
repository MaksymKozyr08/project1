"""
app.py - Unified Desktop GUI Application for Vocabulary Flashcard Drilling.

Features:
- Scientific & Rigorous Laboratory-grade UI Design.
- Multi-Attempt Vocabulary Drilling with Character-Level Alignment & Diff Metrics.
- Granular Lexical Selection: Select/deselect specific words from every chapter/block.
- Robust Hint, Reveal, and Skip mechanisms with auto-cleared input vectors.
- Bilingual Ukrainian/English interface with linguistic classification tags.
- High-performance lazy rendering supporting 3,000+ words.
- Automatic CustomTkinter support with seamless standard Tkinter fallback.
"""

import json
import os
import random
import difflib
import re
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
    print(" Falling back to standard Tkinter interface with dark scientific theme...")
    print(" To enable modern CustomTkinter widgets: pip install customtkinter")
    print("=" * 70 + "\n")

    def _resolve_master(master):
        if hasattr(master, "scrollable_frame"):
            return master.scrollable_frame
        return master

    class CTkFallback(tk.Tk):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.configure(bg="#0b0f19")

    class CTkFrameFallback(tk.Frame):
        def __init__(self, master=None, **kwargs):
            master = _resolve_master(master)
            fg_color = kwargs.pop("fg_color", None)
            kwargs.pop("corner_radius", None)
            border_width = kwargs.pop("border_width", None)
            border_color = kwargs.pop("border_color", None)
            if fg_color is not None:
                if fg_color == "transparent":
                    bg = getattr(master, "cget", lambda x: "#0b0f19")("bg") if master else "#0b0f19"
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
                    kwargs["bg"] = getattr(self.master, "cget", lambda x: "#0b0f19")("bg")
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
                kwargs["bg"] = getattr(master, "cget", lambda x: "#0b0f19")("bg") if master else "#0b0f19"
            super().__init__(master, **kwargs)

        def configure(self, **kwargs):
            text_color = kwargs.pop("text_color", None)
            fg_color = kwargs.pop("fg_color", None)
            kwargs.pop("font", None)
            if text_color:
                kwargs["fg"] = text_color
            if fg_color:
                kwargs["bg"] = fg_color if fg_color != "transparent" else getattr(self.master, "cget", lambda x: "#0b0f19")("bg")
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
                kwargs["insertbackground"] = "#f8fafc"
                kwargs["fg"] = "#f8fafc"
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
            self._variable = kwargs.get("variable", None)
            if text_color:
                kwargs["fg"] = text_color
            bg = getattr(master, "cget", lambda x: "#0b0f19")("bg") if master else "#0b0f19"
            kwargs.setdefault("bg", bg)
            kwargs.setdefault("activebackground", bg)
            kwargs.setdefault("activeforeground", text_color or "#f8fafc")
            kwargs.setdefault("selectcolor", "#1e293b")
            super().__init__(master, **kwargs)

        def get(self):
            if self._variable is not None:
                return self._variable.get()
            return 1

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
            bg = getattr(master, "cget", lambda x: "#0b0f19")("bg") if master else "#0b0f19"
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
                    bg="#1e293b", fg="#f8fafc", activebackground="#334155", activeforeground="#f8fafc",
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
                    btn.configure(bg="#38bdf8", fg="#0b0f19")
                else:
                    btn.configure(bg="#1e293b", fg="#f8fafc")

        def configure(self, **kwargs):
            pass

    class CTkScrollableFrameFallback(tk.Frame):
        def __init__(self, master=None, **kwargs):
            master = _resolve_master(master)
            kwargs.pop("fg_color", None)
            height = kwargs.pop("height", 200)
            bg = getattr(master, "cget", lambda x: "#0b0f19")("bg") if master else "#0b0f19"
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
# SCIENTIFIC DESIGN PALETTE (ACADEMIC SLATE & CYAN)
# ============================================================================
PALETTE = {
    "bg_main": "#0b0f19",       # Deep scientific slate
    "bg_surface": "#111827",    # Panel slate
    "bg_card": "#1e293b",       # Card container
    "bg_inner": "#0f172a",      # Recessed input / well
    "border": "#334155",        # Slate border
    "border_focus": "#38bdf8",  # Scientific cyan focus
    "accent_primary": "#38bdf8",# Cyan / Sky
    "accent_hover": "#7dd3fc",
    "accent_secondary": "#818cf8", # Indigo / violet
    "success": "#10b981",       # Emerald green
    "success_hover": "#34d399",
    "error": "#ef4444",         # Red
    "warning": "#f59e0b",       # Amber
    "text_primary": "#f8fafc",  # White
    "text_secondary": "#94a3b8",# Slate gray
    "text_dim": "#64748b",      # Muted slate
}


# ============================================================================
# 1. DIFF EVALUATION ENGINE & LINGUISTIC PARSER
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
    matching_count: int
    wrong_count: int
    all_variants: List[str]


def parse_pos_tag(word_str: str) -> Tuple[str, str]:
    """
    Extracts grammatical part-of-speech classification from word prompt if present.
    Returns: (cleaned_word, pos_label)
    e.g. 'aim (n)' -> ('aim', 'NOUN')
         'comment (v)' -> ('comment', 'VERB')
         'to maintain' -> ('to maintain', 'VERBAL PHRASE')
    """
    raw = word_str.strip()
    pos = ""
    match = re.search(r'\((n|v|adj|adv|phr|prep)\b.*?\)', raw, re.IGNORECASE)
    if match:
        tag = match.group(1).lower()
        tag_map = {
            "n": "NOUN",
            "v": "VERB",
            "adj": "ADJECTIVE",
            "adv": "ADVERB",
            "phr": "PHRASE",
            "prep": "PREPOSITION"
        }
        pos = tag_map.get(tag, tag.upper())
    elif raw.lower().startswith("to ") and len(raw) > 3:
        pos = "VERBAL PHRASE"
    return raw, pos


def _evaluate_single(user_clean: str, target_clean: str, all_variants: List[str]) -> DiffResult:
    """Evaluates user input against a single concrete target string with character-level alignment."""
    user_norm = user_clean.lower()
    target_norm = target_clean.lower()

    is_exact = (user_norm == target_norm)

    matcher = difflib.SequenceMatcher(None, user_norm, target_norm)
    ratio = matcher.ratio()

    user_segments: List[Segment] = []
    target_segments: List[Segment] = []
    missing_count = 0
    matching_count = 0
    wrong_count = 0

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        user_part = user_clean[i1:i2]
        target_part = target_clean[j1:j2]

        if tag == 'equal':
            if user_part:
                user_segments.append(Segment(text=user_part, tag='correct'))
                matching_count += len(user_part)
            if target_part:
                target_segments.append(Segment(text=target_part, tag='correct'))
        elif tag == 'replace':
            if user_part:
                user_segments.append(Segment(text=user_part, tag='wrong'))
                wrong_count += len(user_part)
            if target_part:
                target_segments.append(Segment(text=target_part, tag='missing'))
                missing_count += len(target_part)
        elif tag == 'delete':
            if user_part:
                user_segments.append(Segment(text=user_part, tag='wrong'))
                wrong_count += len(user_part)
        elif tag == 'insert':
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
        missing_count=missing_count,
        matching_count=matching_count,
        wrong_count=wrong_count,
        all_variants=all_variants
    )


def get_target_variants(target_str: str) -> List[str]:
    """
    Parses a target string containing alternative answers ('/' or ',')
    and parenthetical annotations. Returns list of accepted answer variants.
    """
    if not target_str:
        return []

    raw = target_str.strip()
    parts = [p.strip() for p in raw.split('/') if p.strip()]
    if not parts:
        parts = [raw]

    variants: List[str] = []
    seen: Set[str] = set()

    def add_var(v: str):
        cleaned = re.sub(r'\s+', ' ', v.strip())
        if cleaned:
            norm = cleaned.lower()
            if norm not in seen:
                seen.add(norm)
                variants.append(cleaned)

    for p in parts:
        sub_parts = [sp.strip() for sp in p.split(',') if sp.strip()]
        for sp in sub_parts:
            # 1) Variant without parentheses: e.g. "приміряти" from "приміряти (одяг)"
            no_paren = re.sub(r'\(.*?\)', '', sp).strip()
            if no_paren:
                add_var(no_paren)
            # 2) Full part
            add_var(sp)
            # 3) English verbs starting with "to "
            if sp.lower().startswith('to ') and len(sp) > 3:
                add_var(sp[3:].strip())

    add_var(raw)
    return variants


def evaluate_answer(user_input: str, target_word: str) -> DiffResult:
    """Evaluates user input against valid target variants with scientific similarity scoring."""
    user_clean = user_input.strip()
    user_norm = user_clean.lower()

    variants = get_target_variants(target_word)
    if not variants:
        variants = [target_word.strip()]

    # Check exact match against any valid variant
    for v in variants:
        if user_norm == v.lower():
            res = _evaluate_single(user_clean, v, variants)
            res.target_word_raw = v
            return res

    # Otherwise find closest candidate
    candidates = variants[:-1] if len(variants) > 1 else variants
    best_variant = candidates[0]
    best_ratio = -1.0

    for v in candidates:
        ratio = difflib.SequenceMatcher(None, user_norm, v.lower()).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_variant = v

    res = _evaluate_single(user_clean, best_variant, variants)
    res.target_word_raw = best_variant
    return res


# ============================================================================
# 2. VOCABULARY DATA REPOSITORY
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
    ]
}


def generate_words_json(output_path: str = "words.json") -> Dict[str, List[Dict[str, str]]]:
    """Generates words.json fallback template."""
    if not os.path.isabs(output_path):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_dir, os.path.basename(output_path))
    data = {k: list(v) for k, v in DEFAULT_VOCABULARY.items()}
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return data


@dataclass
class Flashcard:
    prompt: str
    target: str
    direction: str  # 'EN->UA' or 'UA->EN'
    chapter: str
    pos_tag: str
    original_pair: Dict[str, str]
    mode: str = "word"  # 'word' or 'sentence'
    source_sentence: str = ""
    target_sentence_cloze: str = ""
    target_sentence_full: str = ""


CURATED_SENTENCES: Dict[str, Tuple[str, str]] = {
    "apple": ("She ate a sweet red apple after lunch.", "Вона з'їла солодке червоне яблуко після обіду."),
    "book": ("I am reading a fascinating book about history.", "Я читаю захоплюючу книгу про історію."),
    "house": ("They built a modern house near the forest.", "Вони побудували сучасний будинок біля лісу."),
    "water": ("Fresh drinking water is vital for human health.", "Свіжа питна вода життєво необхідна для здоров'я."),
    "sun": ("The morning sun was shining brightly in the sky.", "Ранкове сонце яскраво світило в небі."),
    "friend": ("A loyal friend will always support you in difficult times.", "Вірний друг завжди підтримає тебе у скрутну хвилину."),
    "family": ("Spending quality time with family is very important.", "Проводити якісний час із сім'єю дуже важливо."),
    "city": ("Kyiv is a vibrant and historic European city.", "Київ — жваве та історичне європейське місто."),
    "road": ("The winding road led through scenic mountains.", "Звивиста дорога вела крізь мальовничі гори."),
    "tree": ("An ancient oak tree stood in the middle of the park.", "Стародавнє дерево стояло посеред парку."),
    "actual": ("The actual results exceeded our initial expectations.", "Фактичні результати перевершили наші початкові очікування."),
    "actually": ("I thought it would rain, but it was actually sunny.", "Я думав, що піде дощ, але насправді було сонячно."),
    "admire": ("We sincerely admire your dedication and hard work.", "Ми щиро захоплюємося вашою відданістю та наполегливою працею."),
    "accent": ("He speaks English fluently with a slight French accent.", "Він вільно говорить англійською з легким французьким акцентом."),
    "apartment": ("They recently rented a cozy apartment downtown.", "Нещодавно вони орендували затишну квартиру в центрі міста."),
    "awesome": ("The live performance was absolutely awesome.", "Живий виступ був просто неймовірний."),
    "abroad": ("Many students dream of studying abroad for a semester.", "Багато студентів мріють навчатися за кордоном протягом семестру."),
    "advantage": ("Having strong communication skills is a huge advantage.", "Володіння сильними комунікативними навичками є величезною перевагою."),
    "allow": ("The new security rules allow authorized access only.", "Нові правила безпеки дозволяють доступ лише авторизованим користувачам."),
    "to allow": ("The new security rules allow authorized access only.", "Нові правила безпеки дозволяють доступ лише авторизованим користувачам."),
    "maintain": ("Engineers must maintain database integrity at all times.", "Інженери повинні підтримувати цілісність бази даних повсякчас."),
    "to maintain": ("Engineers must maintain database integrity at all times.", "Інженери повинні підтримувати цілісність бази даних повсякчас."),
    "durability": ("ACID transactions guarantee durability during power failures.", "ACID транзакції гарантують довговічність під час збоїв живлення."),
    "scalability": ("Horizontal sharding provides high scalability for massive workloads.", "Горизонтальне шарування забезпечує високу масштабованість для великих навантажень."),
    "consistency": ("Eventual consistency is widely used in distributed caches.", "Кінцева послідовність широко використовується у розподілених кешах."),
    "integrity": ("Referential integrity prevents orphan records in relational tables.", "Референційна цілісність запобігає появі осиротілих записів у таблицях."),
    "sharding": ("Database sharding splits heavy tables across cluster nodes.", "Шарування баз даних розділяє великі таблиці між вузлами кластера."),
    "backup": ("Always create an automated daily backup of critical files.", "Завжди створюйте автоматичну щоденну резервну копію важливих файлів."),
    "recovery": ("A solid disaster recovery plan ensures business continuity.", "Надійний план аварійного відновлення забезпечує безперервність бізнесу."),
    "security": ("Multi-factor authentication improves account security.", "Багатофакторна автентифікація покращує безпеку облікового запису."),
    "solution": ("Developers implemented an elegant solution to the latency issue.", "Розробники впровадили елегантне рішення проблеми із затримкою."),
    "strategy": ("A clear testing strategy reduces software bugs significantly.", "Чітка стратегія тестування суттєво зменшує кількість помилок."),
    "performance": ("Indexing frequently queried columns maximizes search performance.", "Індексування часто запитуваних колонок максимізує продуктивність пошуку."),
    "compliance": ("Regular system audits guarantee strict compliance with industry standards.", "Регулярні аудити гарантують суворе дотримання галузевих стандартів."),
    "challenge": ("Refactoring legacy systems presents a formidable technical challenge.", "Рефакторинг застарілих систем становить серйозний технічний виклик."),
    "opportunity": ("Artificial intelligence provides a tremendous opportunity for growth.", "Штучний інтелект надає колосальну можливість для зростання."),
    "permission": ("The administrator granted write permission to the team directory.", "Адміністратор надав дозвіл на запис у директорію команди.")
}


def get_context_sentences(en_raw: str, ua_raw: str, direction: str) -> Tuple[str, str, str]:
    """
    Constructs contextual sentences:
    Returns (source_sentence, target_sentence_cloze, target_sentence_full).
    """
    en_clean = re.sub(r'\(.*?\)', '', en_raw).strip()
    ua_clean = re.sub(r'\(.*?\)', '', ua_raw).split('/')[0].strip()

    base_en = en_clean[3:].strip() if en_clean.lower().startswith("to ") else en_clean
    key_en = base_en.lower()

    if key_en in CURATED_SENTENCES:
        en_s, ua_s = CURATED_SENTENCES[key_en]
    elif en_clean.lower() in CURATED_SENTENCES:
        en_s, ua_s = CURATED_SENTENCES[en_clean.lower()]
    else:
        _, pos = parse_pos_tag(en_raw)
        if pos in ("VERB", "VERBAL PHRASE") or "(v)" in en_raw.lower() or en_clean.lower().startswith("to "):
            en_s = f"It is very important to {base_en} these project requirements carefully."
            ua_s = f"Дуже важливо ретельно {ua_clean} ці вимоги проєкту."
        elif pos == "ADJECTIVE" or "(adj)" in en_raw.lower() or any(en_clean.lower().endswith(s) for s in ("able", "ible", "al", "ic", "ive", "ous", "ed")):
            en_s = f"The team presented an {en_clean} demonstration during the technical review."
            ua_s = f"Команда представила {ua_clean} демонстрацію під час технічного огляду."
        elif pos == "ADVERB" or "(adv)" in en_raw.lower() or en_clean.lower().endswith("ly"):
            en_s = f"The software {en_clean} processed the incoming network request."
            ua_s = f"Програмне забезпечення {ua_clean} обробило вхідний мережевий запит."
        elif " " in en_clean:
            en_s = f"Modern high-tech systems strongly emphasize {en_clean}."
            ua_s = f"Сучасні високотехнологічні системи значно наголошують на {ua_clean}."
        else:
            en_s = f"We observed that the {en_clean} played a significant role in this task."
            ua_s = f"Ми помітили, що цей {ua_clean} відіграв значну роль у цьому завданні."

    def mask_word(sent: str, target_w: str) -> Tuple[str, str]:
        # Try direct case-insensitive match
        pat = re.compile(r'\b' + re.escape(target_w) + r'\b', re.IGNORECASE)
        m = pat.search(sent)
        if m:
            matched_text = m.group(0)
            cloze = pat.sub("[ _______ ]", sent, count=1)
            full = pat.sub(f"[ {matched_text} ]", sent, count=1)
            return cloze, full

        # Try stem match (for inflected Ukrainian endings)
        if len(target_w) > 4:
            stem = target_w[:-2]
            pat_stem = re.compile(r'\b' + re.escape(stem) + r'\w*', re.IGNORECASE)
            m_stem = pat_stem.search(sent)
            if m_stem:
                matched_text = m_stem.group(0)
                cloze = pat_stem.sub("[ _______ ]", sent, count=1)
                full = pat_stem.sub(f"[ {matched_text} ]", sent, count=1)
                return cloze, full

        # Fallback
        return f"{sent} [ _______ ]", f"{sent} [ {target_w} ]"

    if direction == "UA->EN":
        # Target language is English
        cloze_s, full_s = mask_word(en_s, base_en)
        return ua_s, cloze_s, full_s
    else:
        # Target language is Ukrainian
        cloze_s, full_s = mask_word(ua_s, ua_clean)
        return en_s, cloze_s, full_s


class VocabularyRepository:
    """In-memory vocabulary repository designed for fast indexing across 40+ chapters."""

    def __init__(self, json_path: str = "words.json"):
        if not os.path.isabs(json_path):
            base_dir = os.path.dirname(os.path.abspath(__file__))
            if os.path.exists(json_path):
                json_path = os.path.abspath(json_path)
            elif os.path.exists(os.path.join(base_dir, json_path)):
                json_path = os.path.join(base_dir, json_path)
            elif os.path.exists(os.path.join(base_dir, os.path.basename(json_path))):
                json_path = os.path.join(base_dir, os.path.basename(json_path))
            else:
                json_path = os.path.join(base_dir, json_path)
        self.json_path = json_path
        self.chapters: Dict[str, List[Dict[str, str]]] = {}
        self.load_data()

    def load_data(self) -> None:
        if not os.path.exists(self.json_path):
            print(f"[VocabularyRepository] '{self.json_path}' not found. Generating fallback template...")
            generate_words_json(self.json_path)

        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if isinstance(data, dict):
                self.chapters = data
            elif isinstance(data, list):
                self.chapters = {"Default Corpus": data}
            else:
                raise ValueError("Invalid JSON format for vocabulary file.")
        except Exception as e:
            print(f"[VocabularyRepository] Error reading {self.json_path}: {e}. Re-generating fallback...")
            generate_words_json(self.json_path)
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self.chapters = json.load(f)

    def get_chapter_names(self) -> List[str]:
        return list(self.chapters.keys())

    def get_chapter_counts(self) -> Dict[str, int]:
        return {ch: len(words) for ch, words in self.chapters.items()}

    def get_total_word_count(self) -> int:
        return sum(len(words) for words in self.chapters.values())

    def create_session_deck(
        self,
        selected_word_pairs: Optional[List[Tuple[str, Dict[str, str]]]] = None,
        selected_chapters: Optional[List[str]] = None,
        direction: str = "EN->UA",
        shuffle: bool = True,
        max_words: Optional[int] = None,
        practice_mode: str = "word"
    ) -> List[Flashcard]:
        """Creates session deck from specifically selected word pairs or chapters in Word or Sentence mode."""
        raw_pool: List[Tuple[str, Dict[str, str]]] = []

        if selected_word_pairs is not None:
            raw_pool = list(selected_word_pairs)
        elif selected_chapters:
            for ch in selected_chapters:
                if ch in self.chapters:
                    for pair in self.chapters[ch]:
                        raw_pool.append((ch, pair))
        else:
            for ch, words in self.chapters.items():
                for pair in words:
                    raw_pool.append((ch, pair))

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
                _, pos_tag = parse_pos_tag(en_val)
            else:
                prompt, target = ua_val, en_val
                _, pos_tag = parse_pos_tag(en_val)

            if prompt and target:
                src_s, clz_s, ful_s = "", "", ""
                if practice_mode == "sentence":
                    src_s, clz_s, ful_s = get_context_sentences(en_val, ua_val, direction)

                deck.append(Flashcard(
                    prompt=prompt,
                    target=target,
                    direction=direction,
                    chapter=ch_name,
                    pos_tag=pos_tag,
                    original_pair=pair,
                    mode=practice_mode,
                    source_sentence=src_s,
                    target_sentence_cloze=clz_s,
                    target_sentence_full=ful_s
                ))

        return deck


# ============================================================================
# 3. SCIENTIFIC DIFF FEEDBACK WIDGET
# ============================================================================

class DiffFeedbackWidget(ctk.CTkFrame):
    """
    Scientific Error Decomposition Widget with character-level alignment,
    similarity index (Levenshtein ratio), accepted variants, and metrics.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            fg_color=PALETTE["bg_surface"],
            corner_radius=12,
            border_width=1,
            border_color=PALETTE["border"]
        )

        # Header: Diagnostic status & Similarity Index
        self.header_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.header_bar.pack(fill="x", padx=16, pady=(12, 6))

        self.status_label = ctk.CTkLabel(
            self.header_bar,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=PALETTE["text_primary"]
        )
        self.status_label.pack(side="left")

        self.similarity_badge = ctk.CTkLabel(
            self.header_bar,
            text="Similarity Index: 0.0%",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=PALETTE["accent_primary"]
        )
        self.similarity_badge.pack(side="right")

        # Row 1: User Vector
        self.user_row = ctk.CTkFrame(self, fg_color="transparent")
        self.user_row.pack(fill="x", padx=16, pady=3)

        self.user_lbl = ctk.CTkLabel(
            self.user_row,
            text="Введена відповідь:",
            width=140,
            anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=PALETTE["text_secondary"]
        )
        self.user_lbl.pack(side="left")

        self.user_text = tk.Text(
            self.user_row,
            height=1.4,
            bg=PALETTE["bg_inner"],
            fg=PALETTE["text_primary"],
            relief="flat",
            bd=0,
            highlightthickness=0,
            font=("Segoe UI", 15, "bold"),
            wrap="none"
        )
        self.user_text.pack(side="left", fill="x", expand=True)

        # Row 2: Target Vector
        self.target_row = ctk.CTkFrame(self, fg_color="transparent")
        self.target_row.pack(fill="x", padx=16, pady=3)

        self.target_lbl = ctk.CTkLabel(
            self.target_row,
            text="Еталонний таргет:",
            width=140,
            anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=PALETTE["text_secondary"]
        )
        self.target_lbl.pack(side="left")

        self.target_text = tk.Text(
            self.target_row,
            height=1.4,
            bg=PALETTE["bg_inner"],
            fg=PALETTE["text_primary"],
            relief="flat",
            bd=0,
            highlightthickness=0,
            font=("Segoe UI", 15, "bold"),
            wrap="none"
        )
        self.target_text.pack(side="left", fill="x", expand=True)

        # Tag configurations
        for text_w in (self.user_text, self.target_text):
            text_w.tag_config("correct", foreground=PALETTE["success"], font=("Segoe UI", 15, "bold"))
            text_w.tag_config("wrong", foreground=PALETTE["error"], font=("Segoe UI", 15, "bold"))
            text_w.tag_config("missing", foreground=PALETTE["warning"], font=("Segoe UI", 15, "bold", "underline"))
            text_w.tag_config("placeholder", foreground=PALETTE["text_dim"], font=("Segoe UI", 15, "bold"))

        # Bottom Bar: Metrics Breakdown & Color Legend
        self.footer_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_bar.pack(fill="x", padx=16, pady=(6, 10))

        self.metrics_lbl = ctk.CTkLabel(
            self.footer_bar,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=PALETTE["text_dim"]
        )
        self.metrics_lbl.pack(side="left")

        self.legend_lbl = ctk.CTkLabel(
            self.footer_bar,
            text="🟢 Збіг  |  🔴 Помилка  |  🟡 Очікувана літера  |  ⚪ Плейсхолдер (_)",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=PALETTE["text_dim"]
        )
        self.legend_lbl.pack(side="right")

    def display_diff(
        self,
        res: DiffResult,
        attempt_num: int = 1,
        is_revealed: bool = False,
        hint_level: int = 0,
        hint_prefix: str = "",
        hint_target: str = ""
    ) -> None:
        """Renders character diff segments and metrics."""
        if hint_level > 0 and not is_revealed:
            tot_len = len(hint_target)
            curr_char = hint_target[hint_level - 1] if 0 < hint_level <= tot_len else ""
            remaining = max(0, tot_len - hint_level)

            self.similarity_badge.configure(text=f"Відкрито: {hint_level}/{tot_len} літер")
            self.status_label.configure(
                text=f"💡 ПІДКАЗКА #{hint_level}: відкрито літеру '{curr_char}' (позиція {hint_level} з {tot_len})",
                text_color=PALETTE["warning"]
            )
            self.target_lbl.configure(text="Еталон (підказка):")

            # User input display
            self.user_text.config(state="normal")
            self.user_text.delete("1.0", "end")
            self.user_text.insert("end", hint_prefix, "correct")
            self.user_text.config(state="disabled")

            # Target display: strictly only revealed letters, rest are placeholders
            self.target_text.config(state="normal")
            self.target_text.delete("1.0", "end")
            self.target_text.insert("end", hint_prefix, "correct")
            if remaining > 0:
                placeholders = " _" * remaining
                self.target_text.insert("end", placeholders, "placeholder")
            self.target_text.config(state="disabled")

            # Do not show other variants during hint
            self.variants_lbl.configure(text="")
            self.metrics_lbl.configure(
                text=f"Підказка: відкрито {hint_level} з {tot_len} літер | Залишилось: {remaining}"
            )
            return

        sim_pct = round(res.accuracy_ratio * 100.0, 1)
        self.similarity_badge.configure(text=f"Схожість: {sim_pct}%")

        if is_revealed:
            self.status_label.configure(
                text="👁 РІШЕННЯ РОЗКРИТО (REVEALED):",
                text_color=PALETTE["warning"]
            )
            self.target_lbl.configure(text="Еталонний таргет:")
        elif res.is_exact:
            self.status_label.configure(
                text=f"✓ ТОЧНИЙ ЗБІГ! Спроба #{attempt_num}",
                text_color=PALETTE["success"]
            )
            self.target_lbl.configure(text="Еталонний таргет:")
        else:
            self.status_label.configure(
                text=f"✕ НЕВІДПОВІДНІСТЬ — Спроба #{attempt_num}:",
                text_color=PALETTE["error"]
            )
            self.target_lbl.configure(text="Еталон (відомі літери):")

        # Populate user text
        self.user_text.config(state="normal")
        self.user_text.delete("1.0", "end")
        if not res.user_segments:
            self.user_text.insert("end", "(порожній ввід)", "wrong")
        else:
            for seg in res.user_segments:
                self.user_text.insert("end", seg.text, seg.tag)
        self.user_text.config(state="disabled")

        # Populate target text
        self.target_text.config(state="normal")
        self.target_text.delete("1.0", "end")
        for seg in res.target_segments:
            if not is_revealed and not res.is_exact and seg.tag in ('missing', 'wrong'):
                masked_text = "_" * len(seg.text)
                self.target_text.insert("end", masked_text, "placeholder")
            else:
                self.target_text.insert("end", seg.text, seg.tag)
        self.target_text.config(state="disabled")

        # Metrics breakdown
        self.metrics_lbl.configure(
            text=f"Символи:  Збіг: {res.matching_count}  |  Помилка: {res.wrong_count}  |  Пропущено: {res.missing_count}"
        )


# ============================================================================
# 4. GRANULAR WORD SELECTION: CHAPTER BLOCK ACCORDION WIDGET
# ============================================================================

class ChapterBlockWidget(ctk.CTkFrame):
    """
    Expandable accordion card representing one chapter/block.
    Allows toggling the entire block or individual words within it.
    """

    def __init__(self, master, chapter_name: str, words: List[Dict[str, str]], on_selection_changed_cb):
        super().__init__(master, fg_color=PALETTE["bg_surface"], corner_radius=10, border_width=1, border_color=PALETTE["border"])
        self.chapter_name = chapter_name
        self.words = words
        self.on_selection_changed_cb = on_selection_changed_cb

        # Set of selected word indices
        self.selected_indices: Set[int] = set(range(len(words)))
        self.is_expanded: bool = False
        self.words_widgets_built: bool = False

        self.word_vars: List[ctk.BooleanVar] = []
        self.word_checkbox_rows: List[Tuple[ctk.CTkCheckBox, str, str]] = []  # (widget, en, ua)

        self._build_header()

    def _build_header(self):
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=12, pady=8)

        self.ch_var = ctk.BooleanVar(value=True)
        self.ch_chk = ctk.CTkCheckBox(
            self.header_frame,
            text=self.chapter_name,
            variable=self.ch_var,
            command=self._on_chapter_chk_toggled,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=PALETTE["text_primary"],
            fg_color=PALETTE["accent_primary"],
            hover_color=PALETTE["accent_hover"]
        )
        self.ch_chk.pack(side="left", padx=(0, 10))

        self.count_badge = ctk.CTkLabel(
            self.header_frame,
            text=f"[{len(self.words)}/{len(self.words)} слів]",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=PALETTE["accent_primary"]
        )
        self.count_badge.pack(side="left", padx=5)

        # Right control buttons
        btn_box = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        btn_box.pack(side="right")

        self.expand_btn = ctk.CTkButton(
            btn_box,
            text=f"▼ Слова ({len(self.words)})",
            width=110,
            height=26,
            fg_color=PALETTE["bg_card"],
            hover_color="#475569",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=PALETTE["text_primary"],
            command=self.toggle_expansion
        )
        self.expand_btn.pack(side="left", padx=4)

        btn_all = ctk.CTkButton(
            btn_box,
            text="Всі",
            width=40,
            height=26,
            fg_color=PALETTE["bg_card"],
            hover_color="#475569",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=PALETTE["text_secondary"],
            command=self.select_all
        )
        btn_all.pack(side="left", padx=2)

        btn_none = ctk.CTkButton(
            btn_box,
            text="0",
            width=32,
            height=26,
            fg_color=PALETTE["bg_card"],
            hover_color="#475569",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=PALETTE["text_secondary"],
            command=self.deselect_all
        )
        btn_none.pack(side="left", padx=2)

        # Container for word items
        self.words_container = ctk.CTkFrame(self, fg_color=PALETTE["bg_inner"], corner_radius=8)

    def _ensure_words_built(self):
        """Lazy builds word checkboxes upon first expansion for ultra-fast startup."""
        if self.words_widgets_built:
            return

        self.words_widgets_built = True
        for idx, w in enumerate(self.words):
            var = ctk.BooleanVar(value=(idx in self.selected_indices))
            self.word_vars.append(var)

            en_txt = w.get("en", "")
            ua_txt = w.get("ua", "")

            row = ctk.CTkFrame(self.words_container, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=2)

            chk = ctk.CTkCheckBox(
                row,
                text=f"{en_txt}   ➔   {ua_txt}",
                variable=var,
                command=lambda i=idx, v=var: self._on_word_chk_toggled(i, v.get()),
                font=ctk.CTkFont(family="Segoe UI", size=12),
                text_color=PALETTE["text_secondary"],
                fg_color=PALETTE["accent_primary"],
                hover_color=PALETTE["accent_hover"]
            )
            chk.pack(side="left", fill="x", expand=True)

            self.word_checkbox_rows.append((chk, en_txt.lower(), ua_txt.lower()))

    def toggle_expansion(self):
        self.is_expanded = not self.is_expanded
        if self.is_expanded:
            self._ensure_words_built()
            self.words_container.pack(fill="x", padx=12, pady=(0, 10))
            self.expand_btn.configure(text="▲ Згорнути")
        else:
            self.words_container.pack_forget()
            self.expand_btn.configure(text=f"▼ Слова ({len(self.words)})")

    def filter_words(self, query: str) -> bool:
        """Filters words inside this chapter. Returns True if chapter has matches."""
        q = query.strip().lower()
        if not q:
            # Show all
            if self.words_widgets_built:
                for chk, _, _ in self.word_checkbox_rows:
                    chk.master.pack(fill="x", padx=10, pady=2)
            return True

        ch_match = q in self.chapter_name.lower()
        word_matches = 0

        self._ensure_words_built()
        for chk, en, ua in self.word_checkbox_rows:
            if ch_match or q in en or q in ua:
                chk.master.pack(fill="x", padx=10, pady=2)
                word_matches += 1
            else:
                chk.master.pack_forget()

        if word_matches > 0 and not self.is_expanded:
            self.toggle_expansion()

        return ch_match or (word_matches > 0)

    def _on_chapter_chk_toggled(self):
        val = self.ch_var.get()
        if val:
            self.select_all()
        else:
            self.deselect_all()

    def _on_word_chk_toggled(self, idx: int, is_selected: bool):
        if is_selected:
            self.selected_indices.add(idx)
        else:
            self.selected_indices.discard(idx)
        self._update_badges_and_vars()
        self.on_selection_changed_cb()

    def select_all(self):
        self.selected_indices = set(range(len(self.words)))
        if self.words_widgets_built:
            for v in self.word_vars:
                v.set(True)
        self._update_badges_and_vars()
        self.on_selection_changed_cb()

    def deselect_all(self):
        self.selected_indices.clear()
        if self.words_widgets_built:
            for v in self.word_vars:
                v.set(False)
        self._update_badges_and_vars()
        self.on_selection_changed_cb()

    def _update_badges_and_vars(self):
        sel_cnt = len(self.selected_indices)
        tot_cnt = len(self.words)
        self.count_badge.configure(text=f"[{sel_cnt}/{tot_cnt} слів]")
        self.ch_var.set(sel_cnt > 0)

    def get_selected_pairs(self) -> List[Tuple[str, Dict[str, str]]]:
        """Returns list of (chapter_name, pair) for all selected words."""
        return [(self.chapter_name, self.words[idx]) for idx in sorted(self.selected_indices)]


# ============================================================================
# 5. START MENU FRAME (SESSION CONFIGURATION)
# ============================================================================

class StartMenuFrame(ctk.CTkFrame):
    """Scientific Parameter Configuration & Word Selection Frame."""

    def __init__(self, master, repository: VocabularyRepository, on_start_callback):
        super().__init__(master, fg_color="transparent")
        self.repo = repository
        self.on_start_callback = on_start_callback

        self.mode_var = ctk.StringVar(value="Слова (Words)")
        self.direction_var = ctk.StringVar(value="English ➔ Ukrainian")
        self.size_var = ctk.StringVar(value="All Words")
        self.shuffle_var = ctk.BooleanVar(value=True)

        self.block_widgets: List[ChapterBlockWidget] = []
        self._build_ui()

    def _build_ui(self):
        content_box = ctk.CTkFrame(
            self,
            fg_color=PALETTE["bg_surface"],
            corner_radius=16,
            border_width=1,
            border_color=PALETTE["border"]
        )
        content_box.pack(fill="both", expand=True, padx=25, pady=15)

        # Header Title
        title_box = ctk.CTkFrame(content_box, fg_color="transparent")
        title_box.pack(fill="x", padx=25, pady=(15, 5))

        title_lbl = ctk.CTkLabel(
            title_box,
            text="VOCABULARY DRILL SYSTEM",
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color=PALETTE["accent_primary"]
        )
        title_lbl.pack(anchor="w")

        subtitle_lbl = ctk.CTkLabel(
            title_box,
            text="Платформа когнітивного тестування лексики з посимвольним аналізом та гранулярним вибором слів",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=PALETTE["text_secondary"]
        )
        subtitle_lbl.pack(anchor="w")

        # Two-column layout: Left (Parameters), Right (Corpus Selection)
        grid_frame = ctk.CTkFrame(content_box, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=20, pady=5)

        # Left Column: Configuration Parameters
        left_col = ctk.CTkFrame(
            grid_frame,
            fg_color=PALETTE["bg_card"],
            corner_radius=12,
            border_width=1,
            border_color=PALETTE["border"],
            width=320
        )
        left_col.pack(side="left", fill="both", padx=(0, 10), pady=5)
        left_col.pack_propagate(False)

        # 0. Practice Mode (Words vs Sentences)
        sec0_lbl = ctk.CTkLabel(
            left_col,
            text="1. РЕЖИМ ТРЕНУВАННЯ",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=PALETTE["text_primary"]
        )
        sec0_lbl.pack(anchor="w", padx=16, pady=(14, 6))

        self.mode_seg = ctk.CTkSegmentedButton(
            left_col,
            values=["Слова (Words)", "Речення (Sentences)"],
            variable=self.mode_var,
            selected_color=PALETTE["accent_primary"],
            selected_hover_color=PALETTE["accent_hover"],
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        )
        self.mode_seg.set("Слова (Words)")
        self.mode_seg.pack(fill="x", padx=16, pady=4)

        # 1. Practice Direction
        sec1_lbl = ctk.CTkLabel(
            left_col,
            text="2. НАПРЯМ ТЕСТУВАННЯ",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=PALETTE["text_primary"]
        )
        sec1_lbl.pack(anchor="w", padx=16, pady=(16, 6))

        self.dir_seg = ctk.CTkSegmentedButton(
            left_col,
            values=["English ➔ Ukrainian", "Ukrainian ➔ English"],
            variable=self.direction_var,
            selected_color=PALETTE["accent_primary"],
            selected_hover_color=PALETTE["accent_hover"],
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        )
        self.dir_seg.set("English ➔ Ukrainian")
        self.dir_seg.pack(fill="x", padx=16, pady=4)

        # 2. Sample Size (N)
        sec2_lbl = ctk.CTkLabel(
            left_col,
            text="3. ОБСЯГ СЕСІЇ (SAMPLE SIZE)",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=PALETTE["text_primary"]
        )
        sec2_lbl.pack(anchor="w", padx=16, pady=(16, 6))

        self.size_seg = ctk.CTkSegmentedButton(
            left_col,
            values=["10 Cards", "25 Cards", "50 Cards", "All Words"],
            variable=self.size_var,
            font=ctk.CTkFont(family="Segoe UI", size=12)
        )
        self.size_seg.set("All Words")
        self.size_seg.pack(fill="x", padx=16, pady=4)

        # 3. Randomization
        sec3_lbl = ctk.CTkLabel(
            left_col,
            text="4. СТОХАСТИЧНИЙ ПОРЯДОК",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=PALETTE["text_primary"]
        )
        sec3_lbl.pack(anchor="w", padx=16, pady=(16, 6))

        shuffle_chk = ctk.CTkCheckBox(
            left_col,
            text="Випадковий порядок карток",
            variable=self.shuffle_var,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=PALETTE["text_secondary"],
            fg_color=PALETTE["accent_primary"],
            hover_color=PALETTE["accent_hover"]
        )
        shuffle_chk.pack(anchor="w", padx=16, pady=4)

        # Live selection counter card
        self.telemetry_box = ctk.CTkFrame(left_col, fg_color=PALETTE["bg_inner"], corner_radius=10, border_width=1, border_color=PALETTE["border"])
        self.telemetry_box.pack(fill="x", padx=16, pady=(20, 10))

        self.total_selected_lbl = ctk.CTkLabel(
            self.telemetry_box,
            text="Обрано слів: 0",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color=PALETTE["accent_primary"]
        )
        self.total_selected_lbl.pack(pady=(12, 4))

        self.blocks_selected_lbl = ctk.CTkLabel(
            self.telemetry_box,
            text="Блоків активних: 0",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=PALETTE["text_secondary"]
        )
        self.blocks_selected_lbl.pack(pady=(0, 12))

        # Right Column: Chapter & Granular Word Scope
        right_col = ctk.CTkFrame(
            grid_frame,
            fg_color=PALETTE["bg_card"],
            corner_radius=12,
            border_width=1,
            border_color=PALETTE["border"]
        )
        right_col.pack(side="right", fill="both", expand=True, padx=(10, 0), pady=5)

        # Right Header Bar
        rh_bar = ctk.CTkFrame(right_col, fg_color="transparent")
        rh_bar.pack(fill="x", padx=16, pady=(14, 6))

        rh_title = ctk.CTkLabel(
            rh_bar,
            text="4. КОРПУС ТА ВИБІР СЛІВ (CORPUS SELECTION)",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=PALETTE["text_primary"]
        )
        rh_title.pack(side="left")

        # Global Action Buttons
        glob_btns = ctk.CTkFrame(rh_bar, fg_color="transparent")
        glob_btns.pack(side="right")

        btn_all_glob = ctk.CTkButton(
            glob_btns,
            text="Обрати всі слова",
            width=120,
            height=26,
            fg_color=PALETTE["bg_surface"],
            hover_color="#475569",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=PALETTE["text_primary"],
            command=self.select_all_globally
        )
        btn_all_glob.pack(side="left", padx=3)

        btn_none_glob = ctk.CTkButton(
            glob_btns,
            text="Зняти всі",
            width=80,
            height=26,
            fg_color=PALETTE["bg_surface"],
            hover_color="#475569",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=PALETTE["text_secondary"],
            command=self.deselect_all_globally
        )
        btn_none_glob.pack(side="left", padx=3)

        # Real-time search & filter bar
        search_box = ctk.CTkFrame(right_col, fg_color="transparent")
        search_box.pack(fill="x", padx=16, pady=4)

        self.search_entry = ctk.CTkEntry(
            search_box,
            placeholder_text="🔍 Пошук слова або розділу (фільтр у реальному часі)...",
            height=34,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            fg_color=PALETTE["bg_inner"],
            border_color=PALETTE["border"],
            border_width=1
        )
        self.search_entry.pack(fill="x")
        self.search_entry.bind("<KeyRelease>", self._on_search_query_changed)

        # Scrollable container for chapters & words
        self.scroll_area = ctk.CTkScrollableFrame(
            right_col,
            fg_color="transparent",
            height=260
        )
        self.scroll_area.pack(fill="both", expand=True, padx=12, pady=6)

        # Instantiate Chapter Block Widgets
        for ch_name, words in self.repo.chapters.items():
            block_w = ChapterBlockWidget(
                self.scroll_area,
                chapter_name=ch_name,
                words=words,
                on_selection_changed_cb=self._on_corpus_selection_updated
            )
            block_w.pack(fill="x", pady=4)
            self.block_widgets.append(block_w)

        # Bottom Start Practice Button
        self.start_btn = ctk.CTkButton(
            content_box,
            text="🚀 Почати тестування",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            fg_color=PALETTE["accent_primary"],
            hover_color=PALETTE["accent_hover"],
            text_color=PALETTE["bg_main"],
            height=46,
            corner_radius=10,
            command=self._on_start_clicked
        )
        self.start_btn.pack(fill="x", padx=25, pady=(10, 16))

        self._on_corpus_selection_updated()

    def _on_search_query_changed(self, event=None):
        q = self.search_entry.get().strip()
        for bw in self.block_widgets:
            has_match = bw.filter_words(q)
            if has_match:
                bw.pack(fill="x", pady=4)
            else:
                bw.pack_forget()

    def select_all_globally(self):
        for bw in self.block_widgets:
            bw.select_all()

    def deselect_all_globally(self):
        for bw in self.block_widgets:
            bw.deselect_all()

    def _on_corpus_selection_updated(self):
        total_selected = sum(len(bw.selected_indices) for bw in self.block_widgets)
        active_blocks = sum(1 for bw in self.block_widgets if len(bw.selected_indices) > 0)
        total_available = self.repo.get_total_word_count()

        self.total_selected_lbl.configure(text=f"Обрано: {total_selected} / {total_available} слів")
        self.blocks_selected_lbl.configure(text=f"Блоків активних: {active_blocks} з {len(self.block_widgets)}")

        if total_selected == 0:
            self.start_btn.configure(
                state="disabled",
                text="Оберіть хоча б 1 слово для тренування",
                fg_color=PALETTE["border"]
            )
        else:
            self.start_btn.configure(
                state="normal",
                text=f"🚀 Почати тестування ({total_selected} слів)",
                fg_color=PALETTE["accent_primary"],
                text_color=PALETTE["bg_main"]
            )

    def _on_start_clicked(self):
        chosen_pairs: List[Tuple[str, Dict[str, str]]] = []
        for bw in self.block_widgets:
            chosen_pairs.extend(bw.get_selected_pairs())

        raw_dir = (self.dir_seg.get() or self.direction_var.get() or "").strip()
        dir_val = "UA->EN" if raw_dir.startswith("Ukrainian") or "UA->EN" in raw_dir else "EN->UA"

        mode_str = (self.mode_seg.get() or self.mode_var.get() or "").strip()
        practice_mode = "sentence" if ("Речення" in mode_str or "Sentences" in mode_str) else "word"

        size_str = self.size_seg.get()
        max_w = None
        if "10" in size_str:
            max_w = 10
        elif "25" in size_str:
            max_w = 25
        elif "50" in size_str:
            max_w = 50

        deck = self.repo.create_session_deck(
            selected_word_pairs=chosen_pairs,
            direction=dir_val,
            shuffle=self.shuffle_var.get(),
            max_words=max_w,
            practice_mode=practice_mode
        )

        self.on_start_callback(deck)


# ============================================================================
# 6. FLASHCARD PRACTICE FRAME (SCIENTIFIC TESTING & FEEDBACK)
# ============================================================================

@dataclass
class CardSessionRecord:
    card: Flashcard
    status: str  # 'correct', 'mistake', 'skipped'
    attempts: int
    last_user_input: str


class FlashcardFrame(ctk.CTkFrame):
    """
    Cognitive Lexical Testing Interface.
    Features safe entry management (no ghost text), progressive hints,
    full reveal, skip handling, error tracking, and character diff analytics.
    """

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
        self.hint_level: int = 0
        self.current_had_mistake: bool = False
        self.current_user_input: str = ""
        self.session_records: List[CardSessionRecord] = []
        self.is_auto_advancing: bool = False
        self.current_card: Optional[Flashcard] = None

        self._build_ui()

    def _build_ui(self):
        # 1. Scientific Telemetry HUD Bar
        hud_bar = ctk.CTkFrame(
            self,
            fg_color=PALETTE["bg_surface"],
            corner_radius=12,
            border_width=1,
            border_color=PALETTE["border"]
        )
        hud_bar.pack(fill="x", padx=20, pady=(12, 8))

        back_btn = ctk.CTkButton(
            hud_bar,
            text="⬅ До Меню",
            width=90,
            height=30,
            fg_color=PALETTE["bg_card"],
            hover_color="#475569",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=PALETTE["text_primary"],
            command=self._on_back_clicked
        )
        back_btn.pack(side="left", padx=10, pady=8)

        self.chapter_badge = ctk.CTkLabel(
            hud_bar,
            text="БЛОК: —",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=PALETTE["accent_secondary"]
        )
        self.chapter_badge.pack(side="left", padx=10)

        # Metric Chips (Right)
        score_box = ctk.CTkFrame(hud_bar, fg_color="transparent")
        score_box.pack(side="right", padx=10)

        self.correct_badge = ctk.CTkLabel(
            score_box, text="✓ 0",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=PALETTE["success"]
        )
        self.correct_badge.pack(side="left", padx=8)

        self.incorrect_badge = ctk.CTkLabel(
            score_box, text="✕ 0",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=PALETTE["error"]
        )
        self.incorrect_badge.pack(side="left", padx=8)

        self.skip_badge = ctk.CTkLabel(
            score_box, text="⏭ 0",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=PALETTE["text_dim"]
        )
        self.skip_badge.pack(side="left", padx=8)

        self.accuracy_badge = ctk.CTkLabel(
            score_box, text="🎯 0.0%",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=PALETTE["accent_primary"]
        )
        self.accuracy_badge.pack(side="left", padx=8)

        # 2. Progress Bar
        prog_box = ctk.CTkFrame(self, fg_color="transparent")
        prog_box.pack(fill="x", padx=25, pady=(2, 8))

        self.card_count_lbl = ctk.CTkLabel(
            prog_box, text="Картка: 0 / 0",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=PALETTE["text_primary"]
        )
        self.card_count_lbl.pack(side="left", padx=(0, 10))

        self.progress_bar = ctk.CTkProgressBar(
            prog_box, height=8, corner_radius=4,
            progress_color=PALETTE["accent_primary"], fg_color=PALETTE["bg_card"]
        )
        self.progress_bar.pack(side="left", fill="x", expand=True)
        self.progress_bar.set(0)

        # 3. Main Stimulus & Testing Card
        card_container = ctk.CTkFrame(
            self,
            fg_color=PALETTE["bg_surface"],
            corner_radius=16,
            border_width=1,
            border_color=PALETTE["border"]
        )
        card_container.pack(fill="both", expand=True, padx=20, pady=5)

        # Linguistic Meta Badges
        meta_row = ctk.CTkFrame(card_container, fg_color="transparent")
        meta_row.pack(fill="x", padx=40, pady=(16, 2))

        self.lang_pill = ctk.CTkLabel(
            meta_row,
            text="ТЕСТУВАННЯ: ENGLISH ➔ UKRAINIAN",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=PALETTE["accent_primary"]
        )
        self.lang_pill.pack(side="left")

        self.pos_badge = ctk.CTkLabel(
            meta_row,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=PALETTE["accent_secondary"]
        )
        self.pos_badge.pack(side="right")

        # Contextual Sentence Box (Sentence Cloze Mode)
        self.sentence_box = ctk.CTkFrame(
            card_container,
            fg_color=PALETTE["bg_inner"],
            corner_radius=12,
            border_width=1,
            border_color=PALETTE["border"]
        )
        self.source_sentence_lbl = ctk.CTkLabel(
            self.sentence_box,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=PALETTE["text_secondary"],
            wraplength=840,
            justify="center"
        )
        self.source_sentence_lbl.pack(padx=20, pady=(10, 4))

        self.cloze_sentence_lbl = ctk.CTkLabel(
            self.sentence_box,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=17, weight="bold"),
            text_color=PALETTE["accent_primary"],
            wraplength=840,
            justify="center"
        )
        self.cloze_sentence_lbl.pack(padx=20, pady=(4, 10))

        # Lexical Prompt Display
        self.prompt_lbl = ctk.CTkLabel(
            card_container,
            text="Target Word",
            font=ctk.CTkFont(family="Segoe UI", size=30, weight="bold"),
            text_color=PALETTE["text_primary"]
        )
        self.prompt_lbl.pack(pady=(10, 16))

        # Input Entry Frame
        entry_frame = ctk.CTkFrame(card_container, fg_color="transparent")
        entry_frame.pack(fill="x", padx=40, pady=4)

        self.entry = ctk.CTkEntry(
            entry_frame,
            placeholder_text="Введіть відповідь та натисніть Enter...",
            height=48,
            font=ctk.CTkFont(family="Segoe UI", size=18),
            corner_radius=10,
            border_width=2,
            border_color=PALETTE["border"],
            fg_color=PALETTE["bg_inner"]
        )
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", self._on_enter_pressed)

        # Action Controls
        controls_box = ctk.CTkFrame(card_container, fg_color="transparent")
        controls_box.pack(fill="x", padx=40, pady=10)

        # Hint Button (Provides progressive clues without ending trial)
        self.hint_btn = ctk.CTkButton(
            controls_box,
            text="💡 Підказка",
            width=115, height=38,
            fg_color=PALETTE["warning"],
            hover_color="#d97706",
            text_color=PALETTE["bg_main"],
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=self._on_hint_clicked
        )
        self.hint_btn.pack(side="left", padx=(0, 8))

        # Reveal Solution Button
        self.reveal_btn = ctk.CTkButton(
            controls_box,
            text="👁 Розкрити",
            width=105, height=38,
            fg_color=PALETTE["bg_card"],
            hover_color="#475569",
            text_color=PALETTE["text_primary"],
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=self._on_reveal_clicked
        )
        self.reveal_btn.pack(side="left", padx=(0, 8))

        # Skip Button
        self.skip_btn = ctk.CTkButton(
            controls_box,
            text="⏭ Пропустити",
            width=115, height=38,
            fg_color=PALETTE["bg_card"],
            hover_color="#475569",
            text_color=PALETTE["text_secondary"],
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=self._on_skip_clicked
        )
        self.skip_btn.pack(side="left")

        # Primary Action / Validation Button
        self.action_btn = ctk.CTkButton(
            controls_box,
            text="✓ Перевірити (Enter)",
            height=38,
            fg_color=PALETTE["accent_primary"],
            hover_color=PALETTE["accent_hover"],
            text_color=PALETTE["bg_main"],
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            command=self._on_action_clicked
        )
        self.action_btn.pack(side="right", fill="x", expand=True, padx=(15, 0))

        # Diff Feedback Engine
        self.diff_widget = DiffFeedbackWidget(card_container)

    def _reset_entry(self, initial_text: str = "", state: str = "normal", border_color: str = PALETTE["border"]):
        """
        Safely configures and resets the entry widget.
        Guarantees that state='normal' is set BEFORE calling delete/insert,
        completely resolving Tkinter's disabled-entry ghost text bug.
        """
        self.entry.configure(state="normal")
        self.entry.delete(0, "end")
        if initial_text:
            self.entry.insert(0, initial_text)
        self.entry.configure(state=state, border_color=border_color)

    def start_session(self, deck: List[Flashcard]):
        """Initializes a new practice session with the provided deck."""
        self.deck = deck
        self.current_idx = 0
        self.correct_count = 0
        self.incorrect_count = 0
        self.skipped_count = 0
        self.session_records = []

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
        self.hint_level = 0
        self.current_had_mistake = False
        self.current_user_input = ""
        self.is_auto_advancing = False
        self.current_card = self.deck[self.current_idx]

        # Reset Entry completely
        self._reset_entry(initial_text="", state="normal", border_color=PALETTE["border"])
        self.diff_widget.pack_forget()
        self.entry.focus_set()

        # Update Linguistic Prompt & Badges
        dir_text = "ТЕСТУВАННЯ: ENGLISH ➔ UKRAINIAN" if self.current_card.direction == "EN->UA" else "ТЕСТУВАННЯ: UKRAINIAN ➔ ENGLISH"
        self.lang_pill.configure(text=dir_text)
        self.chapter_badge.configure(text=f"БЛОК: {self.current_card.chapter}")

        if self.current_card.pos_tag:
            self.pos_badge.configure(text=f"[{self.current_card.pos_tag}]")
        else:
            self.pos_badge.configure(text="")

        if self.current_card.mode == "sentence" and self.current_card.source_sentence:
            self.sentence_box.pack(fill="x", padx=40, pady=(4, 10), before=self.prompt_lbl)
            self.source_sentence_lbl.configure(text=f"📖 Контекст: {self.current_card.source_sentence}")
            self.cloze_sentence_lbl.configure(
                text=self.current_card.target_sentence_cloze,
                text_color=PALETTE["accent_primary"]
            )
            self.prompt_lbl.configure(
                text=f"Вставте слово: {self.current_card.prompt}",
                font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold")
            )
        else:
            self.sentence_box.pack_forget()
            self.prompt_lbl.configure(
                text=self.current_card.prompt,
                font=ctk.CTkFont(family="Segoe UI", size=30, weight="bold")
            )

        # Progress telemetry
        total = len(self.deck)
        current_num = self.current_idx + 1
        self.card_count_lbl.configure(text=f"Картка: {current_num} / {total}")
        self.progress_bar.set(current_num / total)

        self._update_score_hud()

        self.hint_btn.configure(state="normal")
        self.reveal_btn.configure(state="normal")
        self.skip_btn.configure(state="normal")
        self.action_btn.configure(
            text="✓ Перевірити (Enter)",
            fg_color=PALETTE["accent_primary"],
            text_color=PALETTE["bg_main"],
            state="normal"
        )

    def _update_score_hud(self):
        self.correct_badge.configure(text=f"✓ {self.correct_count}")
        self.incorrect_badge.configure(text=f"✕ {self.incorrect_count}")
        self.skip_badge.configure(text=f"⏭ {self.skipped_count}")

        total_answered = self.correct_count + self.incorrect_count
        acc = round((self.correct_count / total_answered) * 100.0, 1) if total_answered > 0 else 0.0
        self.accuracy_badge.configure(text=f"🎯 {acc}%")

    def _on_enter_pressed(self, event=None):
        self._on_action_clicked()

    def _on_action_clicked(self):
        if self.is_auto_advancing:
            return

        # If card was already revealed, Enter proceeds to next card
        if self.card_revealed:
            if self.current_card:
                self.session_records.append(CardSessionRecord(
                    card=self.current_card,
                    status="mistake",
                    attempts=self.card_attempts,
                    last_user_input=self.current_user_input
                ))
            self._advance_to_next_card()
            return

        user_input = self.entry.get().strip()
        self.current_user_input = user_input

        # Check if user explicitly typed "skip" or "скіп" into input
        if user_input.lower() in ("skip", "скіп", "/skip", ":skip"):
            self._on_skip_clicked()
            return

        if not self.current_card:
            return

        self.card_attempts += 1
        res = evaluate_answer(user_input, self.current_card.target)

        self.diff_widget.display_diff(res, attempt_num=self.card_attempts)
        self.diff_widget.pack(fill="x", padx=20, pady=(5, 12))

        if res.is_exact:
            self.correct_count += 1
            self._update_score_hud()

            if self.current_card.mode == "sentence" and self.current_card.target_sentence_full:
                self.cloze_sentence_lbl.configure(
                    text=f"✓ {self.current_card.target_sentence_full}",
                    text_color=PALETTE["success"]
                )

            status = "mistake" if (self.current_had_mistake or self.card_attempts > 1 or self.hint_level > 0) else "correct"
            self.session_records.append(CardSessionRecord(
                card=self.current_card,
                status=status,
                attempts=self.card_attempts,
                last_user_input=user_input
            ))

            self._reset_entry(initial_text=res.target_word_raw, state="disabled", border_color=PALETTE["success"])
            self.action_btn.configure(
                text="✓ Правильно! Перехід...",
                fg_color=PALETTE["success"],
                text_color=PALETTE["bg_main"],
                state="disabled"
            )

            self.is_auto_advancing = True
            self.after(750, self._advance_to_next_card)
        else:
            self.current_had_mistake = True
            self.entry.configure(border_color=PALETTE["error"])
            self.entry.focus_set()

    def _on_hint_clicked(self):
        """
        Progressive Hint:
        1st click: reveals strictly only the 1st letter.
        2nd click: reveals the 2nd letter (prefix of length 2).
        k-th click: reveals the k-th letter, and so on.
        """
        if not self.current_card or self.card_revealed:
            return

        self.current_had_mistake = True
        variants = get_target_variants(self.current_card.target)
        primary_target = variants[0] if variants else self.current_card.target
        tot_len = len(primary_target)

        # Advance hint level strictly by 1 on each click
        self.hint_level += 1
        if self.hint_level > tot_len:
            self.hint_level = tot_len

        hint_prefix = primary_target[:self.hint_level]

        # Safely reset entry with current prefix and keep it editable/focused
        self._reset_entry(initial_text=hint_prefix, state="normal", border_color=PALETTE["warning"])
        self.entry.focus_set()
        try:
            self.entry.icursor("end")
        except Exception:
            pass

        res = evaluate_answer(hint_prefix, primary_target)
        self.diff_widget.display_diff(
            res,
            attempt_num=self.card_attempts,
            hint_level=self.hint_level,
            hint_prefix=hint_prefix,
            hint_target=primary_target
        )
        self.diff_widget.pack(fill="x", padx=20, pady=(5, 12))

    def _on_reveal_clicked(self):
        """Reveals full target solution, fills entry cleanly, and prepares Enter to advance."""
        if not self.current_card or self.card_revealed:
            return

        self.card_revealed = True
        self.current_had_mistake = True
        self.incorrect_count += 1
        self._update_score_hud()

        res = evaluate_answer("", self.current_card.target)
        self.diff_widget.display_diff(res, is_revealed=True)
        self.diff_widget.pack(fill="x", padx=20, pady=(5, 12))

        if self.current_card.mode == "sentence" and self.current_card.target_sentence_full:
            self.cloze_sentence_lbl.configure(
                text=f"👁 {self.current_card.target_sentence_full}",
                text_color=PALETTE["warning"]
            )

        # Fill the correct target cleanly in amber disabled state
        self._reset_entry(initial_text=res.target_word_raw, state="disabled", border_color=PALETTE["warning"])

        self.action_btn.configure(
            text="Наступна картка ➔ (Натисніть Enter)",
            fg_color=PALETTE["warning"],
            text_color=PALETTE["bg_main"],
            state="normal"
        )
        self.action_btn.focus_set()

    def _on_skip_clicked(self):
        """Safely skips the card and advances without leaving ghost text."""
        if self.current_card:
            self.session_records.append(CardSessionRecord(
                card=self.current_card,
                status="skipped",
                attempts=self.card_attempts,
                last_user_input=self.current_user_input
            ))
        self._reset_entry(initial_text="", state="normal")
        self.skipped_count += 1
        self._advance_to_next_card()

    def _advance_to_next_card(self):
        self.current_idx += 1
        self._load_current_card()

    def _on_back_clicked(self):
        self._reset_entry(initial_text="", state="normal")
        self.on_back_callback()

    def _finish_session(self):
        app_instance = cast("VocabDrillApp", self.winfo_toplevel())
        app_instance.show_summary(
            total=len(self.deck),
            correct=self.correct_count,
            incorrect=self.incorrect_count,
            skipped=self.skipped_count,
            records=list(self.session_records)
        )


# ============================================================================
# 7. SUMMARY FRAME (SCIENTIFIC PERFORMANCE REPORT)
# ============================================================================

class SummaryFrame(ctk.CTkFrame):
    """Session performance evaluation report with detailed mistake & correct lists."""

    def __init__(self, master, on_menu_callback, on_restart_callback):
        super().__init__(master, fg_color="transparent")
        self.on_menu_callback = on_menu_callback
        self.on_restart_callback = on_restart_callback
        self.records: List[CardSessionRecord] = []
        self._build_ui()

    def _build_ui(self):
        box = ctk.CTkFrame(
            self,
            fg_color=PALETTE["bg_surface"],
            corner_radius=16,
            border_width=1,
            border_color=PALETTE["border"]
        )
        box.pack(fill="both", expand=True, padx=40, pady=20)

        title = ctk.CTkLabel(
            box,
            text="📊 ЗВІТ СЕСІЇ ТЕСТУВАННЯ (SESSION REPORT)",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color=PALETTE["accent_primary"]
        )
        title.pack(pady=(16, 6))

        self.acc_lbl = ctk.CTkLabel(
            box,
            text="Точність (Accuracy P_acc): 0.0%",
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color=PALETTE["success"]
        )
        self.acc_lbl.pack(pady=4)

        # Performance Metrics Grid
        stats_grid = ctk.CTkFrame(
            box,
            fg_color=PALETTE["bg_inner"],
            corner_radius=10,
            border_width=1,
            border_color=PALETTE["border"]
        )
        stats_grid.pack(fill="x", padx=30, pady=8)

        self.details_lbl = ctk.CTkLabel(
            stats_grid,
            text="Карток: 0  |  ✓ Успішно: 0  |  ✕ З помилками: 0  |  ⏭ Пропущено: 0",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=PALETTE["text_primary"]
        )
        self.details_lbl.pack(pady=10)

        # Scrollable area showing detailed list of words (mistakes & corrects)
        self.results_scroll = ctk.CTkScrollableFrame(
            box,
            fg_color=PALETTE["bg_inner"],
            corner_radius=10,
            height=320
        )
        self.results_scroll.pack(fill="both", expand=True, padx=30, pady=8)

        btn_row = ctk.CTkFrame(box, fg_color="transparent")
        btn_row.pack(pady=(10, 16))

        btn_menu = ctk.CTkButton(
            btn_row,
            text="Головне меню",
            width=130,
            height=40,
            fg_color=PALETTE["bg_card"],
            hover_color="#475569",
            text_color=PALETTE["text_primary"],
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            command=self.on_menu_callback
        )
        btn_menu.pack(side="left", padx=8)

        self.btn_again = ctk.CTkButton(
            btn_row,
            text="🔁 Повторити все (помилки × 3)",
            width=210,
            height=40,
            fg_color=PALETTE["accent_primary"],
            hover_color=PALETTE["accent_hover"],
            text_color=PALETTE["bg_main"],
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            command=lambda: self.on_restart_callback(repeat_mistakes_factor=3, only_mistakes=False)
        )
        self.btn_again.pack(side="left", padx=8)

        self.btn_mistakes_only = ctk.CTkButton(
            btn_row,
            text="🎯 Тільки проблемні слова (× 3)",
            width=230,
            height=40,
            fg_color=PALETTE["warning"],
            hover_color="#d97706",
            text_color=PALETTE["bg_main"],
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            command=lambda: self.on_restart_callback(repeat_mistakes_factor=3, only_mistakes=True)
        )
        self.btn_mistakes_only.pack(side="left", padx=8)

    def set_summary(self, total: int, correct: int, incorrect: int, skipped: int, records: Optional[List[CardSessionRecord]] = None):
        self.records = records or []
        for child in self.results_scroll.winfo_children():
            child.destroy()

        mistakes = [r for r in self.records if r.status == "mistake"]
        skipped_items = [r for r in self.records if r.status == "skipped"]
        corrects = [r for r in self.records if r.status == "correct"]

        num_mistakes = len(mistakes)
        num_correct = len(corrects)
        num_skipped = len(skipped_items)

        total_tested = num_correct + num_mistakes
        acc = round((num_correct / total_tested) * 100.0, 1) if total_tested > 0 else 0.0

        self.acc_lbl.configure(text=f"Точність (Accuracy): {acc}%")
        self.details_lbl.configure(
            text=f"Всього карток (N): {len(self.records)}   |   ✓ Без помилок: {num_correct}   |   ✕ З помилками: {num_mistakes}   |   ⏭ Пропущено: {num_skipped}"
        )

        problematic_count = num_mistakes + num_skipped

        if problematic_count > 0:
            self.btn_mistakes_only.pack(side="left", padx=8)
            self.btn_mistakes_only.configure(
                text=f"🎯 Тільки проблемні ({problematic_count}) × 3",
                state="normal"
            )
            self.btn_again.configure(text="🔁 Повторити все (помилки × 3)")
        else:
            self.btn_mistakes_only.pack_forget()
            self.btn_again.configure(text="🔁 Повторити тестування")

        # 1. Section: Mistake Words
        if mistakes:
            sec_err = ctk.CTkFrame(self.results_scroll, fg_color="transparent")
            sec_err.pack(fill="x", padx=6, pady=(6, 4))

            lbl_err = ctk.CTkLabel(
                sec_err,
                text=f"❌ СЛОВА З ПОМИЛКАМИ (будуть повторені по 3 рази — {len(mistakes)}):",
                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                text_color=PALETTE["error"]
            )
            lbl_err.pack(anchor="w")

            for r in mistakes:
                row = ctk.CTkFrame(
                    self.results_scroll,
                    fg_color=PALETTE["bg_surface"],
                    corner_radius=8,
                    border_width=1,
                    border_color=PALETTE["error"]
                )
                row.pack(fill="x", padx=6, pady=3)

                txt_left = f"❌  {r.card.prompt}   ➔   {r.card.target}"
                lbl_word = ctk.CTkLabel(
                    row,
                    text=txt_left,
                    font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                    text_color=PALETTE["text_primary"]
                )
                lbl_word.pack(side="left", padx=12, pady=8)

                info_txt = f"Спроб: {r.attempts}"
                if r.last_user_input and r.last_user_input.lower() != r.card.target.lower():
                    info_txt += f"  (Введено: \"{r.last_user_input}\")"

                lbl_info = ctk.CTkLabel(
                    row,
                    text=info_txt,
                    font=ctk.CTkFont(family="Segoe UI", size=11),
                    text_color=PALETTE["error"]
                )
                lbl_info.pack(side="right", padx=12)

        # 2. Section: Skipped Words
        if skipped_items:
            sec_skip = ctk.CTkFrame(self.results_scroll, fg_color="transparent")
            sec_skip.pack(fill="x", padx=6, pady=(12, 4))

            lbl_skip = ctk.CTkLabel(
                sec_skip,
                text=f"⏭ ПРОПУЩЕНІ СЛОВА ({len(skipped_items)}):",
                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                text_color=PALETTE["warning"]
            )
            lbl_skip.pack(anchor="w")

            for r in skipped_items:
                row = ctk.CTkFrame(
                    self.results_scroll,
                    fg_color=PALETTE["bg_surface"],
                    corner_radius=8,
                    border_width=1,
                    border_color=PALETTE["border"]
                )
                row.pack(fill="x", padx=6, pady=3)

                txt_left = f"⏭  {r.card.prompt}   ➔   {r.card.target}"
                lbl_word = ctk.CTkLabel(
                    row,
                    text=txt_left,
                    font=ctk.CTkFont(family="Segoe UI", size=13),
                    text_color=PALETTE["text_secondary"]
                )
                lbl_word.pack(side="left", padx=12, pady=8)

                lbl_info = ctk.CTkLabel(
                    row,
                    text="Пропущено",
                    font=ctk.CTkFont(family="Segoe UI", size=11),
                    text_color=PALETTE["text_dim"]
                )
                lbl_info.pack(side="right", padx=12)

        # 3. Section: Correct Words
        if corrects:
            sec_cor = ctk.CTkFrame(self.results_scroll, fg_color="transparent")
            sec_cor.pack(fill="x", padx=6, pady=(12, 4))

            lbl_cor = ctk.CTkLabel(
                sec_cor,
                text=f"✓ ПРАВИЛЬНО ЗАСВОЄНІ СЛОВА ({len(corrects)}):",
                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                text_color=PALETTE["success"]
            )
            lbl_cor.pack(anchor="w")

            for r in corrects:
                row = ctk.CTkFrame(
                    self.results_scroll,
                    fg_color=PALETTE["bg_surface"],
                    corner_radius=8,
                    border_width=1,
                    border_color=PALETTE["border"]
                )
                row.pack(fill="x", padx=6, pady=3)

                txt_left = f"✓  {r.card.prompt}   ➔   {r.card.target}"
                lbl_word = ctk.CTkLabel(
                    row,
                    text=txt_left,
                    font=ctk.CTkFont(family="Segoe UI", size=13),
                    text_color=PALETTE["text_primary"]
                )
                lbl_word.pack(side="left", padx=12, pady=6)

                lbl_info = ctk.CTkLabel(
                    row,
                    text="✓ З 1-ї спроби",
                    font=ctk.CTkFont(family="Segoe UI", size=11),
                    text_color=PALETTE["success"]
                )
                lbl_info.pack(side="right", padx=12)

        if not mistakes and not skipped_items and corrects:
            celebration = ctk.CTkLabel(
                self.results_scroll,
                text="🎉 Ідеальний результат! Усі слова засвоєно без жодної помилки!",
                font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                text_color=PALETTE["success"]
            )
            celebration.pack(pady=30)


# ============================================================================
# 8. MAIN APPLICATION CONTAINER
# ============================================================================

class VocabDrillApp(ctk.CTk):
    """Main Application Window."""

    def __init__(self):
        super().__init__()

        self.title("VocabDrill - Cognitive Lexical Testing & Error Analysis System")
        self.geometry("1040x740")
        self.minsize(920, 660)

        self.configure(fg_color=PALETTE["bg_main"])

        self.repository = VocabularyRepository("words.json")
        self.last_deck: List[Flashcard] = []
        self.base_session_deck: List[Flashcard] = []
        self.last_records: List[CardSessionRecord] = []

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

    def start_practice(self, deck: List[Flashcard], is_retry: bool = False):
        if not is_retry:
            self.base_session_deck = list(deck)
        self.last_deck = list(deck)
        self.start_menu_frame.pack_forget()
        self.summary_frame.pack_forget()
        self.flashcard_frame.pack(fill="both", expand=True)
        self.flashcard_frame.start_session(deck)

    def restart_practice(self, repeat_mistakes_factor: int = 3, only_mistakes: bool = False):
        source_deck = self.base_session_deck if self.base_session_deck else self.last_deck
        if not source_deck:
            self.show_start_menu()
            return

        mistake_prompts = {r.card.prompt for r in self.last_records if r.status in ("mistake", "skipped")}

        # Deduplicate source cards by prompt
        seen_prompts = set()
        unique_source: List[Flashcard] = []
        for card in source_deck:
            if card.prompt not in seen_prompts:
                seen_prompts.add(card.prompt)
                unique_source.append(card)

        new_deck: List[Flashcard] = []
        for card in unique_source:
            if card.prompt in mistake_prompts:
                # Word had a mistake - repeat it multiple times!
                for _ in range(repeat_mistakes_factor):
                    new_deck.append(card)
            elif not only_mistakes:
                new_deck.append(card)

        if not new_deck:
            new_deck = list(unique_source)

        random.shuffle(new_deck)
        self.start_practice(new_deck, is_retry=True)

    def show_summary(self, total: int, correct: int, incorrect: int, skipped: int, records: Optional[List[CardSessionRecord]] = None):
        self.last_records = records or []
        self.flashcard_frame.pack_forget()
        self.start_menu_frame.pack_forget()
        self.summary_frame.set_summary(total, correct, incorrect, skipped, self.last_records)
        self.summary_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = VocabDrillApp()
    app.mainloop()
