from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import json
from datetime import datetime
# Anime
from .spiders.animeflix import AnimeflixSpider
from .spiders.animepahe import AnimePaheSpider
from .spiders.gogoanime import GogoanimeSpider
from .spiders.kato import KatoSpider
from .spiders.nineanime import NineanimeSpider
from .spiders.yugen import YugenSpider
from .spiders.zoro import ZoroSpider

from .functions.metadataFunc import getMetadata



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
    def post_process(self):
        with open("results.json", "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                return False
        with open("process-results.json", "w+") as anime_results:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            anime_results.write('{"data":[')
            is_first_item = True
            for key, value in data.items():
                data = getMetadata(key, value)
                if is_first_item:
                    is_first_item = False
                else:
                    anime_results.write(',')
                json.dump(data, anime_results, indent=4)
            anime_results.write(f'],"last_run":"{timestamp}"}}')
        return True
    def upload(self):
        pass





