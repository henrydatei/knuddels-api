import dataclasses
from typing import List

from .ChannelGroupInfo import ChannelGroupInfo
from .Channel import Channel
from .User import User

@dataclasses.dataclass
class ChannelGroup:
    id: str
    name: str
    info: ChannelGroupInfo
    channels: List[Channel]
    onlineContacts: List[User]