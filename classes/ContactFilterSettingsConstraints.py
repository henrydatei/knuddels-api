import dataclasses

@dataclasses.dataclass
class ContactFilterSettingsConstraints:
    minAge: int
    maxAge: int