from typing import Annotated

from fastapi import HTTPException, Path, status
from fastapi.params import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from core.repositories import ProductRepo
from core.models import Product


async def product_by_id(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    product_id: Annotated[int, Path],
) -> Product:
    product = await ProductRepo.find_one_or_none_by_id(
        session=session, data_id=product_id
    )
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Товар с ID: {product_id} не найден!",
        )

    return product
