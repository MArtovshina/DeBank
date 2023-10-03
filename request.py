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
        stat = resp_text["error_msg"]
        return stat

