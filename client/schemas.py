from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, field_validator, ConfigDict, Field, EmailStr

from models import Size


class ProductSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    description: str | None = None
    weight_kg: float | None = None
    size: Size | None = None
    client_id: int | None = None

    @field_validator('size', mode='before')
    @classmethod
    def formatting_size(cls, size: list[str] | dict[str, float] | Size) -> Size:
        if type(size) is list:
            return Size(*size)

        return size


class InvoiceSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    client_id: int | None = None
    product_id: int | None = None
    source_address: str | None = Field(
        None,
        pattern=r"^POINT\([0-9]*\.[0-9]* [0-9]*\.[0-9]*\)$",
    )
    destination_address: str | None = Field(
        None,
        pattern=r"^POINT\([0-9]*\.[0-9]* [0-9]*\.[0-9]*\)$",
    )
    payment_method_id: int | None = None

    @field_validator(
        'source_address',
        'destination_address',
        mode='before',
    )
    @classmethod
    def formatting_address(
            cls,
            point: list[str] | str,
    ) -> str:

        if type(point) is list:

            if not len(point) == 2:
                raise ValueError('Incorrect format for coordinates')

            try:
                point = [float(point[0]), float(point[1])]
            except ValueError:
                raise ValueError('Incorrect format for coordinates')

            return f'POINT({point[0]} {point[1]})'

        return point


class ClaimSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    client_id: int | None = None
    invoice_id: int | None = None
    contact_email: EmailStr | None = None
    description: str | None = None
    money_required: Annotated[Decimal, Field(max_digits=10, decimal_places=2)] | None = None
    image_name: str | None = None


class PaymentMethodSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    is_supported: bool
