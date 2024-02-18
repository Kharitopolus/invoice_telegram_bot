from pydantic import dataclasses
from database import Base
from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, composite
from geoalchemy2 import Geometry


class Invoice(Base):
    __tablename__ = 'invoice'

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('client.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    source_address = Column(Geometry('POINT'))
    destination_address = Column(Geometry('POINT'))
    payment_method_id: Mapped[int] = mapped_column(ForeignKey('payment_method.id'))

    client: Mapped['Client'] = relationship(back_populates='invoices')
    product: Mapped['Product'] = relationship(back_populates='invoices')
    payment_method: Mapped['PaymentMethod'] = relationship(back_populates='invoices')
    claim: Mapped['Claim'] = relationship(back_populates='invoice')



@dataclasses.dataclass
class Size:
    length: float
    width: float
    height: float


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('client.id'))
    description: Mapped[str]
    weight_kg: Mapped[float]
    size: Mapped[Size] = composite(
        mapped_column('length'),
        mapped_column('wigth'),
        mapped_column('height'),
    )

    invoices: Mapped[list[Invoice]] = relationship(back_populates='product')
    client: Mapped['Client'] = relationship(back_populates='products')


class PaymentMethod(Base):
    __tablename__ = 'payment_method'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    is_supported: Mapped[bool] = mapped_column(default=True)

    invoices: Mapped[list[Invoice]] = relationship(back_populates='payment_method')
