import re
from abc import ABC
from abc import abstractmethod
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):

    def __init__(self):
        pass

    @abstractmethod
    async def add_one(self):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self):
        raise NotImplementedError

    @abstractmethod
    async def edit_one(self):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @classmethod
    @property
    def operate_name(cls):
        repository_suff_off = cls.__name__.replace("Repository", "")
        repository_suff_off_snake_case = (
            re.sub(r"(?<!^)(?=[A-Z])", "_", repository_suff_off).lower()
        )
        return repository_suff_off_snake_case


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict):
        row = self.model(**data)
        self.session.add(row)
        return row

    async def get_one(self, pk: int | UUID):
        model_inst = await self.session.get(self.model, pk)
        return model_inst

    async def edit_one(self, pk: int | UUID, data: dict):
        model_inst = await self.session.get(self.model, pk)
        for key, value in data.items():
            setattr(model_inst, key, value)
        self.session.add(model_inst)
        return model_inst

    async def delete_one(self, pk: int | UUID):
        model_inst = await self.session.get(self.model, pk)
        await self.session.delete(model_inst)
        return model_inst

    async def find_all(self):
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def find_with_condition(self, condition: dict):
        stmt = select(self.model).filter_by(**condition)
        res = await self.session.execute(stmt)
        return res.scalars().all()

