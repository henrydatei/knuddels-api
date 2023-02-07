import dataclasses
from typing import List

from .ChannelGroupInfo import ChannelGroupInfo
from .User import User

@dataclasses.dataclass
class Channel:
    id: str
    name: str
    groupInfo: ChannelGroupInfo
    users: List[User]