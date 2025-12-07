# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib
import json
import os
import re

from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter


class EkantipurScraperPipeline:
    def process_item(self, item, spider):
        return item



class SaveEachItemPipeline:
    def process_item(self, item, spider):
        url = item.get("url", "")

        # Generate unique hash from URL
        unique_hash = hashlib.md5(url.encode("utf-8")).hexdigest()

        # Extract YYYY-MM from URL using regex
        match = re.search(r"/(\d{4})/(\d{2})/\d{2}/", url)
        if match:
            year, month = match.group(1), match.group(2)
            subdir = f"{year}-{month}"
        else:
            subdir = "unknown"  # fallback if URL doesn't contain a date

        # Ensure output directory exists
        dir_path = os.path.join("data", subdir)
        os.makedirs(dir_path, exist_ok=True)

        # File path
        file_path = os.path.join(dir_path, f"{unique_hash}.json")

        # Skip if file already exists
        if os.path.exists(file_path):
            raise DropItem(f"Duplicate item skipped: {url}")

        # Save item as JSON
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(dict(item), f, ensure_ascii=False, indent=2)

        return item

