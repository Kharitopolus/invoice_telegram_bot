from aiogram import Router
from aiogram.filters import Command, ExceptionTypeFilter
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, ErrorEvent

from client.exceptions import ProductSchemaException
from keyboards import confirm_keyboard
from client.utils import get_update_schema_in_state_func
from client.schemas import ProductSchema
from services.product import ProductService

router: Router = Router()


class FSMAddProduct(StatesGroup):
    fill_product_description = State()
    fill_product_weight = State()
    fill_product_size = State()
    confirm_product = State()


update_product_data = get_update_schema_in_state_func(
    state_key='product',
    schema=ProductSchema,
    exception_for_schema=ProductSchemaException,
)


@router.message(Command(commands="add_product"))
async def start_adding_product(message: Message, state: FSMContext):
    await state.set_state(FSMAddProduct.fill_product_description)
    await message.answer(
        'Введите описание товара'
    )


@router.message(StateFilter(FSMAddProduct.fill_product_description))
async def fill_product_description(message: Message, state: FSMContext):
    await update_product_data(state, 'description', message.text)

    await state.set_state(FSMAddProduct.fill_product_weight)
    await message.answer(
        'Введите вес товара в килограммах'
    )


@router.message(StateFilter(FSMAddProduct.fill_product_weight))
async def fill_product_weight(message: Message, state: FSMContext):
    await update_product_data(state, 'weight_kg', message.text)

    await state.set_state(FSMAddProduct.fill_product_size)
    await message.answer(
        'Введите длину, ширину и высоту товара отделенные пробелом'
    )


@router.message(StateFilter(FSMAddProduct.fill_product_size))
async def fill_product_size(message: Message, state: FSMContext):
    await update_product_data(state, 'size', message.text.split())

    await state.set_state(FSMAddProduct.confirm_product)
    await message.answer(
        f'Подтвердите создание товара',
        reply_markup=confirm_keyboard(),
    )


@router.callback_query(StateFilter(FSMAddProduct.confirm_product))
async def confirm_product(callback: CallbackQuery, state: FSMContext):
    product = await update_product_data(state, 'client_id', callback.from_user.id)
    await ProductService().add_product(product)

    await state.set_state(default_state)
    await callback.message.answer('Продукт сохранен')


@router.error(ExceptionTypeFilter(ProductSchemaException))
async def handle_product_errors(event: ErrorEvent):
    exception = str(event.exception)

    if 'weight_kg' in exception:
        await event.update.message.answer('вес должен быть одним числом')

    if 'size' in exception:
        await event.update.message.answer(
            'нужно ввести три числа (длину, ширину и высоту) через пробел'
        )
