def clean_header(text: str) -> str:
    text = text.lower().strip()
    replacements = {
        "fg %": "fg_percent",
        "xp %": "xp_percent",
        "long": "fg_long",
        "fg blk": "fg_blocked",
        "1-19": "fg_1_19",
        "20-29": "fg_20_29",
        "30-39": "fg_30_39",
        "40-49": "fg_40_49",
        "50-59": "fg_50_59",
        "60+": "fg_60_plus",
        " › a-m": "",
        "a-m": "",
        " ": "_"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text