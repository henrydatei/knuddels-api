import dataclasses

from .User import User

@dataclasses.dataclass
class FotomeetMatch:
    matchedAt: str
    isNew: bool
    user: User