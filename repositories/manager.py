from sqlalchemy import select, func

from models.user import Manager, Client
from repository import SQLAlchemyRepository


class ManagerRepository(SQLAlchemyRepository):
    model = Manager

    async def get_with_minimum_clients(self):
        # this is mock
        query = select(Manager).limit(1)

        # query = (
        #     select([Client.manager_id, func.count(1)]).
        #     group_by(Client.manager_id).
        #     order_by(func.count(Client.manager_id)).
        #     limit(1)
        # )
        res = await self.session.execute(query)
        return res.scalars().first()


