import scrapy
from scrapers.items import ScrapersItem

class YugenSpider(scrapy.Spider):
    name = "yugen"
    allowed_domains = ["yugen.to", "yugenanime.tv"]
    start_urls = ["https://yugenanime.tv/discover/"]
    custom_settings = {
        "ANIMEPIPELINE_ENABLED": True,
    }

    def parse(self, response):
        totalPages = response.css("li a.btn ::attr(href)")[1].get().split("=")[-1]
        currentPage = response.css("li div.btn-default ::text").get()
        if totalPages and currentPage:
            if int(currentPage) == 1:
                for pageNumber in range(2, int(totalPages) + 1):
                    yield scrapy.Request(
                        url=f"https://yugenanime.tv/discover/?page={pageNumber}")
                    
        animeList = response.css("a.anime-meta")
        animeItem = ScrapersItem()
        for anime in animeList:
            title = anime.attrib["title"]
            link = f"https://yugenanime.tv{anime.attrib['href']}"

            animeItem["title"] = title
            animeItem["link"] = {"Yugen":link}
            animeItem["type"] = "Anime"

            yield animeItem



