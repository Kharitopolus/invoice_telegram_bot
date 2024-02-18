from abc import ABC
from abc import abstractmethod

from repository import AbstractRepository


class IUnitOfWork(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(IUnitOfWork):
    def __init__(self, session_factory, repositories: list[AbstractRepository]):
        self._session_factory = session_factory
        self._repositories = repositories

    async def __aenter__(self):
        self._session = self._session_factory()

        for repository in self._repositories:
            setattr(self, repository.operate_name, repository(self._session))

    async def __aexit__(self, *args):
        await self._session.rollback()
        await self._session.close()

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback
