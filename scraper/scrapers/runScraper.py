from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import json
from pymongo import MongoClient
from appConfig import MONGODB_CONNECTION_URI
client = MongoClient(MONGODB_CONNECTION_URI)
db = client["scraper"]
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
        for key, value in data.items():
            item_type = eval(key)[1]
            database = db[item_type]
            item = getMetadata(key, value)
            if database.find_one({"title": item["title"]}) is None:
                database.insert_one(item)
                print(f"########### DATABASE ADD: {item['title']}, {item_type}, {item['mal_id']}")
            else:
                #update item
                database.update_one({"title": item["title"]}, {"$set": item})
                print(f"########### DATABASE UPDATE: {item['title']}, {item_type}, {item['mal_id']}")
        return True
    def upload(self):
        pass





