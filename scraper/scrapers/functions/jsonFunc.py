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

    if title is None or item_type is None or link_data is None:
        return

    link_key, link_value = next(iter(link_data.items()), (None, None))

    if link_key is None or link_value is None:
        return

    key = json.dumps((title, item_type))
    previous_data = load_from_json()
    if key in previous_data:
        previous_data[key].append(link_value)
    else:
        previous_data[key] = [link_value]
    save_to_json(previous_data)
    print("####################################DONE####################################")


    











