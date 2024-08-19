import asyncio

from bs4 import BeautifulSoup


# =============================SecurityLabNews=============================
class SecurityParser:
    def __init__(self, parsing_url: str = "https://www.securitylab.ru/news/"):
        self.parsing_url: str = parsing_url

    async def get_few_news_to_db(self, search_elements: list, last_added_article_id: int):
        soup = BeautifulSoup(await self.fetch_html(self.parsing_url), "lxml")

        articles_cards = soup.find_all(search_elements[0], class_=search_elements[1])

        format_string = "%H:%M %Y.%m.%d"

        tasks = [
            self.add_article_to_db(*await self.parse_article(article, last_added_article_id, format_string))
            for article in articles_cards
        ]

        await asyncio.gather(*tasks)

    async def fetch_html(self, url):
        import aiohttp

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0"
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.text()

    async def parse_article(self, article, last_added_article_id, format_string):
        from datetime import datetime
        article_url = f'https://www.securitylab.ru{article.get("href")}'
        article_id = int(article_url.split("/")[-1][:-4])

        if article_id > last_added_article_id:
            article_title = article.find("h2", class_="article-card-title").text.strip()
            article_desc = article.find("p").text.strip()
            article_date_time = article.find("time").get("datetime")

            date_time = datetime.fromisoformat(article_date_time).strftime(format_string)

            return article_id, article_title, article_desc, date_time

    async def add_article_to_db(self, article_id, article_title, article_description, article_data):
        from db import Database
        async with Database('/home/phonik/PycharmProjects/NEws_Bot/database/db.db') as db:
            await db.add_article(article_id, article_title, article_description, article_data)


# ==================Системное==================


async def main():
    parser = SecurityParser("https://www.securitylab.ru/news/")

    await parser.get_few_news_to_db(["a", "article-card inline-card"], 535346)


if __name__ == "__main__":
    asyncio.run(main())
