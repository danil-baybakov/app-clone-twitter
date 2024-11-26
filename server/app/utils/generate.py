from db.db import Base, async_session_maker  # noqa
from models.users import User
from sqlalchemy import insert, select

USERS = [
    {"name": "TestUser", "api_key": "test"},
    {"name": "Danil Baybakov", "api_key": "danil"},
    {"name": "Egor Egorov", "api_key": "egor"},
    {"name": "Sergey Sergeev", "api_key": "sergey"},
]


async def generate_users():
    """
    Функция генерирует список объектов пользователей и
    добавляет их в БД
    :return:
    """
    async with async_session_maker() as session:
        stmt = select(User)
        res = await session.execute(stmt)
        users = res.all()

        if not users:
            stmt = insert(User).values(USERS)
            await session.execute(stmt)
            await session.commit()


if __name__ == "__main__":
    ...
