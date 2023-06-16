import logging
BOT_NAME = 'scrapers'
SPIDER_MODULES = ['scrapers.spiders']
NEWSPIDER_MODULE = 'scrapers.spiders'
ROBOTSTXT_OBEY = False #LMAO
USER_AGENT = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
CONCURRENT_REQUESTS = 32
COOKIES_ENABLED = False
TELNETCONSOLE_ENABLED = False
EXTENSIONS = {
   'scrapy.extensions.telnet.TelnetConsole': None,
}
AUTOTHROTTLE_ENABLED = True

ITEM_PIPELINES = {
    'scrapers.pipelines.AnimePipeline': 200,
    'scrapers.pipelines.EroAnimePipeline': 201,
    'scrapers.pipelines.MangaPipeline': 202,
    'scrapers.pipelines.EroMangaPipeline': 203,
}

ANIMEPIPELINE_ENABLED = False
EROANIMEPIPELINE_ENABLED = False
MANGAPIPELINE_ENABLED = False
EROMANGAPIPELINE_ENABLED = False

LOG_ENABLED = False
logger = logging.getLogger('scrapy')
logger.setLevel(logging.WARNING)