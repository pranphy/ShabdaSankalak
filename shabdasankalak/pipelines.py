# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib
import json
import os
import re
from urllib.parse import urlparse

from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter


class EkantipurScraperPipeline:
    def process_item(self, item, spider):
        return item



def _save_item_to_hashed_file(item, subdir: str):
    """Save item to data/<subdir>/<md5(url)>.json.

    Raises DropItem if file already exists. Returns the file path on success.
    """
    url = item.get("url", "")
    unique_hash = hashlib.md5(url.encode("utf-8")).hexdigest()

    dir_path = os.path.join("data", subdir)
    os.makedirs(dir_path, exist_ok=True)

    file_path = os.path.join(dir_path, f"{unique_hash}.json")
    if os.path.exists(file_path):
        raise DropItem(f"Duplicate item skipped: {url}")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(dict(item), f, ensure_ascii=False, indent=2)

    return file_path


class SaveEachItemPipeline:
    """Generic pipeline that decides subdir by domain or spider name and
    saves each item as a hashed JSON file.
    """

    def process_item(self, item, spider):
        url = item.get("url", "")
        parsed = urlparse(url)
        domain = parsed.netloc.lower() if parsed.netloc else ""

        # Try site-specific heuristics first
        subdir = None

        if "ekantipur" in domain or getattr(spider, "name", "") == "ekantipur":
            match = re.search(r"/(\d{4})/(\d{2})/\d{2}/", url)
            if match:
                year, month = match.group(1), match.group(2)
                # store Ekantipur items under data/ekantipur/YYYY-MM/
                subdir = os.path.join("ekantipur", f"{year}-{month}")

        if subdir is None and ("ukaalo" in domain or getattr(spider, "name", "") == "ukaalo"):
            match = re.search(r"/news/(\d+)", url)
            if match:
                subdir = "ukaalo"

        if subdir is None:
            subdir = domain.replace(":", "_").replace(".", "_") if domain else "unknown"

        _save_item_to_hashed_file(item, subdir)
        return item


class EkantipurSaveEachItemPipeline:
    """Pipeline specialized for Ekantipur: extracts YYYY-MM from URL and
    stores under data/ekantipur-YYYY-MM/."""

    def process_item(self, item, spider):
        url = item.get("url", "")
        match = re.search(r"/(\d{4})/(\d{2})/\d{2}/", url)
        if match:
            year, month = match.group(1), match.group(2)
            subdir = os.path.join("ekantipur", f"{year}-{month}")
        else:
            subdir = os.path.join("ekantipur", "unknown")

        _save_item_to_hashed_file(item, subdir)
        return item


class UkaaloSaveEachItemPipeline:
    """Pipeline specialized for Ukaalo: expects article URLs as /news/<digits>
    and stores items under data/ukaalo/ as hashed files."""

    def process_item(self, item, spider):
        url = item.get("url", "")
        match = re.search(r"/news/(\d+)", url)
        if match:
            article_id = match.group(1)
            # Bucket numeric id into ranges of 10,000: 0-9999, 10000-19999, ...
            try:
                n = int(article_id)
            except ValueError:
                subdir = "ukaalo-unknown"
            else:
                bucket_size = 10000
                start = (n // bucket_size) * bucket_size
                end = start + bucket_size - 1
                # zero-pad to 5 digits for consistent folder names
                subdir = os.path.join("ukaalo", f"{start:05d}-{end:05d}")
        else:
            subdir = "ukaalo-unknown"

        _save_item_to_hashed_file(item, subdir)
        return item

