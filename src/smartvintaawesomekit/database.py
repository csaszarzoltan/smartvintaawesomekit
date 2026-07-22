"""Smart database utilities — async SQLAlchemy session management and CRUD helpers.

Provides async session lifecycle, declarative base, and generic CRUD operations
for SQLAlchemy ORM models with Pydantic schema integration.
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

ModelType = TypeVar("ModelType", bound="Base")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

# Default in-memory engine for get_session when no explicit engine is configured.
_default_engine = create_async_engine("sqlite+aiosqlite://", echo=False)
_default_session_factory = async_sessionmaker(
    _default_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""

    pass


async def get_session() -> AsyncSession:  # type: ignore[misc]
    """Async generator that yields an AsyncSession with automatic cleanup.

    Uses an in-memory SQLite engine by default. The session is automatically
    closed after the caller finishes.

    Yields:
        AsyncSession: A SQLAlchemy async session.
    """
    async with _default_session_factory() as session:
        yield session


class CRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base class for CRUD operations on SQLAlchemy models.

    Provides standard create, read, update, delete, and paginated list operations.

    Type Parameters:
        ModelType: The SQLAlchemy model class.
        CreateSchemaType: The Pydantic schema for creation.
        UpdateSchemaType: The Pydantic schema for updates.
    """

    def __init__(self, model: type[ModelType]) -> None:
        """Initialize CRUD with a model class.

        Args:
            model: The SQLAlchemy model class.
        """
        self.model = model

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record in the database.

        Args:
            db: An active database session.
            obj_in: The creation schema with field values.

        Returns:
            The newly created model instance.
        """
        if isinstance(obj_in, dict):
            instance = self.model(**obj_in)
        elif hasattr(obj_in, "model_dump"):
            instance = self.model(**obj_in.model_dump())  # type: ignore[union-attr]
        else:
            instance = self.model()
        if db is not None:
            db.add(instance)  # type: ignore[arg-type]
            await db.flush()
        return instance

    async def read(
        self,
        db: AsyncSession,
        record_id: Any,  # noqa: ANN401
    ) -> ModelType | None:
        """Read a record by its primary key.

        Args:
            db: An active database session.
            record_id: The primary key value.

        Returns:
            The model instance if found, None otherwise.
        """
        if db is None:
            return None
        stmt: Select = select(self.model).where(self.model.id == record_id)  # type: ignore[attr-defined]
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def update(
        self,
        db: AsyncSession,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
    ) -> ModelType:
        """Update an existing record.

        Args:
            db: An active database session.
            db_obj: The existing model instance to update.
            obj_in: The update schema or dict with new field values.

        Returns:
            The updated model instance.
        """
        if db_obj is None:
            return None  # type: ignore[return-value]
        if isinstance(obj_in, dict):
            update_data = obj_in
        elif hasattr(obj_in, "model_dump"):
            update_data = obj_in.model_dump()  # type: ignore[union-attr]
        else:
            update_data = {}
        for key, value in update_data.items():
            setattr(db_obj, key, value)
        if db is not None:
            await db.flush()
        return db_obj

    async def delete(
        self,
        db: AsyncSession,
        record_id: Any,  # noqa: ANN401
    ) -> ModelType | None:
        """Delete a record by its primary key.

        Args:
            db: An active database session.
            record_id: The primary key value.

        Returns:
            The deleted model instance if found, None otherwise.
        """
        if db is None:
            return None
        instance = await self.read(db, record_id)
        if instance is not None:
            await db.delete(instance)  # type: ignore[arg-type]
            await db.flush()
        return instance

    async def get_multi(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ModelType]:
        """Retrieve multiple records with pagination.

        Args:
            db: An active database session.
            skip: Number of records to skip (offset).
            limit: Maximum number of records to return.

        Returns:
            A list of model instances.
        """
        if db is None:
            return []
        stmt: Select = select(self.model).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return list(result.scalars().all())


__all__ = [
    "Base",
    "get_session",
    "CRUD",
]
