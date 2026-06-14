from dataclasses import dataclass
from uuid import UUID

from ...shared.domain.models import AggregateRoot, Entity


@dataclass(kw_only=True)
class Collection(AggregateRoot):
    """"""

    title: str
    description: str | None = None
    owner_id: UUID


@dataclass(kw_only=True)
class CollectionMember(Entity):
    collection_id: UUID
    user_id: UUID
    created_by: UUID


@dataclass(frozen=True)
class PermissionResult:
    allowed: bool
    reason: str | None = None


def can_archive_collection(collection: Collection, user_id: UUID) -> PermissionResult:
    if collection.owner_id == user_id:
        return PermissionResult(True)

    return PermissionResult(False, "")


permission = can_archive_collection(..., ...)
if not permission.allowed:
    raise ...
