import scrapy
from scrapers.items import ScrapersItem

class MangafoxSpider(scrapy.Spider):
    name="mangafox"
    allowed_domains = ["fanfox.net"]
    start_urls = ["https://fanfox.net/directory/"]
    custom_settings = {
        'MANGAPIPELINE_ENABLED': True
    }

    def parse(self, response):
        totalPages = response.css("div.pager-list-left a ::text").getall()[-2]
        currentPage = response.css("div.pager-list-left a.active ::text").get()

        if totalPages and currentPage:
            if int(currentPage) == 1:
                for pageNumber in range(2, int(totalPages) + 1):
                    yield scrapy.Request(f"https://fanfox.net/directory/{pageNumber}.html")

        mangaList = response.css("div.manga-list-1 li p.manga-list-1-item-title")
        mangaItem = ScrapersItem()

        for manga in mangaList:
            link = manga.css("a ::attr(href)").get()
            mangaItem["title"] = manga.css("a ::attr(title)").get()
            mangaItem["link"] = {"MangaFox":f"https://fanfox.net{link}"}
            mangaItem["type"] = "Manga"
            yield mangaItem




