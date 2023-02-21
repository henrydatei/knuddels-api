import dataclasses
from typing import List

from .ChannelGroup import ChannelGroup

@dataclasses.dataclass
class ChannelCategory:
    id: str
    name: str
    channelGroups: List[ChannelGroup]