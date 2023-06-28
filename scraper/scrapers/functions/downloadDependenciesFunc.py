import zipfile
import requests
import os
import datetime
from tqdm import tqdm

def download_dependencies():
    if (os.path.exists("master.zip")):
        #check date of master.zip. If older than 1 week, delete and redownload
        date = datetime.datetime.fromtimestamp(os.path.getmtime("master.zip"))
        if (date < datetime.datetime.now() - datetime.timedelta(days=7)):
            os.remove("master.zip")
            print("Dependencies older than 1 week, redownloading...")
        else:
            print("Dependencies already downloaded and up to date.")
            return True
    file = requests.get("https://github.com/MALSync/MAL-Sync-Backup/archive/refs/heads/master.zip", stream=True)
    with open("master.zip", "wb") as f:
        with tqdm(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc="Downloading dependencies", total=int(file.headers['Content-Length'])) as progress:
            for chunk in file.iter_content(chunk_size=1024):
                f.write(chunk)
                progress.update(len(chunk))
    f.close()
    print("Downloaded dependencies, now extracting... please wait, this may take a while.")
    with zipfile.ZipFile("master.zip", "r") as zip_ref:
        zip_ref.extractall("malSyncData")
    zip_ref.close()
    print("Extracted dependencies and ready to scrape.")
    return True