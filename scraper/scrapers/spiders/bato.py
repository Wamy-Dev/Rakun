import scrapy
from scrapers.items import ScrapersItem

class BatoSpider(scrapy.Spider):
    name = 'bato'
    allowed_domains = ["wto.to", "mto.to","dto.to","hto.to","mangatoto.com","bato.to","batotoo.com","battwo.com","comiko.net","mangatoto.net","mangatoto.org","comiko.org","batocomic.com","batocomic.net","batocomic.org","readtoto.com", "readtoto.net","readtoto.org","xbato.com","xbato.net","xbato.org","zbato.com","zbato.net","zbato.org"]
    start_urls = ["https://bato.to/v3x-search"]
    custom_settings = {
        'MANGAPIPELINE_ENABLED': True
    }

    def parse(self, response):
        totalPages = response.css("a.mb-1.btn.btn-sm ::text").getall()[-1]
        currentPage = response.css("a.mb-1.btn.btn-sm ::text").getall()[0]
        if totalPages and currentPage:
            if int(currentPage) == 1:
                for pageNumber in range(2, int(totalPages) + 1):
                    yield scrapy.Request(url=f"https://bato.to/v3x-search?page={pageNumber}")

        mangaList = response.css("div.flex.border-b.border-b-base-200.pb-5")
        mangaItem = ScrapersItem()
        for manga in mangaList:
            title = manga.css("a.link-hover.link-pri span ::text").get()
            link = manga.css("a.link-hover.link-pri ::attr(href)").get()
            mangaItem["title"] = title.split("[")[0].strip().split("(")[0].strip()
            mangaItem["link"] = {"Bato": f"https://bato..to{link}"}
            mangaItem["type"] = "Manga"
            yield mangaItem
