from scrapers.runScraper import Scraper
from scrapers.functions.csvFunc import delete_csv # noqa F401
from scrapers.functions.downloadDependenciesFunc import download_dependencies # noqa F401


download_dependencies()
delete_csv()
scraper = Scraper()
scraper.run_spiders()
scraper.post_process()
scraper.upload()