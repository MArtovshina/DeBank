import requests
from fake_useragent import UserAgent


class DebankAPI:
    def __init__(self, account):
        self.headers = {
            'authority': 'api.debank.com',
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'account': str(account),
            'content-type': 'application/json',
            'origin': 'https://debank.com',
            'referer': 'https://debank.com/',
            'user-agent': UserAgent().chrome,
        }

    def follow(self, to_id=None):
        json_data = {
            'to_id': to_id,
        }

        response = requests.post('https://api.debank.com/user/follow_v2', headers=self.headers, json=json_data)

        print(f"статус запроса - {response.status_code}")
        resp_text = response.json()
        stat = resp_text["data"]["is_success"]
        if stat:
            print("Подписался")
        else:
            print("Уже подписан")

    def unfollow(self, to_id=None):
        json_data = {
            'to_id': to_id,
        }

        response = requests.post('https://api.debank.com/user/unfollow_v2', headers=self.headers, json=json_data)

        print(response.status_code)
        print(response.text)

    def draw_join(self, join_id=None):
        json_data = {
            'id': join_id,
        }

        response = requests.post('https://api.debank.com/feed/draw/join', headers=self.headers, json=json_data)

        print(f"статус запроса - {response.status_code}")
        resp_text = response.json()
        if "error_msg" in resp_text:
            stat = resp_text["error_msg"]
            return stat
        print("Принял участие")

    def get_following_list(self, my_id=None):
        params = {
            'id': my_id,
            'start': '0',
            'limit': '100',
            'order_by': '-to_usd_value',
        }

        response = requests.get('https://api.debank.com/user/following_list', headers=self.headers, params=params)

        following_list = []

        print(f"статус запроса - {response.status_code}")
        if response.status_code == 200:
            following = response.json()
            for i in following['data']['following_list']:
                following_list.append(i['id'])
        return following_list

    def get_l2_balance(self, my_id=None):
        params = {
            'id': my_id,
        }

        response = requests.get('https://api.debank.com/user/l2_account', headers=self.headers, params=params)

        if response.status_code == 200:
            balance = response.json()
            print(f"Account: {balance['data']['id']}, balance: {balance['data']['balance']}")
        return
