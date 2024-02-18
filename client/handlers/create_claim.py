from aiogram import Router, Bot
from aiogram.filters import Command, ExceptionTypeFilter
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, ErrorEvent

from client.exceptions import ClaimSchemaException
from client.keyboards import choose_users_invoice_keyboard
from keyboards import confirm_keyboard
from client.schemas import ClaimSchema
from client.utils import get_update_schema_in_state_func, notify_manager_about_claim
from services.claim import ClaimService

router: Router = Router()


class FSMCreateClaim(StatesGroup):
    choose_invoice = State()
    fill_contact_email = State()
    fill_description = State()
    fill_money_required = State()
    attach_images = State()
    confirm_claim = State()


update_claim_data = get_update_schema_in_state_func(
    state_key='claim',
    schema=ClaimSchema,
    exception_for_schema=ClaimSchemaException,
)


@router.message(Command(commands="create_claim"))
async def start_creating_invoice(message: Message, state: FSMContext):
    await state.set_state(FSMCreateClaim.choose_invoice)
    await message.answer(
        'Выберите накладную',
        reply_markup=(await choose_users_invoice_keyboard(message.from_user.id)),
    )


@router.callback_query(StateFilter(FSMCreateClaim.choose_invoice))
async def choose_invoice(callback: CallbackQuery, state: FSMContext):
    await update_claim_data(state, 'invoice_id', callback.data)

    await state.set_state(FSMCreateClaim.fill_contact_email)
    await callback.message.answer('введите контактный email')


@router.message(StateFilter(FSMCreateClaim.fill_contact_email))
async def fill_contact_email(message: Message, state: FSMContext):
    await update_claim_data(state, 'contact_email', message.text)

    await state.set_state(FSMCreateClaim.fill_description)
    await message.answer('опишите ситуацию')


@router.message(StateFilter(FSMCreateClaim.fill_description))
async def fill_description(message: Message, state: FSMContext):
    await update_claim_data(state, 'description', message.text)

    await state.set_state(FSMCreateClaim.fill_money_required)
    await message.answer('введите запрашиваемую сумму денег')


@router.message(StateFilter(FSMCreateClaim.fill_money_required))
async def fill_money_required(message: Message, state: FSMContext):
    await update_claim_data(state, 'money_required', message.text)

    await state.set_state(FSMCreateClaim.attach_images)
    await message.answer('отправьте фотографии')


@router.message(StateFilter(FSMCreateClaim.attach_images))
async def attach_images(message: Message, state: FSMContext):
    try:
        await update_claim_data(state, 'image_name', message.photo[0].file_id)
    except TypeError:
        raise ClaimSchemaException('image_name')

    await state.set_state(FSMCreateClaim.confirm_claim)
    await message.answer(
        f'Подтвердите создание претензии',
        reply_markup=confirm_keyboard(),
    )


@router.callback_query(StateFilter(FSMCreateClaim.confirm_claim))
async def confirm_claim(callback: CallbackQuery, bot: Bot, state: FSMContext):
    claim = await update_claim_data(state, 'client_id', callback.from_user.id)
    await ClaimService().add_claim(claim)

    await state.set_state(default_state)
    await notify_manager_about_claim(callback, bot)
    await callback.message.answer('претензия сохранена')


@router.error(ExceptionTypeFilter(ClaimSchemaException))
async def handle_claim_errors(event: ErrorEvent):
    exception = str(event.exception)

    if 'contact_email' in exception:
        await event.update.message.answer(
            'введите нормальный email',
        )

    if 'money_required' in exception:
        await event.update.message.answer(
            'нужно ввести число с точностью не более чем до сотых',
        )

    if 'image_name' in exception:
        await event.update.message.answer(
            'нужно отправить фотографию',
        )
