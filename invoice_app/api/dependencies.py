from ..infra.invoice_repository import InvoiceRepository


def _singleton_invoice_repository():
    repository = None

    def wrapper():
        nonlocal repository
        if repository is None:
            repository = InvoiceRepository()
        return repository

    return wrapper


get_invoice_repository = _singleton_invoice_repository()
