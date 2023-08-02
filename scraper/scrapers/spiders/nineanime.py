import scrapy
from scrapers.items import ScrapersItem

class NineanimeSpider(scrapy.Spider):
    name = 'nineanime'
    allowed_domains = ['9anime.to', "9anime.se", "aniwave.to"]
    start_urls = ['https://aniwave.to/az-list']
    custom_settings = {
        "ANIMEPIPELINE_ENABLED": True,
    }

    def parse(self, response):
        # get the link
        totalPages = response.css("li.page-item a.page-link")[-1].attrib["href"].split("=")[-1]  # noqa: E501
        currentPage = response.css("li.active span.page-link ::text").get()
        if totalPages and currentPage:
            if int(currentPage) == 1:
                for pageNumber in range(2, int(totalPages) + 1):
                    yield scrapy.Request(f"https://aniwave.to/az-list?page={pageNumber}")
        animeList = response.css("div#list-items div.item div.b1")
        animeItem = ScrapersItem()
        for anime in animeList:
            title = anime.css("a.name ::text").get()
            link = anime.css("a.name").attrib["href"]
            animeItem["title"] = title
            animeItem["link"] = {"Aniwave":f"https://aniwave.to{link}"}
            animeItem["type"] = "Anime"
            yield animeItem
