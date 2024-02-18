from aiogram import Router

from .add_product import router as add_product_router
from .create_invoice import router as create_invoice_router
from .create_claim import router as create_claim_router
from .chat_with_manager import router as chat_with_manager_router
from .cancel_operation import router as cancel_operation_router
from ..filters import client_role

router: Router = Router()
router.include_router(add_product_router)
router.include_router(create_invoice_router)
router.include_router(create_claim_router)
router.include_router(chat_with_manager_router)
router.include_router(cancel_operation_router)

router.message.filter(client_role)

