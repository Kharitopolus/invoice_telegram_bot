from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.claim import ClaimService
from services.client import ClientService


async def select_active_chats(manager_id):
    active_chats_buttons = [
        InlineKeyboardButton(
            text=client.username,
            callback_data=str(client.id),
        )
        for client in (
            await ClientService()
            .list_attached_to_manager_clients_with_active_chat(manager_id)
        )
    ]

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(*active_chats_buttons, width=1)
    return kb_builder.as_markup()


async def select_clients_with_claims(manager_id):
    active_chats_buttons = [
        InlineKeyboardButton(
            text=f'{client_username}. жалоб: {claims_count}',
            callback_data=str(client_id),
        )
        for client_id, client_username, claims_count in (
            await ClientService()
            .list_attached_to_manager_clients_with_claims(manager_id)
        )
    ]

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(*active_chats_buttons, width=1)
    return kb_builder.as_markup()


async def select_claims(client_id):
    active_chats_buttons = [
        InlineKeyboardButton(
            text=claim.description,
            callback_data=str(claim.id),
        )
        for claim in (
            await ClaimService()
            .list_claims_for_client(client_id)
        )
    ]

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(*active_chats_buttons, width=1)
    return kb_builder.as_markup()

