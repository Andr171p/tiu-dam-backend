from uuid import UUID

ASSET_STORAGE_KEY_LENGTH = 5


def create_asset_storage_key(asset_id: UUID, version_number: int, filename: str) -> str:
    """Создание ключа хранилища для медиа актива"""

    if version_number < 1:
        raise ValueError("Version number must be greater than 0")

    return f"assets/{asset_id}/v/{version_number}/{filename}"


def parse_asset_storage_key(storage_key: str) -> tuple[UUID, int, str]:
    """Парсинг полезной нагрузки из ключа объекта"""

    parts = storage_key.split("/")
    if len(parts) <= ASSET_STORAGE_KEY_LENGTH:
        raise ValueError(
            "Storage key must have at least 5 components."
            "Key template: 'assets/[asset-id]/v/[version-number]/[filename]'"
        )

    if parts[0] != "assets":
        raise ValueError("Storage key must start with 'assets/'")
    if parts[2] != "v":
        raise ValueError("Storage key must contain '/v/' after asset_id")

    asset_id = parts[1]
    version_number = parts[3]
    filename = "/".join(parts[4:])

    return UUID(asset_id), int(version_number), filename
