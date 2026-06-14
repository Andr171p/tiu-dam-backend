from typing import Any

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from ...shared.domain.exceptions import InvariantViolationError
from ...shared.domain.models import AggregateRoot, Entity
from ...shared.utils.time import current_datetime
from .events import AssetUploaded
from .vo import AssetStatus, AssetVersionStatus


@dataclass(kw_only=True)
class AssetVersion(Entity):

    asset_id: UUID
    number: int

    status: AssetVersionStatus

    storage_key: str
    original_filename: str
    mime_type: str
    size_bytes: int
    checksum: str
    meta: dict[str, Any] = field(default_factory=dict)

    uploaded_by: UUID
    uploaded_at: datetime = field(default_factory=current_datetime)

    def __post_init__(self) -> None:
        if self.number <= 0:
            raise ValueError("Version number must be greater than zero")


@dataclass(kw_only=True)
class Asset(AggregateRoot):

    collection_id: UUID

    title: str
    description: str | None = None
    status: AssetStatus

    current_version_number: int | None = None
    versions: list[AssetVersion] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("Asset title cannot be empty")

    @classmethod
    def create(cls, collection_id: UUID, title: str, description: str | None = None) -> "Asset":
        """Создание нового медиа актива в статусе DRAFT"""

        return cls(
            collection_id=collection_id,
            title=title,
            description=description,
            status=AssetStatus.DRAFT,
        )

    def get_next_version_number(self) -> int:
        """Получает номер для новой версии"""

        return max((version.number for version in self.versions), default=0) + 1

    def add_version(
            self,
            *,
            storage_key: str,
            original_filename: str,
            mime_type: str,
            size_bytes: int,
            checksum: str,
            uploaded_by: UUID,
            uploaded_at: datetime,
            version_number: int | None = None,
    ) -> AssetVersion:
        """Добавление новой версии актива"""

        if version_number is None:
            version_number = self.get_next_version_number()

        # Проверка, что номер не занят
        elif any(version.number == version_number for version in self.versions):
            raise InvariantViolationError(f"Version {version_number} already exists in asset")

        version = AssetVersion(
            asset_id=self.id,
            number=version_number,
            status=AssetVersionStatus.PENDING,
            storage_key=storage_key,
            original_filename=original_filename,
            mime_type=mime_type,
            size_bytes=size_bytes,
            checksum=checksum,
            uploaded_by=uploaded_by,
            uploaded_at=uploaded_at,
        )
        self.versions.append(version)

        self.register_event(
            AssetUploaded(
                asset_id=self.id,
                version_number=version_number,
                storage_key=storage_key,
                uploaded_by=uploaded_by,
            )
        )

        return version
