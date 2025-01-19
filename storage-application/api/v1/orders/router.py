from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from core.repositories import OrderRepo
from core.config import settings
from core.models import Order

from .schemas import OrderCreateSchema, OrderBaseSchema, OrderUpdatePartialSchema
from .dependencies import order_by_id

router = APIRouter(
    prefix=settings.api.v1.orders,
    tags=["Orders"],
)


@router.get("/")
async def get_all_orders(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[Order]:

    orders = await OrderRepo.get_orders_with_products_assoc(session=session)
    return orders


@router.get("/{order_id}")
async def get_order(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    order_id: int,
) -> Order:

    order = await OrderRepo.get_order_with_products_assoc(
        session=session, order_id=order_id
    )
    return order


@router.post("/create", response_model=OrderBaseSchema)
async def create_order(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    order: OrderCreateSchema,
) -> Order:

    new_order = await OrderRepo.add(session=session, order=order)
    return new_order


@router.patch("/update/{order_id}/status")
async def update_order_status(
    session: Annotated[
        AsyncSession,
        Depends(
            db_helper.session_getter,
        ),
    ],
    order_update: OrderUpdatePartialSchema,
    order: Order = Depends(order_by_id),
) -> Order:

    updated_order = await OrderRepo.update_partial(
        session=session,
        instance_update=order_update,
        instance=order,
    )

    return updated_order
