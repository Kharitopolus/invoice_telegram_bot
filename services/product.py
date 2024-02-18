from database import async_session_maker
from repositories.repositories import ProductRepository
from client.schemas import ProductSchema
from unitofwork import UnitOfWork
from utils import model_to_text


class ProductService:

    def __init__(self):
        self.uow = UnitOfWork(
            async_session_maker,
            [
                ProductRepository,
            ],
        )

    async def add_product(self, product: ProductSchema):
        data = product.model_dump(exclude_unset=True)

        async with self.uow:
            await self.uow.product.add_one(data)
            await self.uow.commit()

    async def list_user_products(self, client_id: int):
        condition = {'client_id': client_id}
        async with self.uow:
            products_models = await self.uow.product.find_with_condition(condition)
            products_schemas = [
                ProductSchema.model_validate(product_model) for product_model in products_models
            ]
            return products_schemas

    async def product_to_text(self, product_id: int):
        async with self.uow:
            product = await self.uow.product.get_one(product_id)
            attributes_aliases = {
                'description': 'описание груза',
                'weight_kg': 'вес (кг) груза',
                'length': 'длинна груза',
                'wigth': 'ширина груза',
                'height': 'высота груза',
            }
            product_text = model_to_text(
                product,
                attributes_aliases,
            )
            return product_text

