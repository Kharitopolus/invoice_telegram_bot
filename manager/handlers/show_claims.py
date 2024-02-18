from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from manager.keyboards import select_clients_with_claims, select_claims
from services.claim import ClaimService

router: Router = Router()


class FSMShowClaims(StatesGroup):
    select_client = State()
    select_claim = State()


@router.message(Command(commands="show_clients_with_claims"))
async def show_clients_with_claims(message: Message, state: FSMContext):
    await state.set_state(FSMShowClaims.select_client)
    await message.answer(
        'Нажмите не клиента чтобы посмотреть его претензии',
        reply_markup=(await select_clients_with_claims(manager_id=message.from_user.id)),
    )


@router.callback_query(StateFilter(FSMShowClaims.select_client))
async def show_client_claims(callback: CallbackQuery, state: FSMContext):
    client_id = int(callback.data)

    await state.set_state(FSMShowClaims.select_claim)
    await callback.message.answer(
        'Нажмите на претензию чтобы посмотреть её',
        reply_markup=(await select_claims(client_id=client_id)),
    )


@router.callback_query(StateFilter(FSMShowClaims.select_claim))
async def show_client_claims(callback: CallbackQuery, state: FSMContext):
    claim_id = int(callback.data)
    claim_text, image_name = await ClaimService().claim_to_text(
        claim_id,
        with_image=True,
    )

    await state.set_state(FSMShowClaims.select_claim)
    await callback.message.answer_photo(
        image_name,
        caption=claim_text,
    )
