# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exceptions import NotConfigured
from .functions.csvFunc import combine_item
from .functions.matchFunc import matchName

class AnimePipeline():

    collection = 'Anime'

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('ANIMEPIPELINE_ENABLED'):
            raise NotConfigured
        return cls()
    def open_spider(self, response):
        print(f"########### STARTED {response}")
        #send discord notification here
        pass
    def close_spider(self, response):
        print(f"########### FINISHED {response}")
        #send discord notification here
        pass
    def process_item(self, item, _):
        newItem = combine_item(matchName(item))
        return newItem
         
class EroAnimePipeline():

    collection = 'EroAnime'

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('EROANIMEPIPELINE_ENABLED'):
            raise NotConfigured
        return cls()
    def open_spider(self, _):
        pass
    def close_spider(self, _):
        pass
    def process_item(self, item, _):
        return item

class MangaPipeline():

    collection = 'Manga'

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('MANGAPIPELINE_ENABLED'):
            raise NotConfigured
        return cls()
    def open_spider(self, response):
        print(f"########### STARTED {response}")
        #send discord notification here
        pass
    def close_spider(self, response):
        print(f"########### FINISHED {response}")
        #send discord notification here
        pass
    def process_item(self, item, _):
        newItem = combine_item(matchName(item))
        return newItem
        # return item

class EroMangaPipeline():
    
        collection = 'EroManga'

        @classmethod
        def from_crawler(cls, crawler):
            if not crawler.settings.getbool('EROMANGAPIPELINE_ENABLED'):
                raise NotConfigured
            return cls()
        def open_spider(self, _):
            pass
        def close_spider(self, _):
            pass
        def process_item(self, item, _):
            return item
