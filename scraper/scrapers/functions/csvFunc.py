import os
import pandas as pd
import ast

def load_from_csv():
    if not os.path.exists("results.csv"):
        return pd.DataFrame(columns=["title", "type", "link", "mal_id"])
    else:
        if pd.read_csv("results.csv").empty:
            return pd.DataFrame(columns=["title", "type", "link", "mal_id"])
        return pd.read_csv("results.csv")
    
def delete_csv():
    if os.path.exists("results.csv"):
        os.remove("results.csv")
        return True
    else:
        return False

def combine_item(item):
    title = item.get("title")
    item_type = item.get("type")
    link_data = item.get("link")
    item_mal_id = item.get("mal_id")
    df = load_from_csv()
    existing_row = df[(df['title'] == title) & (df['type'] == item_type)]
    if not existing_row.empty:
        previous = existing_row.iloc[0]["link"]
        previous = ast.literal_eval(previous)
        previous.append(link_data)
        df.loc[(df['title'] == title) & (df['type'] == item_type), "link"] = str(previous)
    else:
        new_row = pd.DataFrame({
            "title": [title],
            "type": [item_type],
            "link": [[link_data]],
            "mal_id": [item_mal_id]
        })
        df = pd.concat([df, new_row], ignore_index=True)
    df.fillna(-1, inplace=True)
    df.to_csv("results.csv", index=False)
    return {
        "title": title,
        "type": item_type,
        "link": link_data,
        "mal_id": item_mal_id
    }



    











