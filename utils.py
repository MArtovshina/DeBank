import requests
from seleniumwire import webdriver

# сбрасывает лимит на запросы, использовать перед другими запросами

headers = {
    "x-api-ts": "",
    "x-api-nonce": "",
    "x-api-sign": "",
    "x-api-ver": "v2",
}


def get_new_headers():
    driver = webdriver.Chrome()

    driver.get('https://debank.com/stream?q=draw&tab=search')

    for request in driver.requests:
        if request.url == "https://api.debank.com/feed/suggested_tags?q=draw":
            headers['x-api-sign'] = request.headers["x-api-sign"]
            headers['x-api-nonce'] = request.headers["x-api-nonce"]
            headers['x-api-ts'] = request.headers["x-api-ts"]


def pre_request():
    requests.get("https://api.debank.com/feed/suggested_tags?q=draw", headers=headers)

# class Prereq:
#1
#     def __init__(self):
#         self.x_api_ts = "1696558602"
#         self.x_api_nonce = "n_GEOUS13sfMUA4zp4Ha2nSh4hmHyE29mX1B07Feyd"
#         self.x_api_sign = "d5610937803427e9841ae65ec978a32a10215280b02c905cd95c5f735d427f30"
#
#         self.headers = {
#             "x-api-ts": self.x_api_ts,
#             "x-api-nonce": self.x_api_nonce,
#             "x-api-sign": self.x_api_sign,
#             "x-api-ver": "v2",
#         }
#
#     def pre_request(self):
#         requests.get("https://api.debank.com/feed/suggested_tags?q=draw", headers=self.headers)
#
#     def get_new_headers(self):
#         driver = webdriver.Chrome()
#         driver.get('https://debank.com/stream?q=draw&tab=search')
#
#         for request in driver.requests:
#             if request.url == "https://api.debank.com/feed/suggested_tags?q=draw":
#                 self.x_api_sign = request.headers["x-api-sign"]
#                 self.x_api_nonce = request.headers["x-api-nonce"]
#                 self.x_api_ts = request.headers["x-api-ts"]
