"""
words_generator.py - Standalone helper & generator for words.json template.

Generates a structured words.json file containing 8 distinct chapters
with English-Ukrainian vocabulary pairs.
"""

import json
import os
from typing import Dict, List

# Core seed data divided into 8 thematic chapters
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
            # Distribute extra words evenly across the 8 chapters
            chapter_keys = list(data.keys())
            for idx, word in enumerate(extra_words):
                chapter_key = chapter_keys[idx % len(chapter_keys)]
                # Avoid duplicate entries
                if not any(w['en'].lower() == word['en'].lower() for w in data[chapter_key]):
                    data[chapter_key].append(word)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return data

if __name__ == '__main__':
    # Try finding words.txt in parent directory or current directory
    possible_txt = [
        "words.txt",
        "../words.txt",
        r"c:\Users\maksym.kozyr\Desktop\Git workspace\project1\words.txt"
    ]
    found_txt = None
    for path in possible_txt:
        if os.path.exists(path):
            found_txt = path
            break

    res_data = generate_words_json("words.json", source_txt=found_txt)
    total_words = sum(len(v) for v in res_data.values())
    print(f"Generated words.json with {len(res_data)} chapters and {total_words} total words.")
