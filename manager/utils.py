from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey


async def set_client_state_to_in_chat(client_id: int, state: FSMContext):
    from client.handlers.chat_with_manager import FSMChatWithManager

    bot_id = state.key.bot_id
    client_key = StorageKey(
        bot_id=bot_id,
        chat_id=client_id,
        user_id=client_id,
    )
    await state.storage.set_state(client_key, FSMChatWithManager.in_chat)






