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


from shabdasankalak.utils import get_hashed_file_path

class ShabdaSankalakPipeline:
    """Unified pipeline for ShabdaSankalak spiders.
    
    Decides the storage subdirectory based on spider.name and URL patterns.
    """

    def process_item(self, item, spider):
        url = item.get("url", "")
        file_path = get_hashed_file_path(url, spider.name)
        
        if os.path.exists(file_path):
            raise DropItem(f"Duplicate item skipped: {url}")

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(dict(item), f, ensure_ascii=False, indent=2)

        return item
