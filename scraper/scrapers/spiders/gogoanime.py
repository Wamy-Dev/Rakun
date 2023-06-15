import scrapy
from scrapers.items import ScrapersItem
import requests
from bs4 import BeautifulSoup

class GogoanimeSpider(scrapy.Spider):
    name = 'gogoanime'
    allowed_domains = ["gogoanime.lu", "gogoanime.bid", "gogoanime.dk", "gogoanime.tel", "gogoanime.ar", "gogoanime.pe", "gogoanime.vc", "gogoanime.cl", "gogoanime.hu"]  # noqa: E501
    start_urls = ["https://gogoanime.hu/anime-list.html"]
    custom_settings = {
        "ANIMEPIPELINE_ENABLED": True,
    }

    def parse(self, response):
        prelimData = requests.get("https://gogoanime.hu/anime-list.html?page=5000")
        soup = BeautifulSoup(prelimData.text, "html.parser")
        totalPages = soup.find("div", {"class": "pagination"}).find_all("a")[-1].text
        currentPage = response.css("li.selected a ::text").get()
        if totalPages and currentPage:
            if int(currentPage) == 1:
                for pageNumber in range(2, int(totalPages) + 1):
                    yield scrapy.Request(f"https://gogoanime.hu/anime-list.html?page={pageNumber}")

        animeList = response.css("ul.listing li a")
        animeItem = ScrapersItem()
        for anime in animeList:
            title = anime.css("::text").get()
            link = anime.attrib["href"]
            animeItem["title"] = title.strip()
            animeItem["link"] = {"Gogoanime":f"https://gogoanime.hu{link}"}
            animeItem["type"] = "Anime"
            yield animeItem


