import dataclasses

from typing import Optional
from .Message import Message

@dataclasses.dataclass
class ReadState:
    markedAsUnread: bool
    unreadMessageCount: int
    lastReadMessage: Optional[Message]