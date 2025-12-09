import re


def is_nepali_line(line: str, threshold: float = 0.3) -> bool:
    """
    Decide if a line is Nepali content based on ratio of Devanagari characters.
    Returns True if the fraction of Devanagari characters in the line is >= threshold.
    """
    line = line.strip()
    if not line:
        return False
    total_chars = len(line)
    nepali_chars = len(re.findall(r"[\u0900-\u097F]", line))
    ratio = nepali_chars / total_chars if total_chars > 0 else 0
    return ratio >= threshold


def clean_content(text: str) -> str:
    """
    Normalize spaces, remove non-breaking spaces and keep only lines that
    contain enough Nepali script according to `is_nepali_line`.
    Returns cleaned text where lines are joined by newlines.
    """
    # Replace non-breaking spaces with normal spaces
    text = text.replace("\xa0", " ")

    lines = text.splitlines()
    cleaned = []
    for line in lines:
        if is_nepali_line(line):
            # Collapse multiple spaces
            line = re.sub(r"\s+", " ", line)
            cleaned.append(line.strip())
    return "\n".join(cleaned)
