from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.invoice import InvoiceService
from services.payment_method import PaymentMethodService
from services.product import ProductService


async def choose_users_product_keyboard(client_id: int):
    products_buttons = [
        InlineKeyboardButton(
            text=product.description,
            callback_data=str(product.id)
        )
        for product in (await ProductService().list_user_products(client_id))
    ]

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(*products_buttons, width=1)
    return kb_builder.as_markup()


async def choose_payment_method_keyboard():
    payment_methods_buttons = [
        InlineKeyboardButton(
            text=payment_method.name,
            callback_data=str(payment_method.id),
        )
        for payment_method in (await PaymentMethodService().list_active_payment_methods())
    ]

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(*payment_methods_buttons, width=1)
    return kb_builder.as_markup()


async def choose_users_invoice_keyboard(client_id: int):
    products_buttons = [
        InlineKeyboardButton(
            text=str(invoice_id),
            callback_data=str(invoice_id),
        )
        for invoice_id in (await InvoiceService().list_user_invoice_id(client_id))
    ]

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(*products_buttons, width=1)
    return kb_builder.as_markup()
