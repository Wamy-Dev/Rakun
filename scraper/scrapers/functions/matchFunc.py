# every item will pass through here, and it will return the item with the proper name

# Powered by Jikan

from jikanpy import Jikan
from fuzzywuzzy import fuzz
jikan = Jikan()

def getMaxSimilarity(item_title, titles):
    max_similarity = 0
    best_title = None
    for title in titles:
        similarity = fuzz.ratio(item_title, title["title"])
        if similarity > max_similarity:
            max_similarity = similarity
            best_title = title["title"]
    return {"title":best_title, "mal_id":title["mal_id"]}

def matchName(item):
    item_title = item["title"]
    item_type = item["type"]
    try:
        search = jikan.search(item_type.lower(), item_title)
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