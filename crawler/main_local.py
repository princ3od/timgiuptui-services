import json
import timeit

from models import Source
from scrapy.crawler import CrawlerProcess, Settings
from scrapy_crawler import settings as local_crawler_settings
from scrapy_crawler.pipelines import NewsCrawlerPipeline
from scrapy_crawler.spiders.nld import NguoiLaoDongSpider
from scrapy_crawler.spiders.tuoitre import TuoiTreSpider
from scrapy_crawler.spiders.vnexpress import VnExpressSpider


def main_local(*args, **kwargs):
    start_time = timeit.default_timer()
    print(">> Start crawling...", flush=True)

    NewsCrawlerPipeline.save_spider_articles = True

    spiders = [
        TuoiTreSpider,
        VnExpressSpider,
        NguoiLaoDongSpider,
    ]
    crawler_settings = Settings()
    crawler_settings.setmodule(local_crawler_settings)
    crawler = CrawlerProcess(settings=crawler_settings)
    sources = {
        "nld": Source(
            editor_id="nld",
            urls={
                "business": "https://nld.com.vn/kinh-te.rss",
            },
        ),
        "vnexpress": Source(
            editor_id="vnexpress",
            urls={
                "business": "https://vnexpress.net/rss/kinh-doanh.rss",
            },
        ),
        "tuoitre": Source(
            editor_id="tuoitre",
            urls={
                "business": "https://tuoitre.vn/rss/kinh-doanh.rss",
            },
        ),
    }
    for spider in spiders:
        crawler.crawl(spider, sources[spider.name])

    crawler.join()
    crawler.start()

    number_of_articles = 0
    for topic in NewsCrawlerPipeline.articles_by_topics:
        number_of_articles += len(NewsCrawlerPipeline.articles_by_topics[topic].keys())
        print(f"> {topic}: {len(NewsCrawlerPipeline.articles_by_topics[topic].keys())}")
    elapsed_time = round(timeit.default_timer() - start_time, 4)
    print(f">> Number of articles: {number_of_articles}")
    print(f">> Time elapsed: {elapsed_time}s")
    with open("articles_by_topics.json", "w", encoding="utf-8") as file:
        json.dump(
            NewsCrawlerPipeline.articles_by_topics,
            file,
            ensure_ascii=False,
            indent=2,
            default=str,
        )


main_local()
