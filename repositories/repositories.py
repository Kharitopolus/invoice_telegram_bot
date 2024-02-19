from sqlalchemy import select, and_, func
from sqlalchemy.orm import joinedload

from models import Manager, Client
from models.claim import Claim
from models.invoice import Invoice, Product, Size, PaymentMethod
from models.user import Client
from repository import SQLAlchemyRepository


class ClientRepository(SQLAlchemyRepository):
    model = Client

    async def list_with_claims_for_manager(self, manager_id: int):
        stmt = (
            select(
                Client.id,
                Client.username,
                func.count(Client.id),
            )
            .join(Claim)
            .group_by(Client.id)
            .having(
                and_(
                    Client.manager_id == manager_id,
                    func.count(Client.id) > 0,
                )
            )
        )
        res = await self.session.execute(stmt)
        return res.all()


class InvoiceRepository(SQLAlchemyRepository):
    model = Invoice

    async def find_with_condition(self, condition: dict):
        stmt = (
            select(
                Invoice.id,
            )
            .filter_by(**condition)
        )
        res = await self.session.execute(stmt)
        return res.scalars().all()


class ClaimRepository(SQLAlchemyRepository):
    model = Claim


class ProductRepository(SQLAlchemyRepository):
    model = Product

    async def add_one(self, data: dict):
        data['size'] = Size(**data['size'])
        await super().add_one(data)


class PaymentMethodRepository(SQLAlchemyRepository):
    model = PaymentMethod


class ManagerRepository(SQLAlchemyRepository):
    model = Manager

    async def get_with_minimum_clients(self):
        query = (
            select(Manager.id, func.count(Client.id))
            .join(Client, isouter=True)
            .group_by(Manager.id)
            .order_by(func.count(Client.id))
            .limit(1)
        )
        res = await self.session.execute(query)
        return res.scalars().first()
