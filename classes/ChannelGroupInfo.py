import dataclasses

from .Color import Color
from .ChannelBackgroundImageInfo import ChannelBackgroundImageInfo

@dataclasses.dataclass
class ChannelGroupInfo:
    backgroundColor: Color
    backgroundImageInfo: ChannelBackgroundImageInfo = dataclasses.field(init = False, default = None)
    highlightColor: Color = dataclasses.field(init = False, default = None)