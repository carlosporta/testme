from fastapi import APIRouter, Depends, status, HTTPException
from invoice_app.domain import exceptions

from ..infra.invoice_repository import InvoiceRepository
from ..domain.schemas import (
    InvoiceCreate,
    InvoiceItemsCreate,
    InvoiceRead,
    InvoiceReadWithItems,
)
from ..domain import usecases

from .dependencies import get_invoice_repository


router = APIRouter()


# Register invoice
@router.post(
    '/register',
    response_model=InvoiceRead,
    status_code=status.HTTP_201_CREATED,
)
def register_invoice(
    schema: InvoiceCreate,
    repository: InvoiceRepository = Depends(get_invoice_repository),
):
    return usecases.register_invoice(repository, schema)


# Return all invoices
@router.get('/all', response_model=list[InvoiceRead])
def get_invoices(
    repository: InvoiceRepository = Depends(get_invoice_repository),
):
    return usecases.get_invoices(repository)


# Invoice can be paid
@router.put('/{invoice_id}/pay', response_model=InvoiceRead)
def pay_invoice(
    invoice_id: int,
    repository: InvoiceRepository = Depends(get_invoice_repository),
):
    try:
        return usecases.pay_invoice(repository, invoice_id)
    except exceptions.InvoiceAlreadyCancelledException:
        raise HTTPException(status.HTTP_409_CONFLICT, 'Invoice already paid')


# Cancel invoice
@router.put('/{invoice_id}/cancel', response_model=InvoiceRead)
def pay_invoice(
    invoice_id: int,
    repository: InvoiceRepository = Depends(get_invoice_repository),
):
    try:
        return usecases.cancel_invoice(repository, invoice_id)
    except exceptions.InvoiceAlreadyPaidException:
        raise HTTPException(status.HTTP_409_CONFLICT, 'Invoice already paid')


# Register invoice items to invoice
@router.post(
    '/{invoice_id}/items/register',
    response_model=InvoiceReadWithItems,
    status_code=status.HTTP_201_CREATED,
)
def register_invoice_items(
    invoice_id: int,
    schema: InvoiceItemsCreate,
    repository: InvoiceRepository = Depends(get_invoice_repository),
):
    try:
        return usecases.register_invoice_items(repository, invoice_id, schema)
    except exceptions.SumItemPriceDivergingFromInvoicePriceException:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            'Invoice items price diverging from invoice price',
        )


# Return invoice by id with all invoice items
@router.get('/{invoice_id}', response_model=InvoiceReadWithItems)
def get_invoice(
    invoice_id: int,
    repository: InvoiceRepository = Depends(get_invoice_repository),
):
    return usecases.get_invoice(repository, invoice_id)
