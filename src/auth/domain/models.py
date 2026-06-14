from dataclasses import dataclass

from pydantic import SecretStr

from ...shared.domain.models import Entity
from .vo import FullName, Username


@dataclass(kw_only=True)
class User(Entity):
    """Конечный пользователь системы"""

    full_name: FullName
    username: Username | None = None
    email: ...
    password_hash: SecretStr
    email_verified: bool
