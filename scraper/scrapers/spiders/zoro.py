import scrapy
from scrapers.items import ScrapersItem

class ZoroSpider(scrapy.Spider):
    '''
    Scrapes Anime from Zoro
    '''
    name = "zoro"
    allowed_domains = ["zoro.to"]
    start_urls = ["https://zoro.to/az-list"]
    custom_settings = {
        "ANIMEPIPELINE_ENABLED": True,
    }

    def parse(self, response):
        totalPages = response.css("li.page-item ::attr(href)")[-1].get().split("=")[-1]
        currentPage = response.css("li.page-item.active a ::text").get()
        if totalPages and currentPage:
            if int(currentPage) == 1:
                for pageNumber in range(2, int(totalPages) + 1):
                    yield scrapy.Request(
                        url=f"https://zoro.to/az-list?page={pageNumber}")
                    
        animeList = response.css("a.dynamic-name")
        animeItem = ScrapersItem()
        for anime in animeList:
            title = anime.attrib["title"]
            link = f"https://zoro.to{anime.attrib['href']}"
            animeItem["title"] = title
            animeItem["link"] = link
            animeItem["type"] = "Anime"
            animeItem["source"] = "Zoro"
            yield animeItem
