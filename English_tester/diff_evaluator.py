"""
diff_evaluator.py - Character-level string alignment and diff evaluator with placeholders.

Computes exact matching, character-level diff opcodes, and missing character
placeholders ('_') between user input and target word using SequenceMatcher.
"""

import difflib
import re
from dataclasses import dataclass
from typing import List, Set

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

def _evaluate_single(user_clean: str, target_clean: str) -> DiffResult:
    """Evaluates user input against a single concrete target string with character-level alignment."""
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

def get_target_variants(target_str: str) -> List[str]:
    """
    Parses a target string that may contain multiple alternative answers
    (separated by '/' or ',') and optional parenthetical explanations (e.g. '(n)', '(одяг)').
    Returns a list of distinct valid single-answer variants.
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
        # Also handle comma-separated options e.g. "вступ, знайомство"
        sub_parts = [sp.strip() for sp in p.split(',') if sp.strip()]
        for sp in sub_parts:
            # 1) Option without parentheses e.g. "приміряти" from "приміряти (одяг)" or "aim" from "aim (n)"
            no_paren = re.sub(r'\(.*?\)', '', sp).strip()
            if no_paren:
                add_var(no_paren)
            # 2) Option with parentheses
            add_var(sp)
            # 3) English verbs starting with "to "
            if sp.lower().startswith('to ') and len(sp) > 3:
                add_var(sp[3:].strip())

    # 4) Full raw string as fallback
    add_var(raw)
    return variants

def evaluate_answer(user_input: str, target_word: str) -> DiffResult:
    """
    Evaluates user input against target word, supporting multiple accepted alternative answers.
    - If user enters ANY of the valid alternative answers, it is considered exact and correct.
    - Diff feedback and displayed target will strictly show the single matched or closest variant,
      avoiding multiple answers grouped together in the target line.
    """
    user_clean = user_input.strip()
    user_norm = user_clean.lower()

    variants = get_target_variants(target_word)
    if not variants:
        variants = [target_word.strip()]

    # 1. Check for exact match against any valid variant
    for v in variants:
        if user_norm == v.lower():
            res = _evaluate_single(user_clean, v)
            res.target_word_raw = v
            return res

    # 2. If no exact match, find the single closest variant to compare against
    # Exclude the combined multi-word fallback (the last item) when there are individual variants
    candidates = variants[:-1] if len(variants) > 1 else variants

    best_variant = candidates[0]
    best_ratio = -1.0

    for v in candidates:
        ratio = difflib.SequenceMatcher(None, user_norm, v.lower()).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_variant = v

    res = _evaluate_single(user_clean, best_variant)
    res.target_word_raw = best_variant
    return res

if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    res = evaluate_answer("яб", "яблуко")
    print("Is exact:", res.is_exact)
    print("User segments:", res.user_segments)
    print("Target segments:", res.target_segments)
