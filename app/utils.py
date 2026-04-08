def fuzzy_match(a: str, b: str):
    return a.lower() in b.lower() or b.lower() in a.lower()