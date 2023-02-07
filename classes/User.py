import dataclasses

from .ProfilePicture import ProfilePicture

@dataclasses.dataclass
class User:
    id: str
    nick: str
    gender: str
    age: int = dataclasses.field(init = False, default = None)
    city: str = dataclasses.field(init = False, default = None)
    conversationId: str = dataclasses.field(init = False, default = None)
    profilePicture: ProfilePicture = dataclasses.field(init = False, default = None)