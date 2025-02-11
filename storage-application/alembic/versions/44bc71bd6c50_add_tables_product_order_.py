"""add tables product-order-orderproductassoc

Revision ID: 44bc71bd6c50
Revises: 
Create Date: 2025-01-10 03:11:22.965024

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "44bc71bd6c50"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("order_product_associations")
    op.drop_table("products")
    op.drop_table("orders")
    # ### end Alembic commands ###


def upgrade() -> None:
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_orders")),
    )
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("quantity_in_storage", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_products")),
    )
    op.create_table(
        "order_product_associations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column(
            "quantity_in_order",
            sa.Integer(),
            server_default="1",
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["orders.id"],
            name=op.f("fk_order_product_associations_order_id_orders"),
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
            name=op.f("fk_order_product_associations_product_id_products"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_order_product_associations")),
        sa.UniqueConstraint(
            "order_id",
            "product_id",
            name=op.f("uq_order_product_associations_order_id_product_id"),
        ),
    )
    # ### end Alembic commands ###
