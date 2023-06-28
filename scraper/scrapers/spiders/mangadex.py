import requests
import scrapy
import zipfile
from scrapers.items import ScrapersItem
import os
import json

class MangadexSpider(scrapy.Spider):
    name = "mangadex"
    allowed_domains = ["homeonacloud.com"]
    start_urls = ["https://homeonacloud.com"]
    custom_settings = {
        "MANGAPIPELINE_ENABLED": True,
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
        files = os.listdir("malSyncData/MAL-Sync-Backup-master/data/pages/Mangadex")
        mangaItem = ScrapersItem()
        for file in files:
            #open each json file
            try:
                with open(f"malSyncData/MAL-Sync-Backup-master/data/pages/Mangadex/{file}", "r") as f:
                    data = json.load(f)
                    mangaItem["title"] = data["title"]
                    mangaItem["link"] = {"Mangadex": data["url"]}
                    mangaItem["type"] = "Manga"
                    yield mangaItem
                f.close()
            except:
                pass

