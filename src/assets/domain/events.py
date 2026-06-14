from dataclasses import dataclass
from uuid import UUID

from ...shared.domain.events import Event


@dataclass(frozen=True, kw_only=True)
class AssetUploaded(Event):
    """Загружена новая версия актива"""

    asset_id: UUID
    version_number: int
    storage_key: str
    uploaded_by: UUID
