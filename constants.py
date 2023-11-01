from fake_useragent import UserAgent

PARSE_URL = "https://api.debank.com/feed/search?q=draw&start=0&limit=100&order_by=-create_at"

PARSE_HEADERS = {
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
DEFAULT_PERMISSIONS = {
    "has_web3_id": False,
    "min_age_days": 0,
    "min_net_worth": 0,
    "min_tvf": 0,
    "min_follower_count": 0,
    "min_ranking": 1000000000
}
