import requests


# сбрасывает лимит на запросы, использовать перед другими запросами
def pre_request():
    headers = {
        "x-api-ts": "1696462606",
        "x-api-nonce": "n_6m7Q0geHdDF7zlWFG17TegKRCfgkKe7okmonz4lV",
        "x-api-sign": "6346053bf96d7519c3075d56424f439404cd17a82e3706ca6d4bce2767ce8097",
        "x-api-ver": "v2",
    }

    url = "https://api.debank.com/feed/suggested_mentions?q=draw"

    requests.get(url, headers=headers)
