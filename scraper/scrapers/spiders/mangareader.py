import scrapy
from scrapers.items import ScrapersItem

class MangareaderSpider(scrapy.Spider):
    name = 'mangareader'
    allowed_domains = ["mangareader.to"]
    start_urls = ["https://mangareader.to/az-list"]
    custom_settings = {
        'MANGAPIPELINE_ENABLED': True
    }

    def parse(self, response):
        totalPages = response.css("li.page-item a.page-link ::attr(href)")[-1].get().split("=")[-1]
        currentPage = response.css("li.page-item.active a.page-link ::text").get()
        if totalPages and currentPage:
            if int(currentPage) == 1:
                for pageNumber in range(2, int(totalPages) + 1):
                    yield scrapy.Request(url=f"https://mangareader.to/az-list?page={pageNumber}")

        mangaList = response.css("div.item-spc")
        mangaItem = ScrapersItem()
        for manga in mangaList:
            title = manga.css("div.manga-detail h3.manga-name ::attr(title)").get()
            link = manga.css("div.manga-detail h3.manga-name a ::attr(href)").get()
            mangaItem["title"] = title
            mangaItem["link"] = {"Mangareader": f"https://mangareader.to{link}"}
            mangaItem["type"] = "Manga"
            yield mangaItem
