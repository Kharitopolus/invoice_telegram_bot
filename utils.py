from typing import Callable

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import BufferedInputFile
from reportlab.lib.pagesizes import A5
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

from models import Invoice


async def set_user_state_to_default(user_id: int, state: FSMContext):
    bot_id = state.key.bot_id
    user_key = StorageKey(
        bot_id=bot_id,
        chat_id=user_id,
        user_id=user_id,
    )
    await state.storage.set_state(user_key, default_state)


def model_to_text(
        model,
        attributes_aliases: dict[str, str],
        attribute_value_converter: dict[str, Callable] = {},
) -> str:
    model_text = ''
    for attribute, alias in attributes_aliases.items():

        if attribute in attribute_value_converter:
            converter = attribute_value_converter[attribute]
            attribute_text = converter(getattr(model, attribute))
        else:
            attribute_text = getattr(model, attribute)

        model_text += f'{alias}:   {attribute_text}\n'

    return model_text


def text_to_pdf(filename: str, text: str):
    pdfmetrics.registerFont(TTFont('Miroslav', 'MIROSLN.ttf'))
    canvas = Canvas(filename)
    canvas.setFont('Miroslav', 20)
    for i, line in enumerate(text.split('\n')):
        canvas.drawString(30, 800 - i * 50, line)

    return BufferedInputFile(canvas.getpdfdata(), filename=filename)
