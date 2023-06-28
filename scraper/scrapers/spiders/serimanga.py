import scrapy
from scrapers.items import ScrapersItem

class SerimangaSpider(scrapy.Spider):
    name = 'serimanga'
    allowed_domains = ["serimanga.com"]
    start_urls = ["https://serimanga.com/mangalar"]
    custom_settings = {
        'MANGAPIPELINE_ENABLED': True
    }

    def parse(self, response):
        totalPages = response.css("li.page-item a ::text").getall()[-2]
        currentPage = response.css("li.page-item.active span ::text").get()
        if totalPages and currentPage:
            if int(currentPage) == 1:
                for pageNumber in range(2, int(totalPages) + 1):
                    yield scrapy.Request(url=f"https://serimanga.com/mangalar?page={pageNumber}")

        mangaList = response.css("ul.sub-manga-list li a")
        mangaItem = ScrapersItem()
        for manga in mangaList:
            title = manga.css("span.mlb-name ::text").get()
            mangaItem["title"] = title
            mangaItem["link"] = {"Serimanga": manga.attrib["href"]}
            mangaItem["type"] = "Manga"
            yield mangaItem
