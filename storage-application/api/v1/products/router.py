from typing import Annotated, Sequence

from fastapi import APIRouter, status
from fastapi.params import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from core.config import settings
from core.models import Product
from core.repositories import ProductRepo

from .schemas import (
    ProductSchema,
    ProductCreateSchema,
    ProductUpdatePartialSchema,
)
from .dependencies import product_by_id


router = APIRouter(
    prefix=settings.api.v1.products,
    tags=["Products"],
)


@router.get("/", response_model=Sequence[ProductSchema])
async def get_all_products(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    products = await ProductRepo.find_all(session=session)
    return products


@router.get("/{product_id}", response_model=ProductSchema)
async def get_product_by_id(
    product: Product = Depends(product_by_id),
):
    return product


@router.post("/create", response_model=ProductCreateSchema)
async def create_product(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    product: ProductCreateSchema,
) -> Product:
    new_product = await ProductRepo.add(session=session, value=product)
    return new_product


@router.patch("/update/{product_id}", response_model=ProductUpdatePartialSchema)
async def update_product(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    product_update: ProductUpdatePartialSchema,
    product: Product = Depends(product_by_id),
) -> Product:
    updated_product = await ProductRepo.update_partial(
        session=session,
        instance_update=product_update,
        instance=product,
    )
    return updated_product


@router.delete("/delete/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    product: Product = Depends(product_by_id),
) -> None:
    await ProductRepo.delete_instance(session=session, instance=product)
