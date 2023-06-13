from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
# Anime
from .spiders.animeflix import AnimeflixSpider
from .spiders.animepahe import AnimePaheSpider
from .spiders.gogoanime import GogoanimeSpider
from .spiders.kato import KatoSpider
from .spiders.nineanime import NineanimeSpider
from .spiders.yugen import YugenSpider
from .spiders.zoro import ZoroSpider



class Scraper:
    def __init__(self):
        settings_file_path = 'scrapers.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)

        self.process = CrawlerProcess(get_project_settings())
        self.spiders = [
            AnimeflixSpider,
            AnimePaheSpider,
            GogoanimeSpider,
            KatoSpider,
            NineanimeSpider,
            YugenSpider,
            ZoroSpider
        ]

    def run_spiders(self):
        for spider in self.spiders:
            self.process.crawl(spider)
        self.process.start()