import dataclasses

@dataclasses.dataclass
class ProfilePicture:
    urlLargeSquare: str
    urlVeryLarge: str = dataclasses.field(init = False, default = None)
    exists: bool = dataclasses.field(init = False, default = None)