import dataclasses
from typing import List

from .User import User

@dataclasses.dataclass
class ProfileVisitors:
    visibilityStatus: str
    visitors: List[User]