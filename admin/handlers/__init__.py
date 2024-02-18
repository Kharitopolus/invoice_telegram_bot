from aiogram import Router

from .control_managers import router as control_managers_router
from .control_payment_methods import router as control_payment_methods_router

router: Router = Router()

router.include_router(control_managers_router)
router.include_router(control_payment_methods_router)