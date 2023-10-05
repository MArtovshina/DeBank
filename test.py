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


