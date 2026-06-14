from typing import TypedDict

from datetime import datetime
from enum import StrEnum, auto


class FileInfo(TypedDict):
    """Информация и сохранённом файле"""

    size: int
    content_type: str
    last_modified: datetime
    etag: str  # уникальный хэш файла


class AssetStatus(StrEnum):
    """Статус текущего состояния медиа актива"""

    DRAFT = auto()
    PROCESSING = auto()  # в обработке
    PUBLISHED = auto()
    ARCHIVED = auto()


class AssetVersionStatus(StrEnum):
    """Статусы обработки версии медиа актива"""

    PENDING = auto()
    PROCESSING = auto()
    FAILED = auto()
