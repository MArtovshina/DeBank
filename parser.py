import os
import json
import time

import requests


def parse():
    url = "https://api.debank.com/feed/search?q=draw&start=0&limit=100&order_by=-create_at"
    response = requests.get(url)
    response_json = response.json()

    if os.path.exists("draw_data.json") and os.path.getsize("draw_data.json") > 0:
        with open("draw_data.json", "r") as json_file:
            draw_data = json.load(json_file)
    else:
        draw_data = []

    for item in response_json["data"]["feeds"]:
        draw = item["article"]["draw"]
        if draw:
            draw_id = draw["id"]
            draw_creator_id = item["article"]["creator"]["id"]
            draw_start = draw["create_at"]
            if draw["prize_value"] is not None:
                draw_prize_value = draw["prize_value"] / 10000
            else:
                draw_prize_value = 0
            draw_prize_count = draw["prize_count"]
            draw_operations = draw["operations"]
            draw_permissions = draw["permissions"]
            draw_end = draw["finish_at"]

            draw_entry = {
                "draw_id": draw_id,
                "draw_creator_id": draw_creator_id,
                "draw_start": draw_start,
                "draw_prize_value": draw_prize_value,
                "draw_prize_count": draw_prize_count,
                "draw_operations": draw_operations,
                "draw_permissions": draw_permissions,
                "draw_end": draw_end
            }

            draw_data.append(draw_entry)

    unique_list = []
    seen_ids = set()

    for item in draw_data:
        if item['draw_id'] not in seen_ids:
            unique_list.append(item)
            seen_ids.add(item['draw_id'])

    for i in range(0, len(unique_list) - 1):
        for j in range(0, len(unique_list) - 1):
            if unique_list[j]["draw_prize_value"] < unique_list[j + 1]["draw_prize_value"]:
                unique_list[j], unique_list[j + 1] = unique_list[j + 1], unique_list[j]

    for i in range(0, len(unique_list)):
        if unique_list[i]["draw_end"] < time.time():
            unique_list.remove(unique_list[i])

    with open("draw_data.json", "w") as json_file:
        json.dump(unique_list, json_file)


def main():
    while True:
        parse()
        time.sleep(600)


if __name__ == '__main__':
    main()
