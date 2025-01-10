from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

if TYPE_CHECKING:
    from .order_product_association import OrderProductAssociation


class Order(Base):
    status: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow,
    )

    products: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="order"
    )
