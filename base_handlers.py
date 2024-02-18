from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from settings import settings
from services.client import ClientService
from services.manager import ManagerService

router: Router = Router()


@router.message(CommandStart())
async def add_client_to_db_if_not(message: Message):
    user_id, username = message.from_user.id, message.from_user.username

    if user_id == settings.bot_admin_id:
        return

    if await ManagerService().get_manager(user_id):
        return

    if await ClientService().get_client(user_id):
        return

    await ClientService().add_client(user_id, username)


@router.message(Command(commands="cancel"))
async def set_default_state(message: Message, state: FSMContext):
    if (await state.get_state()) is not None:
        await state.set_state(default_state)
        await message.answer('операция отменена')
