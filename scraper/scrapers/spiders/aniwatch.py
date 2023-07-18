import scrapy
from scrapers.items import ScrapersItem

class AniwatchSpider(scrapy.Spider):
    '''
    Scrapes Anime from Aniwatch
    '''
    name = "aniwatch"
    allowed_domains = ["aniwatch.to"]
    start_urls = ["https://aniwatch.to/az-list"]
    custom_settings = {
        "ANIMEPIPELINE_ENABLED": True,
    }

    def parse(self, response):
        totalPages = response.css("li.page-item ::attr(href)")[-1].get().split("=")[-1]
        currentPage = response.css("li.page-item.active a ::text").get()
        if totalPages and currentPage:
            if int(currentPage) == 1:
                for pageNumber in range(2, int(totalPages) + 1):
                    yield scrapy.Request(url=f"https://aniwatch.to/az-list?page={pageNumber}")
                    
        animeList = response.css("a.dynamic-name")
        animeItem = ScrapersItem()
        for anime in animeList:
            title = anime.attrib["title"]
            link = f"https://aniwatch.to{anime.attrib['href']}"
            animeItem["title"] = title
            animeItem["link"] = {"Aniwatch":link}
            animeItem["type"] = "Anime"
            yield animeItem
