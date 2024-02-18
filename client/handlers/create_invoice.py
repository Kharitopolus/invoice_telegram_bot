from aiogram import Router, Bot
from aiogram.filters import Command, ExceptionTypeFilter
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, ErrorEvent

from client.exceptions import InvoiceSchemaException
from client.keyboards import choose_users_product_keyboard, choose_payment_method_keyboard
from keyboards import confirm_keyboard
from client.utils import get_update_schema_in_state_func
from client.schemas import InvoiceSchema
from services.invoice import InvoiceService

router: Router = Router()


class FSMCreateInvoice(StatesGroup):
    choose_product = State()
    fill_source_address = State()
    fill_destination_address = State()
    fill_payment_method = State()
    confirm_invoice = State()


update_invoice_data = get_update_schema_in_state_func(
    state_key='invoice',
    schema=InvoiceSchema,
    exception_for_schema=InvoiceSchemaException,
)


@router.message(Command(commands="create_invoice"))
async def start_creating_invoice(message: Message, state: FSMContext):
    await state.set_state(FSMCreateInvoice.choose_product)
    await message.answer(
        'Выберите продукт',
        reply_markup=(await choose_users_product_keyboard(message.from_user.id)),
    )


@router.callback_query(StateFilter(FSMCreateInvoice.choose_product))
async def choose_product(callback: CallbackQuery, state: FSMContext):
    await update_invoice_data(state, 'product_id', callback.data)

    await state.set_state(FSMCreateInvoice.fill_source_address)
    await callback.message.answer(
        'введите широту и долготу(два числа через пробел) адреса отправления'
    )


@router.message(StateFilter(FSMCreateInvoice.fill_source_address))
async def fill_source_address(message: Message, state: FSMContext):
    await update_invoice_data(state, 'source_address', message.text.split())

    await state.set_state(FSMCreateInvoice.fill_destination_address)
    await message.answer(
        'введите широту и долготу(два числа через пробел) адреса получения'
    )



@router.message(StateFilter(FSMCreateInvoice.fill_destination_address))
async def fill_destination_address(message: Message, state: FSMContext):
    await update_invoice_data(state, 'destination_address', message.text.split())

    await state.set_state(FSMCreateInvoice.fill_payment_method)
    await message.answer(
        'Выберите способ оплаты',
        reply_markup=(await choose_payment_method_keyboard()),
    )


@router.callback_query(StateFilter(FSMCreateInvoice.fill_payment_method))
async def fill_payment_method(callback: CallbackQuery, state: FSMContext):
    await update_invoice_data(state, 'payment_method_id', callback.data)

    await state.set_state(FSMCreateInvoice.confirm_invoice)
    await callback.message.answer(
        f'Подтвердите создание накладной',
        reply_markup=confirm_keyboard(),
    )


@router.callback_query(StateFilter(FSMCreateInvoice.confirm_invoice))
async def confirm_invoice(callback: CallbackQuery, state: FSMContext):
    invoice = await update_invoice_data(state, 'client_id', callback.from_user.id)
    invoice_id = await InvoiceService().add_invoice(invoice)
    invoice_pdf = await InvoiceService().invoice_to_pdf(invoice_id)

    await state.set_state(default_state)
    await callback.message.answer_document(invoice_pdf, caption='накладная сохранена')


@router.error(ExceptionTypeFilter(InvoiceSchemaException))
async def handle_invoice_errors(event: ErrorEvent):
    exception = str(event.exception)

    if ('source_address' in exception) or ('destination_address' in exception):
        await event.update.message.answer(
            'нужно ввести два числа',
        )
