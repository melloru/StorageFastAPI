from pydantic import BaseModel


class OrderBaseSchema(BaseModel):
    status: str


class OrderSchema(OrderBaseSchema):
    id: int


class OrderProductSchema(BaseModel):
    product_id: int
    quantity: int


class OrderCreateSchema(OrderBaseSchema):
    products: list[OrderProductSchema]


class OrderUpdatePartialSchema(OrderBaseSchema):
    status: str | None = None
