import dataclasses

@dataclasses.dataclass
class ContactFilterSettings:
    allowedGender: str
    minAge: int
    maxAge: int
    profilePhotoRequired: bool
    alwaysAllowStammis: bool
    enableMessageSmoothing: bool
    onlyVerifiedMembers: bool