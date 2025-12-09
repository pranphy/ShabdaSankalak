import re
import calendar
import json
import scrapy
from shabdasankalak.items import EkantipurScraperItem
from shabdasankalak.utils import is_nepali_line, clean_content

class EkantipurSpider(scrapy.Spider):
    name = "ekantipur"
    allowed_domains = ["ekantipur.com"]
    categories = [
        'Art',
        'bibidha',
        'blog',
        'business',
        'cricket-world-cup-2019',
        'destination',
        'diaspora',
        'entertainment',
        'feature',
        'health',
        'hello-sukrabar',
        'interesting',
        'Interview',
        'kopila',
        'koseli',
        'lifestyle',
        'literature',
        'local-elections-2017',
        'nari-nepali',
        'national',
        'national',
        'nepal-elections-2074',
        'news',
        'opinion',
        'Other',
        'our-nepal',
        'pathakmanch',
        'phadko',
        'pradesh-1',
        'pradesh-2',
        'pradesh-3',
        'pradesh-4',
        'pradesh-5',
        'pradesh-6',
        'pradesh-7',
        'printedition',
        'sports',
        'technology',
        'world',
    ]

    def __init__(self, date=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date_param = date  # optional YYYY/MM
        self.start_urls = []

        # Build start_urls for each category
        if self.date_param:
            year, month = map(int, self.date_param.split("-"))
            _, num_days = calendar.monthrange(year, month)
            for cat in self.categories:
                #for day in [11]:
                for day in range(1, num_days + 1):
                    url = f"https://ekantipur.com/{cat}/{year}/{month:02d}/{day:02d}"
                    self.start_urls.append(url)
        else:
            # Default: just category root pages
            self.start_urls = [f"https://ekantipur.com/{cat}" for cat in self.categories]
        print(f"The start urls is \n {self.start_urls}")

    def parse(self, response):
        # Only follow article detail links with /YYYY/MM/DD/ in them
        for href in response.css("a::attr(href)").getall():
            if re.search(r"/\d{4}/\d{2}/\d{2}/", href):
                yield response.follow(href, self.parse_article)

        # Pagination
        next_page = response.css("a[rel='next']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        item = EkantipurScraperItem()
        item["url"] = response.url

        # Title
        item["title"] = response.css("h1::text").get()

        # Date
        item["date"] = response.css("span.detail-date::text").get()


        # Author
        authors = response.css("div.author a::text").getall()
        item["author"] = ", ".join(a.strip() for a in authors if a.strip()) if authors else None 

        # Category
        item["category"] = response.css("div.cat_name a::text").get()


        # Raw content paragraphs
        paragraphs = response.css("div.story-content p::text").getall()
        if not paragraphs:
            paragraphs = response.css("article p::text").getall()
        raw_content = "\n".join(p.strip() for p in paragraphs if p.strip())

        # Clean content: normalize \xa0 and filter
        cleaned = clean_content(raw_content)

        # Extract place from the very first line if it contains an em dash
        place = None
        if cleaned:
            first_line = cleaned.split("\n", 1)[0]
            if "—" in first_line:
                place, rest = first_line.split("—", 1)
                place = place.strip()
                # Replace content with rest of article (without place dateline)
                cleaned = rest.strip() + ("\n" + cleaned.split("\n", 1)[1] if "\n" in cleaned else "")

        item["place"] = place
        item["content"] = cleaned

        yield item

