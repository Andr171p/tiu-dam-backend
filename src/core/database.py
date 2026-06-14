from datetime import datetime
from uuid import UUID, uuid4

from beanie import Document
from pydantic import Field

from ..shared.utils.time import current_datetime


class BaseDocument(Document):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=current_datetime)
    updated_at: datetime = Field(default_factory=current_datetime)
    deleted_at: datetime | None = Field(None)

    class Settings:
        is_root = True
        use_state_management = True
