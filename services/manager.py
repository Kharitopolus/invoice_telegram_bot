from database import async_session_maker
from repositories.repositories import ManagerRepository
from unitofwork import UnitOfWork


class ManagerService:

    def __init__(self):
        self.uow = UnitOfWork(
            async_session_maker,
            [
                ManagerRepository,
            ],
        )

    async def get_manager(self, manager_id: int):
        async with self.uow:
            client = await self.uow.manager.get_one(manager_id)
            return client

    async def add_manager(self, manager_id: int):
        async with self.uow:
            data = {'id': manager_id}
            manager = await self.uow.manager.add_one(data)
            await self.uow.commit()

    async def delete_manager(self, manager_id: int):
        async with self.uow:
            await self.uow.manager.delete_one(manager_id)
            await self.uow.commit()

    async def list_managers(self):
        async with self.uow:
            managers = await self.uow.manager.find_all()
            return managers.all()
