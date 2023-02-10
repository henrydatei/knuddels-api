import dataclasses
from typing import Optional

from .User import User

@dataclasses.dataclass
class Message:
    id: str
    nestedMessage: Optional[str]
    sender: User = dataclasses.field(init = False, default = None)
    starred: bool = dataclasses.field(init = False, default = None)
    formattedText: str = dataclasses.field(init = False, default = None)
    timestamp: str = dataclasses.field(init = False, default = None)
    image: Optional[str]
    snap: Optional[str]
