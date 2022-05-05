from .models import Invoice, InvoiceItem
from .schemas import (
    InvoiceCreate,
    InvoiceItemRead,
    InvoiceItemsCreate,
    InvoiceRead,
    InvoiceReadWithItems,
    InvoiceUpdate,
)
from ..infra.invoice_repository import InvoiceRepository
from .exceptions import (
    InvoiceAlreadyCancelledException,
    SumItemPriceDivergingFromInvoicePriceException,
    InvoiceAlreadyPaidException,
)


# Register invoice
def register_invoice(
    repository: InvoiceRepository,
    schema: InvoiceCreate,
) -> InvoiceRead:
    invoice = Invoice(**schema.dict())
    created_invoice = repository.save(invoice)
    return InvoiceRead.from_orm(created_invoice)


# Return all invoices
def get_invoices(repository: InvoiceRepository) -> list[Invoice]:
    return [InvoiceRead.from_orm(i) for i in repository.get_all()]


# If not cancelled, invoice can be paid
def pay_invoice(repository: InvoiceRepository, invoice_id: int) -> Invoice:
    invoice = repository.get(invoice_id)

    if invoice.cancelled:
        raise InvoiceAlreadyCancelledException()

    updated_invoice = repository.update(invoice_id, InvoiceUpdate(paid=True))
    return InvoiceRead.from_orm(updated_invoice)


# If not paid, an invoice can be cancelled
def cancel_invoice(repository: InvoiceRepository, invoice_id: int) -> Invoice:
    invoice = repository.get(invoice_id)
    if invoice.paid:
        raise InvoiceAlreadyPaidException()
    return repository.update(invoice_id, InvoiceUpdate(cancelled=True))


# Register invoice items to invoice if the sum of the invoice items is different from the invoice total, raise an error
def register_invoice_items(
    repository: InvoiceRepository,
    invoice_id: int,
    schema: InvoiceItemsCreate,
) -> InvoiceReadWithItems:
    invoice = repository.get(invoice_id)
    total_price = sum(item.price for item in schema.items)

    if total_price != invoice.price:
        raise SumItemPriceDivergingFromInvoicePriceException()

    repository.add_invoice_items([InvoiceItem(**item.dict()) for item in schema.items])
    return InvoiceReadWithItems.from_orm(repository.get(invoice_id))


# Return invoice by id with all invoice items
def get_invoice(repository: InvoiceRepository, invoice_id: int) -> Invoice:
    invoice_db = repository.get(invoice_id)
    invoice = InvoiceRead.from_orm(invoice_db)
    items = [InvoiceItemRead.from_orm(i) for i in invoice_db.items]
    return InvoiceReadWithItems(**invoice.dict(), items=items)
