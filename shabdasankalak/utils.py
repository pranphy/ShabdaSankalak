import re

import hashlib
import os


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


def get_hashed_file_path(url: str, spider_name: str) -> str:
    """
    Determine the file path for a given URL and spider name.
    """
    subdir = "unknown"

    if spider_name == 'kantipur':
        match = re.search(r"/(\d{4})/(\d{2})/\d{2}/", url)
        if match:
            year, month = match.group(1), match.group(2)
            subdir = os.path.join("kantipur", f"{year}-{month}")
        else:
            subdir = os.path.join("kantipur", "unknown")

    elif spider_name == 'ukaalo':
        match = re.search(r"/news/(\d+)", url)
        if match:
            article_id = match.group(1)
            try:
                n = int(article_id)
                bucket_size = 10000
                start = (n // bucket_size) * bucket_size
                end = start + bucket_size - 1
                subdir = os.path.join("ukaalo", f"{start:05d}-{end:05d}")
            except ValueError:
                subdir = "ukaalo-unknown"
        else:
            subdir = "ukaalo-unknown"
    
    else:
         # Fallback for other/unknown spiders
         subdir = spider_name

    unique_hash = hashlib.md5(url.encode("utf-8")).hexdigest()
    dir_path = os.path.join("data", subdir)
    return os.path.join(dir_path, f"{unique_hash}.json")
