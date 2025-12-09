import os

# Allow overriding key settings from environment variables.
# This keeps sensible defaults while letting CI/deploys and local shells
# tweak behavior without editing this file.

def _get_bool_env(name, default):
    v = os.getenv(name)
    if v is None:
        return default
    return str(v).lower() in ("1", "true", "yes", "on")

def _get_float_env(name, default):
    v = os.getenv(name)
    if v is None:
        return default
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


BOT_NAME = os.getenv("BOT_NAME", "shabdasankalak")
FEED_EXPORT_ENCODING = os.getenv("FEED_EXPORT_ENCODING", "utf-8")

SPIDER_MODULES = [os.getenv("SPIDER_MODULES", "shabdasankalak.spiders")]
NEWSPIDER_MODULE = os.getenv("NEWSPIDER_MODULE", "shabdasankalak.spiders")

# Crawling controls
ROBOTSTXT_OBEY = _get_bool_env("ROBOTSTXT_OBEY", True)
DOWNLOAD_DELAY = _get_float_env("DOWNLOAD_DELAY", 1.0)
DOWNLOAD_TIMEOUT = _get_float_env("DOWNLOAD_TIMEOUT", 30)

DEFAULT_REQUEST_HEADERS = {
    "User-Agent": (
        os.getenv(
            "DEFAULT_USER_AGENT",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36",
        )
    ),
    "Accept": os.getenv(
        "DEFAULT_ACCEPT", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    ),
    "Accept-Language": os.getenv("DEFAULT_ACCEPT_LANGUAGE", "en-US,en;q=0.9"),
}

DOWNLOADER_MIDDLEWARES = {
    "shabdasankalak.middlewares.CloudscraperMiddleware": 560,
    "scrapy.downloadermiddlewares.redirect.RedirectMiddleware": 600,
    "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 810,
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": 550,
}

ITEM_PIPELINES = {
    # Use site-specific pipelines so Ekantipur and Ukaalo items are
    # stored in their intended folder structure.
    'shabdasankalak.pipelines.EkantipurSaveEachItemPipeline': 300,
    'shabdasankalak.pipelines.UkaaloSaveEachItemPipeline': 310,
    # Generic pipeline is still available if you prefer it instead
    # 'shabdasankalak.pipelines.SaveEachItemPipeline': 300,
}


# Retry on typical Cloudflare statuses
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [403, 429, 503]


# Optional local overrides: create `shabdasankalak/local_settings.py` to
# override any of the values above without changing this file. This is
# useful for local development or secrets that should not be committed.
try:
    # local_settings may define/override any of the names above
    from .local_settings import *  # type: ignore
except Exception:
    pass

