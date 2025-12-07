from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def run_spider():
    settings = get_project_settings()
    date = "2025-08"
    #opfile = f"ekantipur_articles_{date}.json"
    # Add or override settings programmatically
    settings.set('LOG_LEVEL', 'INFO')
    settings.set('JOBDIR', 'crawls/ekantipur')   # persistent crawl state
    settings.set('FEED_FORMAT', 'json')
    #settings.set('FEED_URI', opfile)
    settings.set('FEED_EXPORT_ENCODING', 'utf-8')

    process = CrawlerProcess(settings)
    process.crawl('ekantipur', date=date)   # pass parameters here
    process.start()

if __name__ == "__main__":
    run_spider()

