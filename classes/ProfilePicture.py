import dataclasses

@dataclasses.dataclass
class ProfilePicture:
    urlLargeSquare: str = dataclasses.field(init = False, default = None)
    urlVeryLarge: str = dataclasses.field(init = False, default = None)
    urlCustomSizeSquare: str = dataclasses.field(init = False, default = None)
    exists: bool = dataclasses.field(init = False, default = None)