# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import logging
from urllib.parse import urlparse
from scrapy.http import HtmlResponse
import cloudscraper

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


logger = logging.getLogger(__name__)

class EkantipurScraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    async def process_start(self, start):
        # Called with an async iterator over the spider start() method or the
        # maching method of an earlier spider middleware.
        async for item_or_request in start:
            yield item_or_request

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class EkantipurScraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class CloudscraperMiddleware:
    def __init__(self):
        # Single persistent session
        self.scraper = cloudscraper.create_scraper(
            browser={"browser": "chrome", "platform": "windows", "mobile": False}
        )

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
            # Only intercept normal GET HTTP(S) requests
            if request.method != "GET" or not request.url.startswith(("http://", "https://")):
                return None

            # Let Scrapy handle robots.txt itself
            path = urlparse(request.url).path or ""
            if path.endswith("/robots.txt"):
                return None

            # Scrapy headers -> plain str dict
            try:
                headers = request.headers.to_unicode_dict()
            except Exception:
                # Manual fallback if needed
                headers = {}
                for k, v in request.headers.items():
                    # k, v can be bytes or list of bytes
                    key = k.decode() if isinstance(k, (bytes, bytearray)) else str(k)
                    if isinstance(v, (list, tuple)):
                        val = v[0]
                        val = val.decode() if isinstance(val, (bytes, bytearray)) else str(val)
                    else:
                        val = v.decode() if isinstance(v, (bytes, bytearray)) else str(v)
                    headers[key] = val

            try:
                resp = self.scraper.get(
                    request.url,
                    headers=headers,
                    timeout=30,
                    allow_redirects=True,
                )

                # Build Scrapy response
                return HtmlResponse(
                    url=str(resp.url),
                    status=resp.status_code,
                    headers=resp.headers,
                    body=resp.content,
                    encoding=resp.encoding or "utf-8",
                    request=request,
                )
            except Exception as e:
                logger.warning(f"Cloudscraper fetch failed for {request.url}: {e}")
                # Let Scrapy try the normal downloader/retry middleware
                return None
