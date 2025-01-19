from fastapi import APIRouter

from core.config import settings

from .products.router import router as products_router
from .orders.router import router as orders_router

routers = APIRouter(
    prefix=settings.api.v1.prefix,
)

router_list = [products_router, orders_router]

for router in router_list:
    routers.include_router(router)
