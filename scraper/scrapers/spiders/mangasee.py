import scrapy
from scrapers.items import ScrapersItem
import os
import json

class MangaseeSpider(scrapy.Spider):
    name = "mangasee"
    allowed_domains = ["homeonacloud.com"]
    start_urls = ["https://homeonacloud.com"]
    custom_settings = {
        "MANGAPIPELINE_ENABLED": True,
    }

    def parse(self, _):
        files = os.listdir("malSyncData/MAL-Sync-Backup-master/data/pages/MangaSee")
        mangaItem = ScrapersItem()
        for file in files:
            #open each json file
            try:
                with open(f"malSyncData/MAL-Sync-Backup-master/data/pages/MangaSee/{file}", "r") as f:
                    data = json.load(f)
                    mangaItem["title"] = data["title"]
                    mangaItem["link"] = {"MangaSee": data["url"]}
                    mangaItem["type"] = "Manga"
                    yield mangaItem
                f.close()
            except Exception:
                pass