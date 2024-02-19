from functools import lru_cache

from database import async_session_maker
from repositories.repositories import ClientRepository, ManagerRepository
from schemas import ClientSchema
from unitofwork import UnitOfWork


class ClientService:

    def __init__(self):
        self.uow = UnitOfWork(
            async_session_maker,
            [
                ClientRepository,
                ManagerRepository,
            ],
        )

    async def add_client(self, client_id: int, client_username: str):
        async with self.uow:
            manager_id = await self.uow.manager.get_with_minimum_clients()
            data = dict(
                id=client_id,
                username=client_username,
                manager_id=manager_id
            )
            await self.uow.client.add_one(data)
            await self.uow.commit()

    async def get_client(self, client_id: int):
        async with self.uow:
            client = await self.uow.client.get_one(client_id)
            return client

    @lru_cache
    async def get_manager_id(self, client_id: int):
        async with self.uow:
            condition = {'id': client_id}
            client_model = (await self.uow.client.find_with_condition(condition))[0]
            manager_id = client_model.manager_id
            return manager_id

    async def activate_chat_with_manager(self, client_id: int):
        async with self.uow:
            data = {'is_chat_with_manager_active': True}
            client = await self.uow.client.edit_one(client_id, data)
            await self.uow.commit()
            return client.manager_id

    async def deactivate_chat_with_manager(self, client_id: int):
        async with self.uow:
            data = {'is_chat_with_manager_active': False}
            await self.uow.client.edit_one(client_id, data)
            await self.uow.commit()

    async def list_attached_to_manager_clients_with_active_chat(self, manager_id: int):
        async with self.uow:
            condition = {'manager_id': manager_id, 'is_chat_with_manager_active': True}
            client_models = await self.uow.client.find_with_condition(condition)
            client_schemas = [
                ClientSchema.model_validate(client_model)
                for client_model in client_models
            ]
            return client_schemas

    async def list_attached_to_manager_clients_with_claims(self, manager_id: int):
        async with self.uow:
            clients_id_username = await self.uow.client.list_with_claims_for_manager(manager_id)
            return clients_id_username
        



