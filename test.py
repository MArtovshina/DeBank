# import requests
# import time
#
#
# def get_operations(operations):
#     test = {
#         "follow_creator": "Подписаться на автора"
#     }
#     print("Задания:")
#     for _ in operations:
#         if operations[_]:
#             print(f"\t{test[_]}{operations[_]}")
#         else:
#             print(f"\t{test[_]}")
#
#
# def get_permissions(permissions):
#     test = {
#         'has_web3_id': "Владеть идентификатором Web3",
#         'min_age_days': "Возраст кошелька должен быть больше ",
#         'min_net_worth': "Капитал должен быть больше ",
#         'min_tvf': "TVF должен быть больше ",
#         'min_follower_count': "Подписчиков должно быть больше ",
#         'min_ranking': "Должен находиться в топ "
#     }
#     print("Условия участия:")
#     for _ in permissions:
#         if permissions[_]:
#             print(f"\t{test[_]}{permissions[_]}")
#         else:
#             print(f"\t{test[_]}")
#
#
# url = "https://api.debank.com/feed/search?q=draw&start=0&limit=100&order_by=-create_at"
# response = requests.get(url)
#
# response_text = response.json()
#
# list_ss = []
#
# for i in response_text['data']['feeds']:
#     try:
#         if i["article"]["draw"]['prize_value']:
#             list_ss.append(i)
#     except TypeError:
#         pass
#
# for i in range(0, len(list_ss) - 1):
#     for j in range(0, len(list_ss) - 1):
#         if list_ss[j]["article"]["draw"]['prize_value'] > list_ss[j + 1]["article"]["draw"]['prize_value']:
#             list_ss[j], list_ss[j + 1] = list_ss[j + 1], list_ss[j]
#
# for i in reversed(list_ss):
#     draw = i["article"]["draw"]
#     if float(draw['create_at']) < time.time() and 'has_web3_id' not in draw['permissions'].keys():
#         draw = i["article"]["draw"]
#         print(f"Ссылка: https://debank.com/stream/{i['article']['id']}")
#         print(f"Начало: {time.strftime('%d.%m.%Y %H:%M', time.localtime(float(draw['create_at'])))}")
#         try:
#             print(f"Награда: {int(draw['prize_value']) / 10000}$")
#         except TypeError:
#             print(f"Награда: None")
#         print(f"Количество победителей: {draw['prize_count']}")
#
#         get_operations(draw['operations'])
#
#         get_permissions(draw['permissions'])
#
#         print(f"Конец: {time.strftime('%d.%m.%Y %H:%M', time.localtime(float(draw['finish_at'])))}")
#         print("-" * 20)


# from seleniumwire import webdriver
# driver = webdriver.Chrome()
#
# # Go to the Google home page
# driver.get('https://debank.com/stream?q=draw&tab=search')
#
# # Access requests via the `requests` attribute
# for request in driver.requests:
#     if request.url == "https://api.debank.com/feed/suggested_tags?q=draw":
#         x_api_sign = request.headers["x-api-sign"]
#         x_api_nonce = request.headers["x-api-nonce"]
#         x_api_ts = request.headers["x-api-ts"]

# with open("draw_data.json", "r") as file:
#     draw = json.load(file)
#
# for line in draw:
#     if type(line['draw_creator_id']) == int:
#         print(line['draw_creator_id'])

# with open("draw_data.json", "r") as file:
#     draw = json.load(file)
#
# for line in draw:
#     permissions = line["draw_permissions"]
#
#     permissions["has_web3_id"] = 'has_web3_id' in permissions
#
#     print(permissions)


# from selenium import webdriver
# import time
#
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument(r"--user-data-dir=C:\Users\Tim\AppData\Local\Chromium\User Data")
# chrome_options.add_argument(r"--profile-directory=Default")
#
# browse_path = "C:/Users/Tim/Desktop/chromium-gost-118.0.5993.118/chrome.exe"
# chrome_options.binary_location = browse_path
#
# driver = webdriver.Chrome(options=chrome_options)
# driver.get("https://google.com")
# time.sleep(100000)

# from selenium import webdriver
#
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--user-data-dir=C:/Полный/Путь/К/Папке/User Data")
#
# driver = webdriver.Chrome(options=chrome_options)


test_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def ss(x):
    if x / 2 == 0:
        return x


new_list = list(map(ss, test_list))

print(new_list)
