"""
diff_evaluator.py - Character-level string alignment and diff evaluator with placeholders.

Computes exact matching, character-level diff opcodes, and missing character
placeholders ('_') between user input and target word using SequenceMatcher.
"""

import difflib
from dataclasses import dataclass
from typing import List

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

if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    res = evaluate_answer("яб", "яблуко")
    print("Is exact:", res.is_exact)
    print("User segments:", res.user_segments)
    print("Target segments:", res.target_segments)
