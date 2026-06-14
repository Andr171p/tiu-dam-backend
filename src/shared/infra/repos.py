import abc
from collections.abc import Awaitable, Callable
from uuid import UUID

from beanie import Document

from ..domain.models import Entity
from ..utils.time import current_datetime


class DocumentMapper[EntityT: Entity, DocumentT: Document](abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def to_entity(document: DocumentT) -> EntityT: ...

    @staticmethod
    @abc.abstractmethod
    def from_entity(entity: EntityT) -> DocumentT: ...


class BeanieRepository[EntityT: Entity, DocumentT: Document]:
    document: type[DocumentT]
    doc_mapper: DocumentMapper[EntityT, DocumentT]

    def __init__(
            self,
            create_wrapper: ...,
            read_wrapper: ...,
            update_wrapper: ...,
            delete_wrapper: ...,
    ) -> None:
        ...

    async def create(self, entity: EntityT) -> None:
        document = self.doc_mapper.from_entity(entity)
        await document.insert()

    async def read(self, uid: UUID) -> EntityT | None:
        document = await self.document.find_one(
            self.document.id == uid, self.document.deleted_at is None
        )
        return None if document is None else self.doc_mapper.to_entity(document)

    async def update(self, entity: EntityT) -> None:
        document = self.doc_mapper.from_entity(entity)
        await self.document.find_one(
            self.document.id == document.id, self.document.deleted_at is None
        ).replace_one(document)

    async def delete(self, uid: UUID) -> None:
        now = current_datetime()
        await self.document.find_one(
            self.document.id == uid, self.document.deleted_at is None
        ).set({self.document.deleted_at: now})
