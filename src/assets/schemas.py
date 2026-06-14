from uuid import UUID

from pydantic import AnyHttpUrl, BaseModel, Field, PositiveInt


class AssetCreate(BaseModel):
    """Создание медиа актива"""

    collection_id: UUID = Field(..., description="ID коллекции, в которой будет расположен актив")
    title: str = Field(..., description="Название медиа актива", examples=["День открытых дверей"])
    description: str | None = Field(None, description="Описание медиа файла")


class AssetUploadRequest(BaseModel):
    """Запрос для инициализации загрузки файла"""

    filename: str = Field(..., min_length=1, max_length=255, description="Оригинальное имя файла")
    content_type: str = Field(
        ...,
        pattern=r"^[\w\-]+/[\w\-\.]+$",
        description="Тип контента файла",
        examples=["application/pdf"],
    )


class AssetUploadResponse(BaseModel):
    """Результат инициализации загрузки файла"""

    upload_url: AnyHttpUrl = Field(..., description="Временная ссылка для загрузки файла")
    storage_key: str = Field(..., description="Ключ файла в хранилище")
    version_number: PositiveInt = Field(..., description="Номер версии актива", examples=[1, 2, 3])


class ConfirmUploadRequest(BaseModel):
    """Подтверждение загрузки медиа"""

    storage_key: str = Field(
        ..., min_length=1, max_length=255, description="Уникальный ключ загруженного объекта"
    )
    filename: str = Field(..., description="Оригинальное имя файла")
    content_type: str = Field(
        ...,
        pattern=r"^[\w\-]+/[\w\-\.]+$",
        description="Тип контента файла",
        examples=["application/pdf"],
    )


class AssetResponse(BaseModel):
    ...
