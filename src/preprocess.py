import re
import unicodedata
from typing import List

# Arabic characters Unicode ranges
ARABIC_LETTERS_RE = re.compile(r"[\u0621-\u063A\u0641-\u064A]+", re.UNICODE)
ARABIC_KEEP_CHARS = "\u0621-\u063A\u0641-\u064A\s"  # letters and space

# Common Arabic diacritics
DIACRITICS_PATTERN = re.compile(r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]")
TATWEEL_PATTERN = re.compile(r"\u0640")

# Basic Arabic stopwords (extendable)
ARABIC_STOPWORDS = set([
    "في", "من", "على", "و", "إلى", "عن", "أن", "إن", "كان", "كانت", "هو", "هي", "هم",
    "ما", "لا", "لم", "لن", "قد", "هذا", "هذه", "هناك", "كل", "أو", "كما", "أي", "بين",
    "مع", "بعد", "قبل", "حتى", "أكثر", "أثناء", "حيث", "لكن", "بل", "إذا", "إلا", "إما",
])


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def remove_diacritics(text: str) -> str:
    return DIACRITICS_PATTERN.sub("", text)


def remove_tatweel(text: str) -> str:
    return TATWEEL_PATTERN.sub("", text)


def normalize_arabic_letters(text: str) -> str:
    # Normalize different forms of alef/ya/ta marbuta
    replacements = {
        "أ": "ا", "إ": "ا", "آ": "ا",
        "ى": "ي", "ئ": "ي", "ؤ": "و",
        "ة": "ه",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text


def keep_arabic_and_space(text: str) -> str:
    # Remove any character that is not Arabic letter or whitespace
    return re.sub(fr"[^{ARABIC_KEEP_CHARS}]+", " ", text)


def tokenize(text: str) -> List[str]:
    return [t for t in re.split(r"\s+", text) if t]


def remove_stopwords(tokens: List[str]) -> List[str]:
    return [t for t in tokens if t not in ARABIC_STOPWORDS]


def preprocess_text(text: str,
                    remove_diac: bool = True,
                    remove_tat: bool = True,
                    normalize_letters: bool = True,
                    filter_non_ar: bool = True,
                    filter_stopwords: bool = True) -> str:
    if text is None:
        return ""
    text = str(text)
    text = normalize_whitespace(text)
    if remove_diac:
        text = remove_diacritics(text)
    if remove_tat:
        text = remove_tatweel(text)
    if normalize_letters:
        text = normalize_arabic_letters(text)
    if filter_non_ar:
        text = keep_arabic_and_space(text)
    text = normalize_whitespace(text)
    tokens = tokenize(text)
    if filter_stopwords:
        tokens = remove_stopwords(tokens)
    return " ".join(tokens)
