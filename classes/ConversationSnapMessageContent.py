import dataclasses

from .UserSentSnap import UserSentSnap

@dataclasses.dataclass
class ConversationSnapMessageContent:
    snap: UserSentSnap