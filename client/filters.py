from aiogram.types import CallbackQuery, Message

from services.client import ClientService


async def client_role(message: Message):
    return await ClientService().get_client(message.from_user.id)


async def enter_the_chat(callback: CallbackQuery):
    return 'enter the chat' in callback.data
