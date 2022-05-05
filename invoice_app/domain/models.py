from sqlalchemy import ForeignKey, Integer, Float, Boolean, Column
from sqlalchemy.orm import relationship

from ..infra.db import Base


class InvoiceItem(Base):
    __tablename__ = 'invoice_items'
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'))
    price = Column(Float)


class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    paid = Column(Boolean, default=False)
    cancelled = Column(Boolean, default=False)
    items = relationship('InvoiceItem', lazy="joined")
