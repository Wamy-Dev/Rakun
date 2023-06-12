# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapersItem(scrapy.Item):
    '''
    Creates a predefined item for the scraped data. 

    Required: 
        Link: The link to the anime, manga, etc.
        Title: The title of the anime, manga, etc.
        Type: The type of the anime, manga, etc.
        Source: The source of the anime, manga, etc.
    '''

    link = scrapy.Field()
    title = scrapy.Field()
    type = scrapy.Field()
    source = scrapy.Field()
