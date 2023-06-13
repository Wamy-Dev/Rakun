import scrapy
from scrapers.items import ScrapersItem
import requests

class AnimeflixSpider(scrapy.Spider):
    name = 'animeflix'
    allowed_domains = ['animeflix.live']
    start_urls = ['https://animeflix.live/']
    custom_settings = {
        "ANIMEPIPELINE_ENABLED": True,
    }

    def parse(self, _):
        # uses the api to get the anime list
        totalPages = 5000
        currentPage = 0

        while currentPage <= totalPages:
            animeData = requests.get(f"https://api.animeflix.live/series?page={currentPage}").json()
            if animeData == []:
                break
            for anime in animeData:
                title = anime["title"]["romaji"]
                link = f"https://animeflix.live/watch/{anime['slug']}-episode-1"
                animeItem = ScrapersItem()
                animeItem["title"] = title
                animeItem["link"] = {"Animeflix":link}
                animeItem["type"] = "Anime"
                yield animeItem
            currentPage += 1


