from aiogram import Router

from .chat_with_client import router as chat_with_client_router
from .show_claims import router as show_claims_router
from ..filters import manager_role

router: Router = Router()
router.include_router(chat_with_client_router)
router.include_router(show_claims_router)
router.message.filter(manager_role)

