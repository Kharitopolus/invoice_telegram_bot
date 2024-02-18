import uuid
from decimal import Decimal

from database import Base
from sqlalchemy import ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship, MappedColumn


class Claim(Base):
    __tablename__ = 'claim'

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('client.id', ondelete="CASCADE")
    )
    invoice_id: Mapped[int] = MappedColumn(
        ForeignKey('invoice.id', ondelete="CASCADE")
    )
    contact_email: Mapped[str]
    description: Mapped[str]
    money_required: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    image_name: Mapped[str | None] = mapped_column(default=None)

    client: Mapped['Client'] = relationship(back_populates='claims')
    invoice: Mapped['Invoice'] = relationship(back_populates='claim')
