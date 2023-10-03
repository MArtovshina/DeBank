import json
import time
from request import DebankAPI

cinf = {
    'has_web3_id': False,
    'my_age_days': 600,
    'my_net_worth': 101,
    'my_tvf': 120,
    'my_follower_count': 2,
    'my_ranking': 280000
}

default_permissions = {
    "has_web3_id": False,
    "min_age_days": 0,
    "min_net_worth": 0,
    "min_tvf": 0,
    "min_follower_count": 0,
    "min_ranking": 1000000000

}


def complete_task(profile):
    with open("draw_data.json", "r") as file:
        draw = json.load(file)

    for line in draw:
        permissions = line["draw_permissions"]

        if 'has_web3_id' in permissions:
            permissions["has_web3_id"] = True
        else:
            permissions["has_web3_id"] = False

        for key, value in default_permissions.items():
            if key not in permissions:
                permissions[key] = value

        if cinf["has_web3_id"] == permissions["has_web3_id"] and \
                cinf["my_age_days"] >= permissions["min_age_days"] and \
                cinf["my_net_worth"] >= permissions["min_net_worth"] and \
                cinf["my_tvf"] >= permissions["min_tvf"] and \
                cinf["my_follower_count"] >= permissions["min_follower_count"] and \
                cinf["my_ranking"] <= permissions["min_ranking"]:

            print(f"Начал подписку на {line['draw_creator_id']}")
            profile.follow(line["draw_creator_id"])
            time.sleep(60)

            print("Начал выполнение задание")
            stat = profile.draw_join(line["draw_id"])

            if stat == "You've hit your 24-hour join Lucky draw limit based on your Web3 Social Ranking":
                print("Дневной лимит исчерпан")
                break
            if stat != "user has joined":
                print("Принял участие")
            else:
                print("Уже участвует")

            time.sleep(60)


def main():
    # Сделать чтение из общей папки аккаунтов
    my_id = "0x41e4db5bee80d0dd6b44b6d80d3cac212583bff7"
    # сделать чтение из файла с параметрами
    account = '{"random_at":1685829887,"random_id":"f8c4750aa04f4db9a703abe33e310792","session_id":"531c88033bbd4d13b85a27b7703500c5","user_addr":"0x41e4db5bee80d0dd6b44b6d80d3cac212583bff7","wallet_type":"metamask","is_verified":true}'

    profile = DebankAPI(account)
    complete_task(profile)


if __name__ == '__main__':
    main()
