from typing import Annotated

from fastapi import Path, HTTPException, status
from fastapi.params import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from core.models import Order
from core.repositories import OrderRepo


async def order_by_id(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    order_id: Annotated[int, Path],
) -> Order:
    order = await OrderRepo.find_one_or_none_by_id(session=session, data_id=order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Заказ с ID: {order_id} не найден!",
        )

    return order
