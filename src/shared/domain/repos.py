from typing import Protocol, Self

from uuid import UUID

from ..schemas import Page, Pagination
from .models import Entity


class UnitOfWork(Protocol):

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...


class Repository[EntityT: Entity](Protocol):

    async def create(self, entity: EntityT) -> EntityT: ...

    async def read(self, uid: UUID) -> EntityT | None: ...

    async def paginate(self, pagination: Pagination) -> Page[EntityT]: ...

    async def update(self, entity: EntityT) -> None: ...

    async def delete(self, uid: UUID) -> None: ...

    async def exists(self, uid: UUID) -> bool: ...
