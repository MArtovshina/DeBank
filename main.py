import os
import time
import pickle
import threading
from debank_request import Debank


def process_account(account_obj):
    print(f"Начал выполнять {account_obj._my_id}")
    account_obj.start()
    with open(f"accs/{account_obj._my_id}.pkl", "wb") as fp:
        pickle.dump(account_obj, fp)


def main():
    accounts = []

    with open('accs.txt', 'r') as file:
        lines = file.readlines()

    for line in lines:
        my_id, account = line.strip().split(';')
        account_file = f"{my_id}.pkl"

        if os.path.exists(f"accs/{account_file}"):
            print(f"Загрузил аккаунт: {my_id}")
            with open(f"accs/{account_file}", 'rb') as f:
                account_obj = pickle.load(f)
        else:
            print(f"Cоздал новый аккаунт {my_id}")
            account_obj = Debank(my_id, account)

        accounts.append(account_obj)

    while True:
        threads = []
        current_time = time.time()
        for account_obj in accounts:
            if current_time - account_obj.last_join_limit >= 24 * 3600:
                thread = threading.Thread(target=process_account, args=(account_obj,))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

        time.sleep(600)


if __name__ == '__main__':
    main()


# while True:
#     current_time = time.time()
#     for account_obj in accounts:
#         if current_time - account_obj.last_join_limit >= 24 * 3600:
#             print(f"Начал выполнять {account_obj._my_id}")
#             account_obj.start()
#             with open(f"accs/{account_obj._my_id}.pkl", "wb") as fp:
#                 pickle.dump(account_obj, fp)
#     time.sleep(300)
