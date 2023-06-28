import scrapy
from scrapers.items import ScrapersItem
import requests
from datetime import datetime
import time

# https://api.mangadex.org/docs/
# https://api.mangadex.org/docs/swagger.html

class MangadexSpider(scrapy.Spider):
    name = "mangadex"
    allowed_domains = ["mangadex.org"]
    custom_settings = {
        'MANGAPIPELINE_ENABLED': True
    }
    start_urls = ["https://mangadex.org"]

    def parse(self, _):
        currentYear = datetime.now().year
        mangaItem = ScrapersItem()
        for year in range(1928, currentYear + 1):
            offset = 0
            limit = 100
            valid = True
            while valid:
                mangaData = requests.get(
                    f"https://api.mangadex.org/manga?limit={limit}&offset={offset}&hasAvailableChapters=true&year={year}"
                )
                if mangaData.ok:
                    data = mangaData.json()
                    total = data["total"]
                    if total == 0:
                        valid = False
                    else:
                        scraped = 0
                        for manga in data["data"]:
                            try:
                                id = manga["id"]
                                attributes = manga["attributes"]
                                title = attributes["title"]["en"]
                                slug = attributes["links"]["ap"]
                                mangaItem["title"] = title
                                mangaItem["link"] = {"MangaDex": f"https://mangadex.org/title/{id}/{slug}"}
                                mangaItem["type"] = "Manga"
                                yield mangaItem
                                scraped += 1
                            except:
                                scraped += 1
                                continue
                        if scraped == limit:
                            offset += limit
                        if total == scraped:
                            valid = False
                else:
                    valid = False
                time.sleep(1)

