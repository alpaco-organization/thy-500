import re
import unicodedata


def normalize_name(value: str) -> str:
    """Normalize a human name for Turkish/diacritic-insensitive exact matching.

    - Trims and collapses whitespace
    - Removes diacritics (Ş→S, Ö→O, İ→I, etc.)
    - Uppercases
    """

    text = (value or "").strip()
    text = re.sub(r"\s+", " ", text)

    # Decompose (NFKD) then drop combining marks (accents, dots, etc.)
    decomposed = unicodedata.normalize("NFKD", text)
    without_marks = "".join(ch for ch in decomposed if not unicodedata.combining(ch))

    return without_marks.upper()
