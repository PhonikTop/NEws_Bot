# import sqlite3

import asyncio
import aiosqlite


class Database:
    def __init__(self, db_file):
        self.db_file = db_file

    # async def __aenter__(self):
    #     self.connection = await aiosqlite.connect(self.db_file)
    #     self.cursor = self.connection.cursor()
    #     return self
    #
    # async def __aexit__(self, exc_type, exc, tb):
    #     await self.connection.commit()
    #     await self.connection.close()

    async def __aenter__(self):
        print(f"Attempting to connect to database at: {self.db_file}")
        self.connection = await aiosqlite.connect(self.db_file)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.connection.commit()
        await self.connection.close()

    async def user_exists(self, user_id):
        async with self.connection.execute(
                "SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)
        ) as cursor:
            result = await cursor.fetchmany(1)
            return bool(len(result))

    async def add_user(self, user_id):
        async with self.connection.execute(
                "INSERT INTO 'users' ('user_id') VALUES (?)", (user_id,)
        ):
            await self.connection.commit()

    async def set_active(self, user_id, active):
        async with self.connection.execute(
                "UPDATE `users` SET `active` = ? WHERE `user_id` = ?",
                (active, user_id)
        ):
            await self.connection.commit()

    async def get_users(self):
        async with self.connection.execute(
                "SELECT `user_id`, `active` FROM `users`"
        ) as cursor:
            return await cursor.fetchall()

    async def add_article(self, article_id, article_title, article_description, article_data):
        async with self.connection.execute(
                "INSERT INTO 'article' ('id', 'title', 'description', 'data') VALUES (?, ?, ?, ?)",
                (article_id, article_title, article_description, article_data)
        ):
            await self.connection.commit()


async def main():
    async with Database('/home/phonik/PycharmProjects/NEws_Bot/database/db.db') as db:
        exists = await db.user_exists(1)
        print(f'User exists: {exists}')
        await db.add_user(1)
        await db.set_active(1, True)
        users = await db.get_users()
        print(users)
        await db.add_article(1, 'Title', 'Description', 'Data')

if __name__ == '__main__':
    asyncio.run(main())