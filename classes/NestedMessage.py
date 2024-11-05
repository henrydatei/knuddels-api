import dataclasses
from typing import Optional

from .User import User

@dataclasses.dataclass
class NestedMessage:
    id: str
    sender: User
    formattedText: str
    timestamp: str
    type: str
    image: Optional[dict]