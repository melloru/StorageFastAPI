from pydantic import BaseModel


class ProductBaseSchema(BaseModel):
    name: str
    description: str
    price: int
    quantity_in_storage: int


class ProductSchema(ProductBaseSchema):
    id: int


class ProductCreateSchema(ProductBaseSchema):
    pass


class ProductUpdatePartialSchema(ProductCreateSchema):
    name: str | None = None
    description: str | None = None
    price: int | None = None
    quantity_in_storage: int | None = None
