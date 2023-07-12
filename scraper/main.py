from scrapers.runScraper import Scraper
from scrapers.functions.jsonFunc import delete_json # noqa F401
from scrapers.functions.downloadDependenciesFunc import download_dependencies # noqa F401


download_dependencies()
delete_json()
scraper = Scraper()
scraper.run_spiders()
scraper.post_process()
scraper.upload()