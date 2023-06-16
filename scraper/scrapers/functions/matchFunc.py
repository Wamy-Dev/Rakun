# every item will pass through here, and it will return the item with the proper name

# Powered by Jikan

from jikanpy import Jikan
from fuzzywuzzy import fuzz
import time
from pymongo import MongoClient
from appConfig import MONGODB_CONNECTION_URI

jikan = Jikan()
client = MongoClient(MONGODB_CONNECTION_URI)
db = client["scraper"]

def checkCache(item):
    item_title = item["title"]
    item_type = item["type"]
    collection_name = f"cache_{item_type.lower()}"
    try:
        collection = db[collection_name]
        data = collection.find_one({"webtitle": item_title})
        if data is None:
            return False
        else:
            return {
                "title": data["title"],
                "type": item_type,
                "link": item["link"],
                "mal_id": data["mal_id"]
            }
    except Exception as e:
        print(e)
        return False
    
def addToCache(item):
    item_title = item["title"]
    item_type = item["type"]
    collection_name = f"cache_{item_type.lower()}"
    try:
        collection = db[collection_name]
        collection.insert_one({
            "title": item_title,
            "webtitle": item["webtitle"],
            "mal_id": item["mal_id"]
        })
        print("####################### ADDED IN CACHE")
    except Exception as e:
        print(e)
        return False

def getMaxSimilarity(item_title, titles):
    max_similarity = 0
    best_title = None
    for title in titles:
        similarity = fuzz.token_sort_ratio(item_title, title["title"])
        if similarity == 100:
            return {"title":title["title"], "mal_id":title["mal_id"]}
        if similarity < 50:
            continue
        if similarity > max_similarity:
            max_similarity = similarity
            best_title = {"title":title["title"], "mal_id":title["mal_id"]}
    return best_title

def matchName(item):
    item_title = item["title"]
    item_type = item["type"]
    cache = checkCache(item)
    if cache:
        print("####################### FOUND IN CACHE")
        return cache
    else:
        try:
            search = jikan.search(item_type.lower(), item_title)
            time.sleep(1) # Jikan Public API has a limit of 60 requests per minute.
            similarTitles = []
            for anime in search["data"]:
                titles = []
                for title in anime["titles"]:
                    titles.append({"title": title["title"], "mal_id": anime["mal_id"]})
                similarTitles.append(getMaxSimilarity(item_title, titles))
            best_title = getMaxSimilarity(item_title, similarTitles)
            if best_title["title"] is None:
                return {
                    "title": item_title,
                    "type": item_type,
                    "link": item["link"],
                    "mal_id": None
                }
            else:
                addToCache({
                    "title": best_title["title"],
                    "webtitle": item_title,
                    "type": item_type,
                    "mal_id": best_title["mal_id"]
                })
                return {
                    "title": best_title["title"],
                    "type": item_type,
                    "link": item["link"],
                    "mal_id": best_title["mal_id"]
                }
        except Exception as e:
            print(e)
            return {
                "title": item_title,
                "type": item_type,
                "link": item["link"],
                "mal_id": None
            }