import os
import json
import time

import requests
import constants as const
from utils import pre_request, get_new_headers


def parse():
    pre_request()
    response = requests.get(const.PARSE_URL, headers=const.PARSE_HEADERS)

    if response.status_code == 429:
        print("Превышен лимит запросов")
        return False

    response_json = response.json()

    if os.path.exists("draw_data.json") and os.path.getsize("draw_data.json") > 0:
        with open("draw_data.json", "r") as json_file:
            draw_data = json.load(json_file)
    else:
        draw_data = []

    for item in response_json["data"]["feeds"]:
        draw = item["article"]["draw"]
        if draw:
            draw_url = f"https://debank.com/stream/{item['article_id']}"
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
                "draw_url": draw_url,
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

    # Удаление дублей
    unique_list = []
    seen_ids = set()

    for item in draw_data:
        if item['draw_id'] not in seen_ids:
            unique_list.append(item)
            seen_ids.add(item['draw_id'])

    # Удаление закончившихся
    for i in range(0, len(unique_list)):
        try:
            if unique_list[i]["draw_end"] < time.time() or type(unique_list[i]['draw_creator_id']) == int:
                unique_list.remove(unique_list[i])
        except IndexError:
            break

    # Удаление нулевых
    for i in range(0, len(unique_list)):
        try:
            if unique_list[i]["draw_prize_value"] == 0:
                unique_list.remove(unique_list[i])
        except IndexError:
            break

    # Сортировка по наградам
    for i in range(0, len(unique_list) - 1):
        for j in range(0, len(unique_list) - 1):
            if unique_list[j]["draw_prize_count"] < unique_list[j + 1]["draw_prize_count"]:
                unique_list[j], unique_list[j + 1] = unique_list[j + 1], unique_list[j]
    #
    # # Сортировка по наградам
    # for i in range(0, len(unique_list) - 1):
    #     for j in range(0, len(unique_list) - 1):
    #         if unique_list[j]["draw_prize_value"] < unique_list[j + 1]["draw_prize_value"]:
    #             unique_list[j], unique_list[j + 1] = unique_list[j + 1], unique_list[j]





    with open("draw_data.json", "w") as json_file:
        json.dump(unique_list, json_file)


def main():
    while True:
        result = parse()
        if result is False:
            get_new_headers()
        time.sleep(1800) if result is None else None


get_new_headers()

if __name__ == '__main__':
    main()
