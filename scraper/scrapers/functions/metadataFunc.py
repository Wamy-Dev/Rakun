from jikanpy import Jikan
import hashlib
import urllib.parse
import requests
import time

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
        "episodes_num": "EPISODES",
        "aired": "AIRED",
        "studio": "STUDIO",
        "external_links": ["EXTERNAL_LINKS", "EXTERNAL_LINKS"],
        "episodes": [{
            "title": "TITLE",
            "number": "NUMBER",
            "aired": "AIRED",
        }],
        "trailer": "TRAILERURL",
        "images": ["IMAGES", "IMAGES"],
        "nyaarss": ["NYAARSS"],
    }
}
'''
def getAnilistID(mal_id, item_type):
    try:
        query = '''query($id: Int, $type: MediaType){Media(idMal: $id, type: $type){id}}'''
        variables = {
            "id": mal_id,
            "type": item_type.upper()
        }
        ani_id = requests.post("https://graphql.anilist.co", json={"query": query, "variables": variables}).json()["data"]["Media"]["id"]
        return ani_id
    except Exception:
        print(f"########### ANI ID META ERROR: ID cannot be found for {mal_id}.")
        return None
def getStreamingLinks(data, links):
    streaming_links = []
    for item in links:
        for key, value in item.items():
            streaming_links.append({key: value})
    if data:
        for link in data:
            source = link["name"]
            link = link["url"]
            streaming_links.append({source: link})
    return streaming_links
def getCharactersVoiceActors(mal_id, item_type):
    characters = []
    voice_actors = []
    if item_type == "Anime" or item_type == "EroAnime":
        characters_data = jikan.anime(mal_id, extension="characters")["data"]
        time.sleep(1)
        for character in characters_data:
            characters.append(character["character"]["name"])
            for voiceActor in character["voice_actors"]:
                voice_actors.append(voiceActor["person"]["name"])
    elif item_type == "Manga" or item_type == "EroManga":
        characters_data = jikan.manga(mal_id, extension="characters")["data"]
        time.sleep(1)
        for character in characters_data:
            characters.append(character["character"]["name"])
    return {
        "characters": characters,
        "voice_actors": voice_actors
    }
def getTitles(data):
    titles = []
    for title in data["titles"]:
        titles.append(title["title"])
    return titles
def getTags(data):
    tags = []
    for each in data["genres"]:
        tags.append(each["name"])
    for each in data["themes"]:
        tags.append(each["name"])
    for each in data["demographics"]:
        tags.append(each["name"])
    return tags
def getStudios(data):
    studios = []
    for each in data["studios"]:
        studios.append(each["name"])
    return studios
def getEpisodes(mal_id, item_type):
    episodes = []
    if item_type == "Anime" or item_type == "EroAnime":
        episodes_data = jikan.anime(mal_id, extension="episodes")["data"]
        time.sleep(1)
        number = 1
        for episode in episodes_data:
            episodes.append({
                "title": episode["title"],
                "aired": episode["aired"],
                "number": number
            })
            number += 1
        return episodes
    else:
        return []
def getAuthors(data):
    authors = []
    for each in data["authors"]:
        authors.append(each["name"])
    return authors
def getJikanMetadata(mal_id, item_type, links):
    data = {}
    try:
        if item_type == "Anime" or item_type == "EroAnime":
            metadata = jikan.anime(mal_id, extension="full")
            time.sleep(1)
            # streaming links
            data["link"] = getStreamingLinks(metadata["data"]["streaming"], links)
        elif item_type == "Manga" or item_type == "EroManga":
            metadata = jikan.manga(mal_id, extension="full")
            readingLinks = []
            for item in links:
                for key, value in item.items():
                    readingLinks.append({key: value})
            data["link"] = readingLinks
            time.sleep(1)
        title = metadata["data"]["title"]
        data["poster"] = metadata["data"]["images"]["webp"]["large_image_url"]
        data["banner"] = None
        data["synopsis"] = metadata["data"]["synopsis"]
        data["tags"] = getTags(metadata["data"])
        data["score"] = metadata["data"]["score"]
        data["rank"] = metadata["data"]["rank"]
        data["status"] = metadata["data"]["status"]
        if item_type == "Anime" or item_type == "Eroanime":
            data["aired"] = metadata["data"]["aired"]
            data["episodes_num"] = metadata["data"]["episodes"]
            data["trailer"] = metadata["data"]["trailer"]["url"]
            data["episodes"] = getEpisodes(mal_id, item_type)
            characters_voiceactors = getCharactersVoiceActors(mal_id, item_type)
            data["characters"] = characters_voiceactors["characters"]
            data["voice_actors"] = characters_voiceactors["voice_actors"]
            data["studios"] = getStudios(metadata["data"])
        elif item_type == "Manga" or item_type == "Eromanga":
            characters_voiceactors = getCharactersVoiceActors(mal_id, item_type)
            data["characters"] = characters_voiceactors["characters"]
            data["published"] = metadata["data"]["published"]
            data["chapters"] = metadata["data"]["chapters"]
            data["volumes"] = metadata["data"]["volumes"]
            data["trailer"] = None
            data["authors"] = getAuthors(metadata["data"])
        data["external_links"] = metadata["data"]["external"]
        data["images"] = []
        data["nyaarss"] = f"https://sukebei.nyaa.si/?page=rss&q={urllib.parse.quote_plus(title)}&c=0_0&f=0" if item_type == "EroAnime" or item_type == "EroManga" else f"https://nyaa.si/?page=rss&q={urllib.parse.quote_plus(title)}&c=0_0&f=0"  # noqa: E501
        
        data["titles"] = getTitles(metadata["data"])
        data["content_type"] = metadata["data"]["type"]
        return data
    except Exception as e:
        print(f"########### JIKAN META ERROR: {e}")
        return None
def getMetadata(title, item_type, links, mal_id):
    if mal_id is None:
        return {
            "id": hashlib.md5((title + item_type).encode()).hexdigest(),
            "title": title,
            "titles": [], 
            "type": item_type,
            "content_type": "TV" if item_type == "Anime" or item_type == "EroAnime" else "Manga",
            "mal_id": None,
            "ani_id": None,
            "link": links,
            "metadata": {
                "poster": None,
                "banner": None,
                "synopsis": "This item does not have a synopsis.",
                "tags": [],
                "score": -1,
                "rank": -1,
                "status": "Finished Airing",
                "episodes": [],
                "aired": None,
                "external_links": [],
                "episodes_num": -1,
                "trailer": None,
                "images": [],
                "characters": [],
                "volumes": -1,
                "chapters": -1,
                "published": None,
                "authors": [],
                "voice_actors": [],
                "studios": None,
                "nyaarss": f"https://sukebei.nyaa.si/?page=rss&q={urllib.parse.quote_plus(title)}&c=0_0&f=0" if item_type == "EroAnime" or item_type == "EroManga" else f"https://nyaa.si/?page=rss&q={urllib.parse.quote_plus(title)}&c=0_0&f=0"  # noqa: E501
            }
        }
    else:
        data = {}
        data["id"] = hashlib.md5((title + item_type).encode()).hexdigest()
        data["title"] = title
        data["mal_id"] = mal_id
        data["ani_id"] = getAnilistID(mal_id, item_type)
        metadata = getJikanMetadata(mal_id, item_type, links)
        if metadata is None:
            return {
                "id": hashlib.md5((title + item_type).encode()).hexdigest(),
                "title": title,
                "titles": [], 
                "type": item_type,
                "content_type": "TV" if item_type == "Anime" or item_type == "EroAnime" else "Manga",
                "mal_id": None,
                "ani_id": None,
                "link": links,
                "metadata": {
                    "poster": None,
                    "banner": None,
                    "synopsis": "This item does not have a synopsis.",
                    "tags": [],
                    "score": -1,
                    "rank": -1,
                    "status": "Finished Airing",
                    "episodes": [],
                    "aired": None,
                    "external_links": [],
                    "episodes_num": -1,
                    "trailer": None,
                    "images": [],
                    "characters": [],
                    "volumes": -1,
                    "chapters": -1,
                    "published": None,
                    "authors": [],
                    "voice_actors": [],
                    "studios": None,
                    "nyaarss": f"https://sukebei.nyaa.si/?page=rss&q={urllib.parse.quote_plus(title)}&c=0_0&f=0" if item_type == "EroAnime" or item_type == "EroManga" else f"https://nyaa.si/?page=rss&q={urllib.parse.quote_plus(title)}&c=0_0&f=0"  # noqa: E501
                }
            }
        else:
            data["link"] = metadata["link"]
            data["titles"] = metadata["titles"]
            data["type"] = item_type
            data["content_type"] = metadata["content_type"]
            # remove link, content_type and titles from metadata
            metadata.pop("link")
            metadata.pop("content_type")
            metadata.pop("titles")
            data["metadata"] = metadata
            return data


