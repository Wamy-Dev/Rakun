import scrapy
from scrapers.items import ScrapersItem
import requests
from datetime import datetime
import time

# https://api.comick.fun/docs/static/index.html
class ComickSpider(scrapy.Spider):
    name = "comick"
    allowed_domains = ["comick.fun", "homeonacloud.com"]
    custom_settings = {
        'MANGAPIPELINE_ENABLED': True
    }
    start_urls = ["https://homeonacloud.com"]

    def parse(self, _):
        currentYear = datetime.now().year
        mangaItem = ScrapersItem()
        userAgent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        
        for year in range(1928, currentYear+1):
            page = 1
            valid = True
            while valid:
                mangaData = requests.get(f"https://api.comick.fun/v1.0/search?page={page}&from={year}&to={year}&type=comic&limit=50", headers={'User-Agent': userAgent})
                if mangaData.ok:
                    if len(mangaData.json()) == 0:
                        valid = False
                    else:
                        for manga in mangaData.json():
                            mangaItem["title"] = manga["title"]
                            mangaItem["link"] = {"Comick": f"https://comick.fun/comic/{manga['slug']}"}
                            mangaItem["type"] = "Manga"
                            yield mangaItem
                        page += 1
                        time.sleep(1)
                else:
                    valid = False

            
