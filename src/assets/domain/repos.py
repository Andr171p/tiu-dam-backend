from ...shared.domain.repos import Repository
from .models import Asset


class AssetRepository(Repository[Asset]):
    ...
