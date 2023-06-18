from scrapers.runScraper import Scraper
from scrapers.functions.jsonFunc import delete_json # noqa F401

# delete_json()
scraper = Scraper()
# scraper.run_spiders()
scraper.post_process()