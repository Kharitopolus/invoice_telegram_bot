from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.types import Message, CallbackQuery

from manager.filters import manager_enter_the_chat
from manager.keyboards import select_active_chats
from keyboards import enter_chat_keyboard
from manager.utils import set_client_state_to_in_chat
from services.client import ClientService
from utils import set_user_state_to_default

router: Router = Router()


class FSMChatWithClient(StatesGroup):
    select_client = State()
    in_chat = State()


@router.message(Command(commands="show_active_chats"))
async def show_active_chats(message: Message, state: FSMContext):
    await state.set_state(FSMChatWithClient.select_client)
    await message.answer(
        'Нажмите не клиента чтобы отправить запрос на начало чата',
        reply_markup=(await select_active_chats(manager_id=message.from_user.id)),
    )


@router.callback_query(StateFilter(FSMChatWithClient.select_client))
async def select_client(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await state.update_data(
        client_chat_id=callback.data,
    )

    await bot.send_message(
        chat_id=callback.data,
        text='Менеджер готов начать с вами чат. Войти в чат?',
        reply_markup=enter_chat_keyboard(),
    )


@router.callback_query(manager_enter_the_chat)
async def accept_invite_to_chat(callback: CallbackQuery, bot: Bot, state: FSMContext):
    client_id = int(callback.data.split()[-1])
    await state.update_data(
        client_chat_id=client_id,
    )

    await set_client_state_to_in_chat(client_id, state)
    await state.set_state(FSMChatWithClient.in_chat)
    await bot.send_message(
        chat_id=client_id,
        text='Менеджер готов начать с вами чат. Войти в чат?',
        reply_markup=enter_chat_keyboard(),
    )


@router.message(Command(commands="end_chat"), StateFilter(FSMChatWithClient.in_chat))
async def end_chat(message: Message, bot: Bot, state: FSMContext):
    client_id = (await state.get_data())['client_chat_id']
    await ClientService().deactivate_chat_with_manager(client_id)

    await set_user_state_to_default(client_id, state)
    await state.set_state(default_state)
    await bot.send_message(client_id, 'менеджер завершил чат')


@router.message(StateFilter(FSMChatWithClient.in_chat))
async def send_message_to_client(message: Message, bot: Bot, state: FSMContext):
    client_id = (await state.get_data())['client_chat_id']

    await bot.send_message(client_id, message.text)
