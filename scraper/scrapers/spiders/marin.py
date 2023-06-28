import requests
import scrapy
import zipfile
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
        if (os.path.exists("malSyncData")):
            pass
        else:
            file = requests.get("https://github.com/MALSync/MAL-Sync-Backup/archive/refs/heads/master.zip")
            with open("master.zip", "wb") as f:
                f.write(file.content)
            f.close()
            with zipfile.ZipFile("master.zip", "r") as zip_ref:
                zip_ref.extractall("malSyncData")
            zip_ref.close()
        files = os.listdir("malSyncData/MAL-Sync-Backup-master/data/pages/Marin")
        animeItem = ScrapersItem()
        for file in files:
            #open each json file
            with open(f"malSyncData/MAL-Sync-Backup-master/data/pages/Marin/{file}", "r") as f:
                data = json.load(f)
                animeItem["title"] = data["title"]
                animeItem["link"] = {"Marin": data["url"]}
                animeItem["type"] = "Anime"
                yield animeItem




