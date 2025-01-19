from typing import Type, TypeVar, Sequence, Generic

from pydantic import BaseModel as PydanticBaseModel

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from core.models import Base


T = TypeVar("T", bound=Base)


class BaseRepo(Generic[T]):
    model: Type[T]

    @classmethod
    async def find_all(
        cls,
        session: AsyncSession,
    ) -> Sequence[T]:
        stmt = select(cls.model)
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def find_by_filter(
        cls,
        session: AsyncSession,
        **filter_by,
    ) -> Sequence[T]:
        stmt = select(cls.model).filter_by(**filter_by)
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def find_one_or_none_by_id(
        cls, session: AsyncSession, data_id: int
    ) -> T | None:
        stmt = select(cls.model).filter_by(id=data_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def add(
        cls,
        session: AsyncSession,
        value: PydanticBaseModel,
    ) -> T:
        new_instance = cls.model(**value.model_dump())
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    async def add_many(cls):
        pass

    @classmethod
    async def delete_instance(
        cls,
        session: AsyncSession,
        instance: T,
    ) -> None:
        await session.delete(instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e

    @classmethod
    async def delete_many(cls):
        pass

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        filter_by,
        **values,
    ):
        stmt = (
            update(cls.model)
            .where(*[getattr(cls.model, k) == v for k, v in filter_by.items()])
            .values(**values)
            .execution_options(synchronize_session="fetch")
        )
        result = await session.execute(stmt)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return result.rowcount

    @classmethod
    async def update_partial(
        cls,
        session: AsyncSession,
        instance_update: PydanticBaseModel,
        instance: T,
    ) -> T:
        for key, value in instance_update.model_dump(exclude_unset=True).items():
            setattr(instance, key, value)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return instance
