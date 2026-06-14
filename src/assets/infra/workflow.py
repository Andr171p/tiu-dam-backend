from typing import Any

from datetime import timedelta
from uuid import UUID

from temporalio import activity, workflow


@activity.defn
async def extract_asset_meta(storage_key: str) -> dict[str, Any]:
    """Извлечение метаданных из изображения"""


@activity.defn
async def generate_asset_preview() -> dict[str, Any]:
    """Генерация превью для изображения"""


@activity.defn
async def apply_watermark_to_asset() -> dict[str, Any]:
    """Наложение водяного знака на изображение"""


@workflow.defn
class AssetProcessingWorkflow:
    """Оркестратор для обработки медиа актива"""

    @workflow.run
    async def run(self, asset_id: UUID, storage_key: str) -> dict[str, Any]:  # noqa: PLR6301
        asset_meta = await workflow.execute_activity(
            extract_asset_meta,
            args=[storage_key],
            start_to_close_timeout=timedelta(minutes=5),
            summary="Извлечение технических метаданных",
        )

        preview_key = await workflow.execute_activity(
            generate_asset_preview,
            args=[storage_key],
            start_to_close_timeout=timedelta(minutes=2),
            summary="Генерация превью для изображения"
        )

        watermarked_key = await workflow.execute_activity(
            apply_watermark_to_asset,
            args=[storage_key],
            start_to_close_timeout=timedelta(minutes=10),
            summary="Наложение водяного знака на изображение"
        )

        return {
            "meta": asset_meta,
            "preview_key": preview_key,
            "watermarked_key": watermarked_key,
        }
