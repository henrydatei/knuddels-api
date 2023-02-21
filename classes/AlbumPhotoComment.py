import dataclasses

from .User import User

@dataclasses.dataclass
class AlbumPhotoComment:
    id: str
    text: str
    timestamp: str
    sender: User