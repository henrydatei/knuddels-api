import dataclasses
from typing import Optional

from .Color import Color
from .ChannelBackgroundImageInfo import ChannelBackgroundImageInfo

@dataclasses.dataclass
class ChannelGroupInfo:
    backgroundColor: Color
    backgroundImageInfo: Optional[ChannelBackgroundImageInfo]
    highlightColor: Color = dataclasses.field(init = False, default = None)