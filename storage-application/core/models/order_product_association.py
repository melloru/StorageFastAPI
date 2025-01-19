from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .order import Order
    from .product import Product


class OrderProductAssociation(IntIdPkMixin, Base):
    __table_args__ = (
        UniqueConstraint(
            "order_id",
            "product_id",
        ),
    )
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity_in_order: Mapped[int] = mapped_column(default=1, server_default="1")
    # price_for_one: Mapped[int] = mapped_column(default=0, server_default="0")

    order: Mapped["Order"] = relationship("Order", back_populates="products_details")
    product: Mapped["Product"] = relationship(
        "Product", back_populates="orders_details"
    )
