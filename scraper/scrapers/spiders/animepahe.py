import scrapy
from scrapers.items import ScrapersItem

class AnimePaheSpider(scrapy.Spider):
    name = "animepahe"
    allowed_domains = ["animepahe.com", "animepahe.org", "animepahe.ru"]
    start_urls = ["https://animepahe.ru/anime"]
    custom_settings = {
        "ANIMEPIPELINE_ENABLED": True,
    }

    def parse(self, response):
        # Doesn't need to worry about pagination as it is all there
        animeList = response.css("div.tab-pane div.col-12 a")
        animeItem = ScrapersItem()
        for anime in animeList:
            title = anime.attrib["title"]
            link = f"https://animepahe.ru{anime.attrib['href']}"

            animeItem["title"] = title
            animeItem["link"] = {"Animepahe":link}
            animeItem["type"] = "Anime"

            yield animeItem
