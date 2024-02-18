from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from client.handlers.chat_with_manager import FSMChatWithManager
from client.utils import notify_manager_about_canceled_operation

router: Router = Router()


@router.message(Command(commands="cancel"), ~StateFilter(FSMChatWithManager.in_chat))
async def set_default_state(message: Message, bot: Bot, state: FSMContext):
    if (await state.get_state()) is not None:
        await notify_manager_about_canceled_operation(message, bot, state)
        await state.set_state(default_state)
        await message.answer('операция отменена')
