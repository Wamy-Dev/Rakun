import scrapy
from scrapers.items import ScrapersItem
import requests

class KatoSpider(scrapy.Spider):
    name = "kato"
    allowed_domains = ["kato.to"]
    start_urls = ["https://kato.to/"]
    custom_settings = {
        "ANIMEPIPELINE_ENABLED": True,
    }

    def parse(self, _):
        # uses the api to get the anime list
        prelimData = requests.get(f"https://c.delusionz.xyz/meta/anilist/advanced-search").json()
        totalPages = prelimData["totalPages"]
        currentPage = 0

        while currentPage <= totalPages:
            animeData = requests.get(f"https://c.delusionz.xyz/meta/anilist/advanced-search?page={currentPage}&type=ANIME").json()
            for anime in animeData["results"]:
                title = anime["title"]["romaji"]
                link = f"https://kato.to/watch/slug?id=search&malId={anime['malId']}&ep=0"
                animeItem = ScrapersItem()
                animeItem["title"] = title
                animeItem["link"] = link
                animeItem["type"] = "Anime"
                animeItem["source"] = "Kato"
                yield animeItem
            currentPage += 1





