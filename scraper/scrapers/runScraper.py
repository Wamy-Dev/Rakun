from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import json
from pymongo import MongoClient
from appConfig import MONGODB_CONNECTION_URI
# Anime
from .spiders.animeflix import AnimeflixSpider
from .spiders.animepahe import AnimePaheSpider
from .spiders.gogoanime import GogoanimeSpider
from .spiders.kato import KatoSpider
from .spiders.nineanime import NineanimeSpider
from .spiders.yugen import YugenSpider
from .spiders.zoro import ZoroSpider


# Functions
from .functions.metadataFunc import getMetadata

client = MongoClient(MONGODB_CONNECTION_URI)
db = client["scraper"]

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
            try:
                item_type = eval(key)[1]
                database = db[item_type]
                item = getMetadata(key, value)
                old_item = database.find_one({"title": item["title"]})
                if old_item is None:
                    database.insert_one(item)
                    print(f"########### DATABASE ADD: {item['title']}, {item['type']}, {item['mal_id']}")
                else:
                    if item["mal_id"] is None and old_item["mal_id"] is None:
                        print(f"########### DATABASE SKIP: {item['title']}, {item['type']}, {item['mal_id']} ")
                        pass
                    elif item["mal_id"] == old_item["mal_id"] is not None and item["mal_id"] is not None:
                        database.update_one({"title": item["title"]}, {"$set": item})
                        print(f"########### DATABASE UPDATE: {item['title']}, {item['type']}, {item['mal_id']}")
                    elif item["mal_id"] is not None and old_item["mal_id"] is None:
                        database.update_one({"title": item["title"]}, {"$set": item})
                        print(f"########### DATABASE UPDATE: {item['title']}, {item['type']}, {item['mal_id']}")
            except Exception as e:
                print(f"########### METADB ERROR: {e}")
                continue
        return True
    def upload(self):
        pass





