import dataclasses
from typing import Optional, Any

from .User import User
from .UserSentImage import UserSentImage
from .UserSentSnap import UserSentSnap
from .MessageContent import MessageContent
from .NestedMessage import NestedMessage

@dataclasses.dataclass
class Message:
    id: str
    nestedMessage: Optional[NestedMessage]
    sender: User = dataclasses.field(init = False, default = None)
    starred: bool = dataclasses.field(init = False, default = None)
    formattedText: str = dataclasses.field(init = False, default = None)
    timestamp: str = dataclasses.field(init = False, default = None)
    image: Optional[UserSentImage]
    snap: Optional[UserSentSnap]
    content: Any
