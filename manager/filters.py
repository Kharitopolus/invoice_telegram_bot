from aiogram.types import Message, CallbackQuery

from services.manager import ManagerService


async def manager_role(message: Message):
    return await ManagerService().get_manager(message.from_user.id)


def manager_enter_the_chat(callback: CallbackQuery):
    return 'enter the chat' in callback.data and callback.data.split()[-1] != 'None'
