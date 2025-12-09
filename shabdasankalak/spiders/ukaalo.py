import re
import scrapy
from shabdasankalak.items import EkantipurScraperItem
from shabdasankalak.utils import is_nepali_line, clean_content


class UkaaloSpider(scrapy.Spider):
    name = "ukaalo"
    allowed_domains = ["ukaalo.com", "www.ukaalo.com"]
    categories = [
        'ukaalo-vishesh',
        'approach',
        'book',
        'cinema',
        'climate',
        'column',
        'culture',
        'desh',
        'games',
        'geopolitics',
        'health',
        'heratige',
        'literature',
        'love_life',
        'market',
        'migration',
        'news',
        'opinion_education',
        'opinion_family',
        'opinion_health',
        'politics',
        'remember',
        'science',
        'songs',
        'television',
        'theater',
        'travel',
        'world',
    ]
    start_urls = [f"https://ukaalo.com/category/{cat}/" for cat in categories]
    #start_urls = ["https://ukaalo.com/news/1991/"]

    def parse(self, response):
        # Follow likely article links. Ukaalo article URLs may vary; try
        # common patterns first (date-based, /news/, /post/) and otherwise
        # follow internal links but avoid obvious index/tag pages.
        for href in response.css("a::attr(href)").getall():
            if not href:
                continue
            # Only follow numeric article URLs of the form /news/<digits>
            # Examples: https://ukaalo.com/news/12345
            if re.search(r"/news/\d+", href):
                yield response.follow(href, self.parse_article)

        # Follow pagination
        next_page = response.css("a[rel='next']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        item = EkantipurScraperItem()
        item["url"] = response.url

        # Title
        title = response.css("h1::text").get()
        if not title:
            title = response.css("header h1::text").get()
        item["title"] = title.strip() if title else None

        # Date: try <time datetime=>, meta tags, or textual date
        date = response.css(".post__meta .post__date p::text").get()
        if not date:
            date = response.css("meta[property='article:published_time']::attr(content)").get()
        if not date:
            date = response.css(".posted-on time::text, .post-date::text").get()
        item["date"] = date.strip() if date else None

        # Author
        authors = response.css(".post__meta .author span::text").getall()
        authors = [a.strip() for a in authors if a and a.strip()]
        item["author"] = ", ".join(authors) if authors else None

        # Category / breadcrumbs
        cat = response.css('div.breadcrumbs li:last-child a::text').get()
        item["category"] = cat.strip() if cat else None

        # Content: try several common containers
        paragraphs = response.css("#news-content p *::text").getall()
        raw_content = "\n".join(p.strip() for p in paragraphs if p and p.strip())

        cleaned = clean_content(raw_content)

        # Extract place from first line if dateline present (em dash)
        place = response.css("#news-content p strong::text").get()

        splace = None

        if cleaned:
            first_line = cleaned.split("\n", 1)[0]
            if "–" in first_line:
                splace, rest = first_line.split("–", 1)
                splace = splace.strip()
                # Replace content with rest of article (without place dateline)
                cleaned = rest.strip() + ("\n" + cleaned.split("\n", 1)[1] if "\n" in cleaned else "")


        item["place"] = place or place
        item["content"] = cleaned 

        yield item
