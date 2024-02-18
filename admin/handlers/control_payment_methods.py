from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import Message

from admin.filters import admin_role
from services.payment_method import PaymentMethodService

router: Router = Router()


class FSMAddProduct(StatesGroup):
    add_payment_method = State()
    disable_payment_method = State()
    activate_payment_method = State()


@router.message(admin_role, Command(commands="list_payment_methods"))
async def list_payment_methods(message: Message):
    payment_methods = await PaymentMethodService().list_payment_methods()

    await message.answer(str(payment_methods))


@router.message(admin_role, Command(commands="add_payment_method"))
async def start_add_payment_method(message: Message, state: FSMContext):
    await state.set_state(FSMAddProduct.add_payment_method)
    await message.answer('Введите название способа оплаты')


@router.message(StateFilter(FSMAddProduct.add_payment_method))
async def add_payment_method(message: Message, state: FSMContext):
    payment_method_name = message.text
    await PaymentMethodService().add_payment_method(payment_method_name)

    await state.set_state(default_state)
    await message.answer('Способ оплаты добавлен')

