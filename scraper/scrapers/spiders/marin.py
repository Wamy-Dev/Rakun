import scrapy
from scrapers.items import ScrapersItem
import os
import json

class MarinSpider(scrapy.Spider):
    name = "marin"
    allowed_domains = ["homeonacloud.com"]
    start_urls = ["https://homeonacloud.com"]
    custom_settings = {
        "ANIMEPIPELINE_ENABLED": True,
    }

    def parse(self, _):
        files = os.listdir("malSyncData/malSyncData/MAL-Sync-Backup-master/data/pages/Marin")
        animeItem = ScrapersItem()
        for file in files:
            #open each json file
            try:
                with open(f"malSyncData/malSyncData/MAL-Sync-Backup-master/data/pages/Marin/{file}", "r") as f:
                    data = json.load(f)
                    animeItem["title"] = data["title"]
                    animeItem["link"] = {"Marin": data["url"]}
                    animeItem["type"] = "Anime"
                    yield animeItem
                f.close()
            except Exception:
                pass




