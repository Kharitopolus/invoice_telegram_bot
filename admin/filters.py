from aiogram.types import Message

from settings import settings


def admin_role(message: Message):
    return message.from_user.id == settings.bot_admin_id



