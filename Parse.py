import json

import requests
from bs4 import BeautifulSoup

from datetime import datetime

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0"
}


# =============================SecurityLabNews=============================


def SecurityLab_update():
    with open("dicts_files/news_dict.json") as file:
        news_dict = json.load(file)

    url = "https://www.securitylab.ru/news/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("a", class_="article-card")

    fresh_news = {}
    for article in articles_cards:
        article_url = f'https://www.securitylab.ru{article.get("href")}'
        article_id = article_url.split("/")[-1]
        article_id = article_id[:-4]

        if article_id in news_dict:
            continue
        else:
            article_title = article.find("h2", class_="article-card-title").text.strip()
            article_desc = article.find("p").text.strip()

            article_date_time = article.find("time").get("datetime")
            date_from_iso = datetime.fromisoformat(article_date_time)
            date_time = datetime.strftime(date_from_iso, "%H:%M %Y.%m.%d")

            news_dict[article_id] = {
                "Time": date_time,
                "Title": article_title,
                "Url": article_url,
                "Desc": article_desc,
                "Site": "Секьюрити лаб",
            }

            fresh_news[article_id] = {
                "article_date_timestamp": date_time,
                "article_title": article_title,
                "article_url": article_url,
                "article_desc": article_desc,
            }

    with open("dicts_files/news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news


# ===============================RiaTurkeyNews=============================


def get_RiaTurkey_update():
    url = "https://ria.ru/location_Turkey/"

    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    Contanier = soup.find_all("div", class_="list-item")

    rio_turkey_news = {}

    for obj in Contanier:
        items_title = f"{obj.find('a', class_='list-item__title color-font-hover-only').text.strip()}"
        items_date = f"{obj.find('div', class_='list-item__date').text.strip()}"

        items_url = f"{obj.find('a', class_='list-item__title color-font-hover-only').get('href')}"

        items_id = items_url.split("/")[-1]
        items_id = items_id[:-4]

        rio_turkey_news[items_id] = {
            "Title": items_title,
            "Url": items_url,
            "Time": items_date,
            "Site": "Риа новости турция",
        }

    with open("dicts_files/rio_Turkey_dict.json", "w") as file:
        json.dump(rio_turkey_news, file, indent=4, ensure_ascii=False)


# ===================================RiaNews=================================


def get_Ria_update():
    url = "https://ria.ru/incidents/"

    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    list_item = soup.find_all("div", class_="list-item")

    rio_news = {}

    for items in list_item:
        items_title = f"{items.find('a', class_='list-item__title color-font-hover-only').text.strip()}"
        items_date = f"{items.find('div', class_='list-item__date').text.strip()}"

        items_url = f"{items.find('a', class_='list-item__title color-font-hover-only').get('href')}"

        items_id = items_url.split("/")[-1]
        items_id = items_id[:-4]

        rio_news[items_id] = {
            "Title": items_title,
            "Url": items_url,
            "Time": items_date,
            "Site": "Риа Новости",
        }

    with open("dicts_files/rio_dict.json", "w") as file:
        json.dump(rio_news, file, indent=4, ensure_ascii=False)


# ==================================FreeSteam=================================


def get_Freesteam_update():
    url = "https://freesteam.ru/"

    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    list_items = soup.find_all("div", class_="col-lg-4 col-md-4 three-columns post-box")

    games_dict = {}

    for items in list_items:
        game_title = f"{items.find('h2', class_='entry-title').text.strip()}"
        news_tag = f"{items.find('span', class_='entry-cats').text.strip()}"

        article_time = (
            f"{items.find('time', class_='entry-date-human published').get('datetime')}"
        )
        date_from_iso = datetime.fromisoformat(article_time)
        date_time = datetime.strftime(date_from_iso, "%H:%M %Y.%m.%d")

        items_url = f"{items.find('a', rel='bookmark').get('href')}"[:-1]

        items_id = items_url.split("/")[-1]

        games_dict[items_id] = {
            "News": game_title,
            "Tags": news_tag,
            "Time": date_time,
            "Url": items_url,
            "Site": "Freesteam",
        }

    with open("dicts_files/games_sales.json", "w") as file:
        json.dump(games_dict, file, indent=4, ensure_ascii=False)


# ==================Системное==================


def main():
    get_Freesteam_update()
    SecurityLab_update()
    get_Ria_update()
    get_RiaTurkey_update()


if __name__ == "__main__":
    main()
