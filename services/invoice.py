from aiogram.types import BufferedInputFile
from geoalchemy2 import WKBElement, WKTElement
from geoalchemy2.shape import to_shape
from reportlab.pdfgen.canvas import Canvas

from database import async_session_maker
from repositories.repositories import InvoiceRepository
from client.schemas import InvoiceSchema
from services.payment_method import PaymentMethodService
from services.product import ProductService
from unitofwork import UnitOfWork
from utils import model_to_text, text_to_pdf


class InvoiceService:

    def __init__(self):
        self.uow = UnitOfWork(
            async_session_maker,
            [
                InvoiceRepository,
            ],
        )

    async def add_invoice(self, invoice: InvoiceSchema):
        data = invoice.model_dump(exclude_unset=True)

        async with self.uow:
            invoice = await self.uow.invoice.add_one(data)
            await self.uow.commit()
            return invoice.id

    async def get_invoice(self, invoice_id: int):
        async with self.uow:
            invoice = await self.uow.invoice.get_one(invoice_id)
            return invoice

    async def list_user_invoice_id(self, client_id: int):
        condition = {'client_id': client_id}
        async with self.uow:
            invoices_id = await self.uow.invoice.find_with_condition(condition)
            return invoices_id

    async def invoice_to_text(self, invoice_id: int):
        async with self.uow:
            invoice = await self.uow.invoice.get_one(invoice_id)
            attributes_aliases = {
                'source_address': 'координаты отправления',
                'destination_address': 'координаты получения',
            }
            attribute_value_converter = {
                'source_address': coordinates_converter,
                'destination_address': coordinates_converter,
            }
            invoice_text = model_to_text(
                invoice,
                attributes_aliases,
                attribute_value_converter,
            )
            product_text = await ProductService().product_to_text(invoice.product_id)
            payment_method_text = await PaymentMethodService().payment_method_to_text(
                invoice.payment_method_id,
            )
            return product_text + invoice_text + payment_method_text

    async def invoice_to_pdf(self, invoice_id: int):
        invoice_text = await self.invoice_to_text(invoice_id)
        invoice_pdf = text_to_pdf(f'invoice_{invoice_id}.pdf', invoice_text)
        return invoice_pdf


def coordinates_converter(coord_from_db: WKBElement | WKTElement):
    point = to_shape(coord_from_db)
    return f'широта {point.x}, долгота {point.y}'
