import json
import os

def save_to_json(items):
    with open("results.json", "w") as file:
        json.dump(items, file, indent=4)

def load_from_json():
    if os.path.exists("results.json"):
        with open("results.json", "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    else:
        return {}

def combine_item(item):
    title = item.get("title")
    item_type = item.get("type")
    link_data = item.get("link")
    item_mal_id = item.get("mal_id")

    key = json.dumps((title, item_type))
    previous_data = load_from_json()

    if key in previous_data:
        link_dict = previous_data[key].get("link", {})
        for source, link in link_data.items():
            link_dict[source] = link
    else:
        previous_data[key] = {
            "link": link_data
        }

    if item_mal_id is not None:
        previous_data[key]["mal_id"] = item_mal_id

    save_to_json(previous_data)


    











