from typing import Any, Callable

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import CallbackQuery, Message
from pydantic import BaseModel, ValidationError

from manager.handlers.chat_with_client import FSMChatWithClient
from services.client import ClientService


def get_update_schema_in_state_func(
        state_key: str, schema: BaseModel,
        exception_for_schema: ValueError,
) -> Callable:
    async def update_schema_in_state(
            state: FSMContext, schema_key: str, schema_value: Any,
            state_key: str = state_key, schema: BaseModel = schema,
            exception_for_schema: ValueError = exception_for_schema,
    ) -> dict:
        state_data = await state.get_data()

        if state_key not in state_data:
            schema_kwargs = {schema_key: schema_value}

            try:
                schema_inst = schema(**schema_kwargs)
            except ValidationError as e:
                raise exception_for_schema(str(e))

            state_kwargs = {state_key: schema_inst}
            await state.update_data(**state_kwargs)
            return schema_inst
        else:
            schema_inst_dict = state_data[state_key].model_dump(exclude_unset=True)
            schema_update_kwargs = {**schema_inst_dict, schema_key: schema_value}

            try:
                schema_updated_inst = schema(**schema_update_kwargs)
            except ValidationError as e:
                raise exception_for_schema(str(e))

            state_kwargs = {state_key: schema_updated_inst}
            await state.update_data(**state_kwargs)
            return schema_updated_inst

    return update_schema_in_state


async def set_manager_state_to_in_chat(manager_id: int, state: FSMContext):
    from manager.handlers.chat_with_client import FSMChatWithClient

    bot_id = state.key.bot_id
    manager_key = StorageKey(
        bot_id=bot_id,
        chat_id=manager_id,
        user_id=manager_id,
    )
    await state.storage.set_state(manager_key, FSMChatWithClient.in_chat)


async def notify_manager_about_claim(callback: CallbackQuery, bot: Bot):
    client_id = callback.from_user.id
    client_username = callback.from_user.username
    manager_id = await ClientService().get_manager_id(client_id)

    await bot.send_message(
        manager_id,
        f'у {client_username} появилась новая претензия',
    )

async def notify_manager_about_canceled_operation(message: Message, bot: Bot, state: FSMContext):
    client_id = message.from_user.id
    client_username = message.from_user.username
    manager_id = await ClientService().get_manager_id(client_id)

    canceled_fsm = (await state.get_state()).split(':')[0]

    if canceled_fsm == 'FSMAddProduct':
        canceled_operation = 'добавление продукта'
    elif canceled_fsm == 'FSMCreateClaim':
        canceled_operation = 'создание претензии'
    else:
        canceled_operation = 'создание накладной'

    await bot.send_message(
        manager_id,
        f'{client_username} не завершил {canceled_operation}',
    )