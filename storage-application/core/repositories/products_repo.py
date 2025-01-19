from core.models import Product
from core.repositories import BaseRepo


class ProductRepo(BaseRepo[Product]):
    model = Product
