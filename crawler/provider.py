import timeit
from twisted.internet import reactor

from constants import PubSubTopicIds
from event_handler import pubsub_publish
from logs import logger
from models import Source
from scrapy.crawler import CrawlerRunner, Settings
from scrapy_crawler import settings as local_crawler_settings
from scrapy_crawler.pipelines import NewsCrawlerPipeline
from scrapy_crawler.spiders.nld import NguoiLaoDongSpider
from scrapy_crawler.spiders.tuoitre import TuoiTreSpider
from scrapy_crawler.spiders.vnexpress import VnExpressSpider



class Provider:

    spiders = [
        NguoiLaoDongSpider,
        TuoiTreSpider,
        VnExpressSpider,
    ]

    def start_crawling(self, sources: list[Source]) -> None:
        self.start_time = timeit.default_timer()
        logger.info(">> Start crawling...")

        source_dict = self._get_source_dict(sources)
        crawler = self._setup_crawler()
        self._setup_spiders(crawler, source_dict)

        self._crawl(crawler)
        self._handle_crawled_articles(NewsCrawlerPipeline.articles_by_topics)

        elapsed_time = round(timeit.default_timer() - self.start_time, 4)
        logger.info(f">> Elapsed time: {elapsed_time}")

    def _get_source_dict(self, sources: list[Source]) -> dict[str, Source]:
        source_dict = {}
        for source in sources:
            if source.editor_id not in source_dict:
                source_dict[source.editor_id] = []
            source_dict[source.editor_id] = source
        return source_dict

    def _setup_crawler(self) -> CrawlerRunner:
        crawler_settings = Settings()
        crawler_settings.setmodule(local_crawler_settings)
        crawler = CrawlerRunner(settings=crawler_settings)
        return crawler

    def _setup_spiders(self, crawler: CrawlerRunner, sources: dict[str, Source]):
        for spider in self.spiders:
            if spider.name not in sources:
                continue
            source = sources[spider.name]
            crawler.crawl(spider, source)

    def _crawl(self, crawler: CrawlerRunner):
        d = crawler.join()
        d.addBoth(lambda _: reactor.stop())
        reactor.run(0)

    def _handle_crawled_articles(self, articles: dict[str, dict]):
        pubsub_publish(topic=PubSubTopicIds.HANDLE_ARTICLES, data=articles)
        number_of_articles = 0
        for topic, articles_by_topic in articles.items():
            number_of_articles += len(articles_by_topic.keys())
            print(f"> {topic}: {len(articles_by_topic.keys())}")
        print(f">> Number of articles: {number_of_articles}")
