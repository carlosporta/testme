from typing import Optional
from pydantic import BaseModel


class InvoiceItemRead(BaseModel):
    id: int
    invoice_id: int
    price: float

    class  Config:
        orm_mode = True


class InvoiceItemCreate(BaseModel):
    invoice_id: int
    price: float


class InvoiceItemsCreate(BaseModel):
    items: list[InvoiceItemCreate]


class InvoiceCreate(BaseModel):
    price: float


class InvoiceRead(BaseModel):
    id: int
    price: float
    paid: bool
    cancelled: bool

    class Config:
        orm_mode = True


class InvoiceReadWithItems(InvoiceRead):
    items: list[InvoiceItemRead]


class InvoiceUpdate(BaseModel):
    paid: Optional[bool] = None
    cancelled: Optional[bool] = None
