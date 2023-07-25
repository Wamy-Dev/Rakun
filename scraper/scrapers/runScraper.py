from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
from pymongo import MongoClient
from appConfig import MONGODB_CONNECTION_URI, MEILISEARCH_API_KEY, MEILISEARCH_HOST
import meilisearch
import pandas as pd
import ast

# Anime
from .spiders.animeflix import AnimeflixSpider
from .spiders.animepahe import AnimePaheSpider
from .spiders.gogoanime import GogoanimeSpider
from .spiders.kato import KatoSpider
from .spiders.nineanime import NineanimeSpider
from .spiders.yugen import YugenSpider
from .spiders.aniwatch import AniwatchSpider
from .spiders.marin import MarinSpider

# Manga
from .spiders.mangadex import MangadexSpider
from .spiders.comick import ComickSpider
from .spiders.mangareader import MangareaderSpider
from .spiders.mangafox import MangafoxSpider
from .spiders.bato import BatoSpider
from .spiders.serimanga import SerimangaSpider
from .spiders.mangafire import MangafireSpider
from .spiders.manganato import ManganatoSpider
from .spiders.mangasee import MangaseeSpider

# Functions
from .functions.metadataFunc import getMetadata

client = MongoClient(MONGODB_CONNECTION_URI)
db = client["scraper"]
def createKey():
   searchclient = meilisearch.Client(MEILISEARCH_HOST, MEILISEARCH_API_KEY) 
   key = searchclient.create_key(
       options={
            'description':"PUBLIC SEARCH KEY",
            'actions': ['search','indexes.get','documents.get','stats.get','version'],
            'indexes': ['*'],
            'expiresAt': None
       })
   print(key)
def getTasks():
    searchclient = meilisearch.Client(MEILISEARCH_HOST, MEILISEARCH_API_KEY)
    return searchclient.get_tasks()
def setupMeilisearch(type):
    searchclient = meilisearch.Client(MEILISEARCH_HOST, MEILISEARCH_API_KEY)
    searchclient.delete_index(type)
    searchclient.create_index(type, {'primaryKey': 'id'})
    searchclient.index(type).update(primary_key="id")
    index = searchclient.index(type)
    index.delete_all_documents()
    if type == "Anime" or type == "Eroanime":
        # update searchable attributes
        index.update_settings({
            "distinctAttribute": "id",
            "searchableAttributes": [
                "title",
                "titles",
                "mal_id",
                "ani_id",
                "metadata.tags",
                "metadata.episodes",
                "metadata.characters",
                "metadata.voice_actors",
                "metadata.studios",
            ],
            "displayedAttributes": [
                "*",
            ]
        })
    elif type == "Manga" or type == "Eromanga":
        index.update_settings({
            "distinctAttribute": "id",
            "searchableAttributes": [
                "title",
                "titles",
                "mal_id",
                "ani_id",
                "metadata.tags",
                "metadata.authors",
            ],
            "displayedAttributes": [
                "*",
            ]
        })
    return index
def getAllMongo(type):
    database = db[type]
    return database.find({})
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
            MarinSpider,
            NineanimeSpider,
            YugenSpider,
            AniwatchSpider,
            MangadexSpider,
            ComickSpider,
            MangareaderSpider,
            MangafoxSpider,
            BatoSpider,
            SerimangaSpider,
            MangafireSpider,
            ManganatoSpider,
            MangaseeSpider,
        ]

    def run_spiders(self):
        for spider in self.spiders:
            self.process.crawl(spider)
        self.process.start()
    def post_process(self):
        data = pd.read_csv("results.csv")
        for row in data.values.tolist()[::-1]:
            title = row[0]
            item_type = row[1]
            links = ast.literal_eval(row[2])
            mal_id = int(row[3])
            if mal_id == -1:
                mal_id = None
            database = db[item_type]
            try:                
                item = getMetadata(title, item_type, links, mal_id)
                old_item = database.find_one({"title": item["title"]})
                if old_item is None:
                    database.insert_one(item)
                    print(f"########### DATABASE ADD: {item['title']}, {item['type']}, {item['mal_id']}")
                else:
                    if item["mal_id"] is None and old_item["mal_id"] is None:
                        print(f"########### DATABASE SKIP: {item['title']}, {item['type']}, {item['mal_id']} ")
                        pass
                    elif item["mal_id"] == old_item["mal_id"] is not None and item["mal_id"] is not None:
                        database.update_one({"mal_id": item["mal_id"]}, {"$set": item})
                        print(f"########### DATABASE UPDATE: {item['title']}, {item['type']}, {item['mal_id']}")
                    elif item["mal_id"] is not None and old_item["mal_id"] is None:
                        database.update_one({"title": item["title"]}, {"$set": item})
                        print(f"########### DATABASE UPDATE: {item['title']}, {item['type']}, {item['mal_id']}")
            except Exception as e:
                print(f"########### METADB ERROR: {e}")
                continue
        return True
    def upload(self):
        collections = ["Anime", "Manga"]
        for collection in collections:
            try:
                index = setupMeilisearch(collection)
                data = getAllMongo(collection)
                items = []
                for item in data:
                    item.pop("_id")
                    item["poster"] = item["metadata"]["poster"]
                    items.append(item)
                process = index.add_documents(items)
                print(process)
                print(f"########### MEILISEARCH UPLOAD: {collection}")
            except Exception as e:
                print(f"########### MEILISEARCH ERROR: {e}")
                continue




