import scrapy
from scrapers.items import ScrapersItem
import requests
from bs4 import BeautifulSoup

class GogoanimeSpider(scrapy.Spider):
    name = 'gogoanime'
    allowed_domains = ["gogoanime.cl", "gogoanime.hu", "gogoanime.gr", "gogoanime.movie", "gogoanime.ar", "gogoanime.dk", "gogoanime.ee", "gogoanime.lu", "gogoanime.so", "gogoanime.sk", "gogoanime.fi", "gogoanime.pe", "gogoanime.cm", "gogoanime.bid", "gogoanime.ai", "gogoanimehd.to"]  # noqa: E501
    start_urls = ["https://gogoanimehd.to/anime-list.html"]
    custom_settings = {
        "ANIMEPIPELINE_ENABLED": True,
    }

    def parse(self, response):
        prelimData = requests.get("https://gogoanimehd.to/anime-list.html?page=5000")
        soup = BeautifulSoup(prelimData.text, "html.parser")
        totalPages = soup.find("div", {"class": "pagination"}).find_all("a")[-1].text
        currentPage = response.css("li.selected a ::text").get()
        if totalPages and currentPage:
            if int(currentPage) == 1:
                for pageNumber in range(2, int(totalPages) + 1):
                    yield scrapy.Request(f"https://gogoanimehd.to/anime-list.html?page={pageNumber}")

        animeList = response.css("ul.listing li a")
        animeItem = ScrapersItem()
        for anime in animeList:
            title = anime.css("::text").get()
            link = anime.attrib["href"]
            animeItem["title"] = title.strip()
            animeItem["link"] = {"Gogoanime":f"https://gogoanimehd.to{link}"}
            animeItem["type"] = "Anime"
            yield animeItem


