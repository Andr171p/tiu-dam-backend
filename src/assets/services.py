from uuid import UUID

from ..collections.domain.repos import CollectionRepository
from ..shared.domain.events import EventPublisher
from ..shared.domain.exceptions import NotFoundError
from ..shared.domain.repos import UnitOfWork
from .domain.models import Asset
from .domain.repos import AssetRepository
from .domain.services import create_asset_storage_key, parse_asset_storage_key
from .domain.storage import Storage
from .schemas import AssetCreate, AssetUploadRequest, AssetUploadResponse

ASSET_UPLOAD_URL_EXPIRES_IN = 3600


class AssetService:
    def __init__(
            self,
            uow: UnitOfWork,
            storage: Storage,
            collection_repo: CollectionRepository,
            asset_repo: AssetRepository,
            event_publisher: EventPublisher,
    ) -> None:
        self.uow = uow
        self.storage = storage
        self.collection_repo = collection_repo
        self.asset_repo = asset_repo
        self.event_publisher = event_publisher

    async def create(self, data: AssetCreate, current_user: ...) -> ...:
        collection = await self.collection_repo.read(data.collection_id)
        if collection is None:
            raise NotFoundError(f"Collection with ID {data.collection_id} not found")

        asset = Asset.create(
            collection_id=data.collection_id,
            title=data.title,
            description=data.description,
        )
        await self.asset_repo.create(asset)
        await self.uow.commit()

        return ...

    async def generate_upload_url(
            self, asset_id: UUID, request: AssetUploadRequest, current_user: ...
    ) -> AssetUploadResponse:
        asset = await self.asset_repo.read(asset_id)
        if asset is None:
            raise NotFoundError(f"Asset with ID {asset_id} not found")

        version_number = asset.get_next_version_number()
        storage_key = create_asset_storage_key(asset_id, version_number, request.filename)
        upload_url = await self.storage.create_presigned_upload_url(
            storage_key=storage_key,
            content_type=request.content_type,
            expires_in=ASSET_UPLOAD_URL_EXPIRES_IN,
        )

        return AssetUploadResponse(
            upload_url=upload_url, storage_key=storage_key, version_number=version_number
        )

    async def confirm_upload(
            self, asset_id: UUID, storage_key: str, current_user: ...
    ) -> ...:
        """Подтверждение загрузки медиа актива и создание новой версии актива"""

        (
            parsed_asset_id, parsed_version_number, parsed_filename
        ) = parse_asset_storage_key(storage_key)
        if parsed_asset_id != asset_id:
            raise ValueError("Storage key does not belong to this asset")

        asset = await self.asset_repo.read(asset_id)
        if asset is None:
            raise NotFoundError(f"Asset with ID {asset_id} not found")

        excepted_version_number = asset.get_next_version_number()
        if parsed_version_number != excepted_version_number:
            raise ValueError(
                f"Version number mismatch: "
                f"expected {excepted_version_number}, got {parsed_version_number}"
            )

        file_info = await self.storage.get_file_info(storage_key)

        asset.add_version(
            storage_key=storage_key,
            original_filename=parsed_filename,
            mime_type=file_info["content_type"],
            size_bytes=file_info["size"],
            checksum=file_info["etag"],
            uploaded_by=current_user.user_id,
            uploaded_at=file_info["last_modified"],
            version_number=parsed_version_number,
        )
        await self.asset_repo.update(asset)
        await self.uow.commit()

        for event in asset.collect_events():
            await self.event_publisher.publish(event)

        return ...

    async def publish(self, asset_id: UUID, current_user: ...) -> ...: ...
