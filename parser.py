import os
import json
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from fake_useragent import UserAgent

headers = {
    'authority': 'api.debank.com',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json',
    'origin': 'https://debank.com',
    'referer': 'https://debank.com/',
    'user-agent': UserAgent().chrome,
    "x-api-ts": "1696466328",
    "x-api-nonce": "n_FlctTlTnrpnMtsGIuqiiUzAwnUhOpbP6qLv6HuEf",
    "x-api-sign": "e59d1c7ade8211a07daac25bfd3f8a9951748c477cda22f91c733855f750e389",
    "x-api-ver": "v2",
}

headers_2 = {
    "x-api-ts": "1696462606",
    "x-api-nonce": "n_6m7Q0geHdDF7zlWFG17TegKRCfgkKe7okmonz4lV",
    "x-api-sign": "6346053bf96d7519c3075d56424f439404cd17a82e3706ca6d4bce2767ce8097",
    "x-api-ver": "v2",
}


def reload_test():
    browser = webdriver.Chrome()
    browser.get('https://debank.com/stream?tab=hot')
    WebDriverWait(browser, 500).until(ec.element_to_be_clickable((By.XPATH, "//*[@data-mode=\"search\"]")))
    browser.quit()


def parse():
    url = "https://api.debank.com/feed/suggested_mentions?q=draw"

    requests.get(url, headers=headers_2)

    url = "https://api.debank.com/feed/search?q=draw&start=0&limit=100&order_by=-create_at"
    response = requests.get(url, headers=headers)

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

    # Удаление дублей
    unique_list = []
    seen_ids = set()

    for item in draw_data:
        if item['draw_id'] not in seen_ids:
            unique_list.append(item)
            seen_ids.add(item['draw_id'])

    # Сортировка по наградам
    for i in range(0, len(unique_list) - 1):
        for j in range(0, len(unique_list) - 1):
            if unique_list[j]["draw_prize_value"] < unique_list[j + 1]["draw_prize_value"]:
                unique_list[j], unique_list[j + 1] = unique_list[j + 1], unique_list[j]

    # Удаление закончившихся
    for i in range(0, len(unique_list)):
        try:
            if unique_list[i]["draw_end"] < time.time():
                unique_list.remove(unique_list[i])
        except IndexError:
            break

    with open("draw_data.json", "w") as json_file:
        json.dump(unique_list, json_file)


def main():
    while True:
        result = parse()
        if result is False:
            reload_test()
        time.sleep(10) if result is None else None


if __name__ == '__main__':
    main()
