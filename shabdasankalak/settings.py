BOT_NAME = "shabdasankalak"
FEED_EXPORT_ENCODING = "utf-8"

SPIDER_MODULES = ["shabdasankalak.spiders"]
NEWSPIDER_MODULE = "shabdasankalak.spiders"

ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 1.0
DOWNLOAD_TIMEOUT = 30

DEFAULT_REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

DOWNLOADER_MIDDLEWARES = {
    "shabdasankalak.middlewares.CloudscraperMiddleware": 560,
    "scrapy.downloadermiddlewares.redirect.RedirectMiddleware": 600,
    "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 810,
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": 550,
}

ITEM_PIPELINES = {
    'shabdasankalak.pipelines.SaveEachItemPipeline': 300,
}


# Retry on typical Cloudflare statuses
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [403, 429, 503]

