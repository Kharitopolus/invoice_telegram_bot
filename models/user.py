from sqlalchemy import ForeignKey, Integer, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from models.claim import Claim


class Client(Base):
    __tablename__ = "client"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str]
    manager_id: Mapped[int] = mapped_column(ForeignKey('manager.id'))
    is_chat_with_manager_active: Mapped[bool] = mapped_column(default=False)

    manager: Mapped['Manager'] = relationship(back_populates="clients")
    invoices: Mapped[list['Invoice']] = relationship(back_populates='client')
    claims: Mapped[list[Claim]] = relationship(back_populates='client')
    products: Mapped[list['Product']] = relationship(back_populates='client')


class Manager(Base):
    __tablename__ = "manager"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    clients: Mapped[list['Client']] = relationship(back_populates='manager')

