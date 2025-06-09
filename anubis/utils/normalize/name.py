import re
import unicodedata

# 🧠 Canonical aliases for display and DB insertion
NAME_ALIASES = {
    "marquise brown": "Hollywood Brown",
    # Add more as needed
}

def normalize_name_for_matching(name: str) -> str:
    """
    Use for fuzzy name resolution / lookups.
    Lowercase, remove accents, strip suffixes, remove punctuation.
    """
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    name = name.lower().strip()
    name = re.sub(r'\b(jr|sr|ii|iii|iv)\b', '', name)
    name = re.sub(r"[^\w\s]", "", name)  # remove punctuation
    name = re.sub(r"\s+", " ", name)     # collapse whitespace
    return name.strip()

def normalize_name_for_display(name: str) -> str:
    """
    Use before inserting player name into DB or displaying in UI.
    Maps aliases to canonical versions (e.g., Marquise Brown → Hollywood Brown).
    """
    key = normalize_name_for_matching(name)
    return NAME_ALIASES.get(key, name.strip())