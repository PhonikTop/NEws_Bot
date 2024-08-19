import json
from datetime import datetime


def add_message(message):
    with open("log.json") as file:
        log = json.load(file)

    time = datetime.strftime(datetime.now(), "%H:%M:%S %Y.%m.%d")

    log[time] = {
        "Time": datetime.strftime(datetime.now(), "%H:%M:%S %Y.%m.%d"),
        "Message": message,
    }

    with open("log.json", "w") as file:
        json.dump(log, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    add_message(message="Пользователь @phoniktop отправил в канал сообщение: aaaa ")
