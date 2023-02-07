import dataclasses

from .Color import Color
from .ChannelBackgroundImageInfo import ChannelBackgroundImageInfo

@dataclasses.dataclass
class ChannelGroupInfo:
    backgroundColor: Color
    backgroundImageInfo: ChannelBackgroundImageInfo
    highlightColor: Color