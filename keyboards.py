from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def confirm_keyboard():
    confirm_button = InlineKeyboardButton(
        text='yes',
        callback_data='confirmed'
    )

    return InlineKeyboardMarkup(
        inline_keyboard=[[confirm_button]]
    )


def enter_chat_keyboard(invite_from_user_id: int | None = None):
    confirm_button = InlineKeyboardButton(
        text='enter the chat',
        callback_data=f'enter the chat {invite_from_user_id}'
    )

    return InlineKeyboardMarkup(
        inline_keyboard=[[confirm_button]]
    )
