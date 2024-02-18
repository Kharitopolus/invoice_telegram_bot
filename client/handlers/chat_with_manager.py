from aiogram import Router, Bot
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import CallbackQuery, Message

from client.filters import enter_the_chat
from client.utils import set_manager_state_to_in_chat
from keyboards import enter_chat_keyboard
from services.client import ClientService
from utils import set_user_state_to_default

router: Router = Router()


class FSMChatWithManager(StatesGroup):
    in_chat = State()


@router.message(Command(commands="call_manager"))
async def call_manager(message: Message, bot: Bot):
    manager_chat = (
        await ClientService()
        .activate_chat_with_manager(client_id=message.from_user.id)
    )

    await bot.send_message(
        manager_chat,
        f'{message.from_user.username} хочет с вами связаться',
        reply_markup=enter_chat_keyboard(invite_from_user_id=message.from_user.id),
    )


@router.callback_query(enter_the_chat)
async def accept_invite_to_chat(callback: CallbackQuery, bot: Bot, state: FSMContext):
    manager_id = await ClientService().get_manager_id(callback.from_user.id)

    await set_manager_state_to_in_chat(manager_id, state)
    await state.set_state(FSMChatWithManager.in_chat)
    await bot.send_message(
        manager_id,
        f'{callback.from_user.username} присоединился к чату',
    )


@router.message(Command(commands="end_chat"), StateFilter(FSMChatWithManager.in_chat))
async def end_chat(message: Message, bot: Bot, state: FSMContext):
    manager_id = await ClientService().get_manager_id(message.from_user.id)
    client_id = message.from_user.id
    await ClientService().deactivate_chat_with_manager(client_id)

    await set_user_state_to_default(manager_id, state)
    await state.set_state(default_state)
    await bot.send_message(manager_id, 'клиент завершил чат')


@router.message(StateFilter(FSMChatWithManager.in_chat))
async def send_message_to_manager(message: Message, bot: Bot):
    manager_chat = await ClientService().get_manager_id(message.from_user.id)

    await bot.send_message(manager_chat, message.text)
