import requests
import scrapy
import zipfile
from scrapers.items import ScrapersItem
import os
import json

class MangafireSpider(scrapy.Spider):
    name = "mangafire"
    allowed_domains = ["homeonacloud.com"]
    start_urls = ["https://homeonacloud.com"]
    custom_settings = {
        "MANGAPIPELINE_ENABLED": True,
    }

    def parse(self, _):
        files = os.listdir("malSyncData/MAL-Sync-Backup-master/data/pages/MangaFire")
        mangaItem = ScrapersItem()
        for file in files:
            #open each json file
            try:
                with open(f"malSyncData/MAL-Sync-Backup-master/data/pages/MangaFire/{file}", "r") as f:
                    data = json.load(f)
                    mangaItem["title"] = data["title"]
                    mangaItem["link"] = {"MangaFire": data["url"]}
                    mangaItem["type"] = "Manga"
                    yield mangaItem
                f.close()
            except Exception:
                pass