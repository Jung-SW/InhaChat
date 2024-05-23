import json
import os
def write_json(page, filename="everytime2024y.json",):
    with open(filename, "r+", encoding="utf-8") as file:
        file_content = json.load(file)
        if page not in file_content["everytime"]:
            file_content["everytime"].append(page)
        file.seek(0)
        json.dump(file_content, file, ensure_ascii=False, indent=4)