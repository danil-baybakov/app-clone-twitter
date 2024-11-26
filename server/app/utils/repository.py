from abc import ABC, abstractmethod
from typing import Optional

from db.db import async_session_maker
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import DeclarativeBase


class AbstractRepository(ABC):

    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def update_all_by_ids(self, ids: int, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def find_all_by_ids(self, ids: list[int]):
        raise NotImplementedError

    @abstractmethod
    async def find_one_or_none(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete_all(self, **kwargs):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model: Optional[DeclarativeBase] = None

    async def add_one(self, data: dict) -> int | None:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def find_all(self, **kwargs) -> list[BaseModel]:
        async with async_session_maker() as session:
            stmt = select(self.model).filter_by(**kwargs)
            res = await session.execute(stmt)
            rows = res.scalars().all()
            return [row for row in rows]

    async def update_all_by_ids(self, ids: int, **kwargs):
        async with async_session_maker() as session:
            stmt = (
                update(self.model)
                .filter(self.model.id.in_(ids))
                .values(**kwargs)
            )
            res = await session.execute(stmt)
            await session.commit()
            return res.rowcount > 0

    async def find_all_by_ids(self, ids: list[int]) -> list[BaseModel]:
        async with async_session_maker() as session:
            stmt = select(self.model).filter(self.model.id.in_(ids))
            res = await session.execute(stmt)
            rows = res.scalars().all()
            return [row for row in rows]

    async def delete_all(self, **kwargs) -> bool:
        async with async_session_maker() as session:
            stmt = delete(self.model).filter_by(**kwargs)
            res = await session.execute(stmt)
            await session.commit()
            return res.rowcount > 0

    async def find_one_or_none(self, **kwargs) -> BaseModel | None:
        try:
            async with async_session_maker() as session:
                stmt = select(self.model).filter_by(**kwargs)
                res = await session.execute(stmt)
                row = res.scalars().one_or_none()
                if row:
                    return row
        except Exception:  # noqa
            pass
