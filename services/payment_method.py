from database import async_session_maker
from repositories.repositories import PaymentMethodRepository
from client.schemas import PaymentMethodSchema
from unitofwork import UnitOfWork
from utils import model_to_text


class PaymentMethodService:
    def __init__(self):
        self.uow = UnitOfWork(
            async_session_maker,
            [
                PaymentMethodRepository,
            ],
        )

    async def add_payment_method(self, name):
        data = {'name': name}

        async with self.uow:
            await self.uow.payment_method.add_one(data)
            await self.uow.commit()

    async def list_payment_methods(self):
        async with self.uow:
            payment_method_models = await self.uow.payment_method.find_all()
            payment_method_schemas = [
                PaymentMethodSchema.model_validate(payment_method_model)
                for payment_method_model in payment_method_models
            ]
            return payment_method_schemas

    async def list_active_payment_methods(self):
        async with self.uow:
            condition = {'is_supported': True}
            payment_method_models = await self.uow.payment_method.find_with_condition(condition)
            payment_method_schemas = [
                PaymentMethodSchema.model_validate(payment_method_model)
                for payment_method_model in payment_method_models
            ]
            return payment_method_schemas

    async def payment_method_to_text(self, payment_method_id: int):
        async with self.uow:
            payment_method = await self.uow.payment_method.get_one(payment_method_id)

            attributes_aliases = {
                'name': 'способ оплаты',
                'is_supported': 'способ оплаты сейчас поддерживается',
            }

            attribute_value_converter = {
                'is_supported': lambda value: 'да' if value else 'нет',
            }

            payment_method_text = model_to_text(
                payment_method,
                attributes_aliases,
                attribute_value_converter,
            )

            return payment_method_text
