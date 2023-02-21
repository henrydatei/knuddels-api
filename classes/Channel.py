import dataclasses
from typing import List

from .ChannelGroupInfo import ChannelGroupInfo
from .User import User

@dataclasses.dataclass
class Channel:
    id: str
    name: str
    groupInfo: ChannelGroupInfo = dataclasses.field(init = False, default = None)
    users: List[User] = dataclasses.field(init = False, default = None)
    onlineUserCount: int = dataclasses.field(init = False, default = None)