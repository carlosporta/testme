from sqlalchemy import insert, update
from sqlalchemy.future import select

from invoice_app.domain.schemas import InvoiceUpdate

from .db import get_session
from ..domain.models import Invoice, InvoiceItem


class InvoiceRepository:
    def save(self, invoice: Invoice) -> Invoice:
        with get_session() as session:
            session.add(invoice)
            session.commit()
            session.refresh(invoice)
            return invoice

    def get(self, invoice_id: int) -> Invoice:
        with get_session() as session:
            stmt = select(Invoice).where(Invoice.id == invoice_id)
            return session.scalar(stmt)

    def get_all(self) -> list[Invoice]:
        with get_session() as session:
            stmt = select(Invoice)
            return session.scalars(stmt).all()

    def update(self, invoice_id: int, schema: InvoiceUpdate) -> Invoice:
        with get_session() as session:
            stmt = (
                update(Invoice)
                .where(Invoice.id == invoice_id)
                .values(**schema.dict(exclude_unset=True))
            )
            session.execute(stmt)
            session.commit()
        return self.get(invoice_id)

    def add_invoice_items(
        self, invoice_items: list[InvoiceItem]
    ) -> None:
        with get_session() as session:
            [session.add(i) for i in invoice_items]
            session.commit()
