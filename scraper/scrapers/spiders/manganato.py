import requests
import scrapy
import zipfile
from scrapers.items import ScrapersItem
import os
import json

class ManganatoSpider(scrapy.Spider):
    name = "manganato"
    allowed_domains = ["homeonacloud.com"]
    start_urls = ["https://homeonacloud.com"]
    custom_settings = {
        "MANGAPIPELINE_ENABLED": True,
    }

    def parse(self, _):
        files = os.listdir("malSyncData/MAL-Sync-Backup-master/data/pages/MangaNato")
        mangaItem = ScrapersItem()
        for file in files:
            #open each json file
            try:
                with open(f"malSyncData/MAL-Sync-Backup-master/data/pages/MangaNato/{file}", "r") as f:
                    data = json.load(f)
                    mangaItem["title"] = data["title"]
                    mangaItem["link"] = {"MangaNato": data["url"]}
                    mangaItem["type"] = "Manga"
                    yield mangaItem
                f.close()
            except Exception:
                pass