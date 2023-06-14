from jikanpy import Jikan
import hashlib
jikan = Jikan()

'''
An end result should look like this:
{
    "id": "HASH",
    "title": "TITLE",
    "titles": ["EXTRA TITLES", "EXTRA TITLES"],
    "type": "TYPE",
    "mal_id": "MAL_ID",
    "ani_id": "ANI_ID",
    "link": {
        "source": "LINK",
        "source": "LINK"
    },
    "metadata": {
        "poster": "POSTERURL",
        "banner": "BANNERURL",
        "synopsis": "SYNOPSIS",
        "tags": ["TAGS", "TAGS"],
        "score": "SCORE",
        "rank": "RANK",
        "status": "STATUS",
        "episodes": "EPISODES",
        "aired": "AIRED",
        "external_links": ["EXTERNAL_LINKS", "EXTERNAL_LINKS"],
        "episodes": [{
            "title": "TITLE",
            "number": "NUMBER",
            "aired": "AIRED",
            "airdate": "AIRDATE",
        }],
        "trailers": ["TRAILERS", "TRAILERS"],
        "images": ["IMAGES", "IMAGES"],
        "nyaarss": ["NYAARSS"],
    }
}
'''
def getMetadata(item):
    if item["mal_id"] is None:
        return {
            "id": hashlib.md5((item["title"] + item["type"]).encode()).hexdigest(),
            "title": item["title"],
            "titles": [], 
            "type": item["type"],
            "mal_id": "",
            "ani_id": "",
            "link": item["link"],
            "metadata": {
                "poster": "",
                "banner": "",
                "synopsis": "This item does not have a synopsis.",
                "tags": [],
                "score": -1,
                "rank": -1,
                "status": "Finished Airing",
                "episodes": -1,
                "aired": "",
                "external_links": [],
                "episodes": [],
                "trailers": [],
                "images": [],
                "nyaarss": f"https://nyaa.si/?page=rss&q={item['title']}&c=0_0&f=0"
            }
        }
    else:
        return item
