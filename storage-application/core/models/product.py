from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from core.models import Base

from .mixins import IntIdPkMixin

if TYPE_CHECKING:
    from .order_product_association import OrderProductAssociation


class Product(IntIdPkMixin, Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    quantity_in_storage: Mapped[int]

    orders_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="product",
    )
