from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from api.v1.orders.schemas import OrderCreateSchema

from core.models import Order, OrderProductAssociation
from core.repositories import BaseRepo, ProductRepo


class OrderRepo(BaseRepo[Order]):
    model = Order

    @classmethod
    async def add(cls, session: AsyncSession, order: OrderCreateSchema) -> Order:
        async with session.begin():
            new_order = cls.model(status=order.status)
            session.add(new_order)

            for order_product in order.products:
                product = await ProductRepo.find_one_or_none_by_id(
                    session=session, data_id=order_product.product_id
                )
                if product is None:
                    raise Exception("Товар не найден.")

                if product.quantity_in_storage < order_product.quantity:
                    raise Exception("Недостаточно товара на складе.")

                product.quantity_in_storage -= order_product.quantity

                association = OrderProductAssociation(
                    product_id=order_product.product_id,
                    quantity_in_order=order_product.quantity,
                )
                new_order.products_details.append(association)

        return new_order

    @classmethod
    async def get_orders_with_products_assoc(cls, session: AsyncSession) -> list[Order]:
        stmt = (
            select(Order)
            .options(
                selectinload(Order.products_details).joinedload(
                    OrderProductAssociation.product
                ),
            )
            .order_by(Order.id)
        )
        orders = await session.scalars(stmt)

        return list(orders)

    @classmethod
    async def get_order_with_products_assoc(
        cls, session: AsyncSession, order_id: int
    ) -> Order:
        stmt = (
            select(Order)
            .filter_by(id=order_id)
            .options(
                selectinload(Order.products_details).joinedload(
                    OrderProductAssociation.product
                ),
            )
            .order_by(Order.id)
        )
        order = await session.scalar(stmt)

        return order
