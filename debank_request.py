import time
import json
import requests
import constants as const
from fake_useragent import UserAgent
from utils import pre_request


class Debank:
    def __init__(self, my_id, account):
        self._my_id = my_id
        self._account = str(account)
        self._headers = {
            'authority': 'api.debank.com',
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'account': self._account,
            'content-type': 'application/json',
            'origin': 'https://debank.com',
            'referer': 'https://debank.com/',
            'user-agent': UserAgent().chrome,
        }
        self._CINF = {
            'has_web3_id': False,
            'my_age_days': None,
            'my_net_worth': None,
            'my_tvf': None,
            'my_follower_count': None,
            'my_ranking': None
        }
        self.list_joined = []
        self.last_join_limit = 0

    def get_cinf(self):
        pre_request()
        response = requests.get(f'https://api.debank.com/user?id={self._my_id}', headers=self._headers)
        resp_text = response.json()

        if resp_text["data"]["user"]["web3_id"]:
            self._CINF['has_web3_id'] = True
        else:
            self._CINF['has_web3_id'] = False

        self._CINF['my_age_days'] = int((time.time() - int(resp_text["data"]["user"]["desc"]["born_at"])) / 86400)
        self._CINF['my_net_worth'] = resp_text["data"]["user"]["stats"]["usd_value"]
        self._CINF['my_tvf'] = resp_text["data"]["user"]["tvf"]
        self._CINF['my_follower_count'] = resp_text["data"]["user"]["follower_count"]
        self._CINF['my_ranking'] = resp_text["data"]["user"]["rank_at"]

    def _follow(self, to_id=None):
        json_data = {
            'to_id': to_id,
        }

        response = requests.post('https://api.debank.com/user/follow_v2', headers=self._headers, json=json_data)

        print(f"статус запроса - {response.status_code}")
        resp_text = response.json()
        stat = resp_text["data"]["is_success"]
        if stat:
            print("Подписался")
        else:
            print("Уже подписан")

    def _unfollow(self, to_id=None):
        json_data = {
            'to_id': to_id,
        }

        response = requests.post('https://api.debank.com/user/unfollow_v2', headers=self._headers, json=json_data)

        print(response.status_code)
        print(response.text)

    def _draw_join(self, join_id=None):
        json_data = {
            'id': join_id,
        }

        response = requests.post('https://api.debank.com/feed/draw/join', headers=self._headers, json=json_data)

        print(f"статус запроса - {response.status_code}")
        resp_text = response.json()
        if "error_msg" in resp_text:
            stat = resp_text["error_msg"]
            return stat
        self.list_joined.append(join_id)
        print("Принял участие")

    def _get_following_list(self):
        params = {
            'id': self._my_id,
            'start': '0',
            'limit': '100',
            'order_by': '-to_usd_value',
        }

        response = requests.get('https://api.debank.com/user/following_list', headers=self._headers, params=params)

        following_list = []

        print(f"статус запроса - {response.status_code}")
        if response.status_code == 200:
            following = response.json()
            for i in following['data']['following_list']:
                following_list.append(i['id'])
        return following_list

    def get_l2_balance(self):
        params = {
            'id': self._my_id,
        }

        response = requests.get('https://api.debank.com/user/l2_account', headers=self._headers, params=params)

        if response.status_code == 200:
            balance = response.json()
            print(f"Account: {balance['data']['id']}, balance: {balance['data']['balance']}")

    def check_followers(self):
        pre_request()
        print("Проверка количества подписок")
        following_list = self._get_following_list()
        print(f"Количество подписок {len(following_list)}")
        if len(following_list) >= 90:
            for i in following_list:
                pre_request()
                self._unfollow(i)
                time.sleep(5)

    def complete_join(self):

        with open("draw_data.json", "r") as file:
            draw = json.load(file)

        for line in draw:
            permissions = line["draw_permissions"]

            if 'has_web3_id' in permissions:
                permissions["has_web3_id"] = True
            else:
                permissions["has_web3_id"] = False

            for key, value in const.DEFAULT_PERMISSIONS.items():
                if key not in permissions:
                    permissions[key] = value

            if self._CINF["has_web3_id"] == permissions["has_web3_id"] and \
                    self._CINF["my_age_days"] >= permissions["min_age_days"] and \
                    self._CINF["my_net_worth"] >= permissions["min_net_worth"] and \
                    self._CINF["my_tvf"] >= permissions["min_tvf"] and \
                    self._CINF["my_follower_count"] >= permissions["min_follower_count"] and \
                    self._CINF["my_ranking"] <= permissions["min_ranking"]:

                print(f"Начал подписку на {line['draw_creator_id']}")
                pre_request()
                self._follow(line["draw_creator_id"])
                time.sleep(5)

                print("Начал выполнение задания")
                pre_request()
                if line["draw_id"] in self.list_joined:
                    continue

                stat = self._draw_join(line["draw_id"])

                if stat == "You've hit your 24-hour join Lucky draw limit based on your Web3 Social Ranking":
                    print("Дневной лимит исчерпан")
                    self.last_join_limit = time.time()
                    break
                if stat == "user has joined":
                    print("Уже участвует")

                time.sleep(5)

    def start(self):
        self.get_cinf()
        self.check_followers()
        self.complete_join()
