import dataclasses
from typing import List

from .User import User
from .ReadState import ReadState
from .Message import Message

@dataclasses.dataclass
class Conversation:
    id: str
    isArchived: bool = dataclasses.field(init = False, default = None)
    otherParticipants: List[User] = dataclasses.field(init = False, default = None)
    readState: ReadState = dataclasses.field(init = False, default = None)
    latestMessage: Message = dataclasses.field(init = False, default = None)