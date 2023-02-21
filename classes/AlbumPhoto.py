import dataclasses
from typing import Optional

from .AlbumPhotoDescription import AlbumPhotoDescription

@dataclasses.dataclass
class AlbumPhoto:
    id: str
    thumbnailUrl: str
    photoUrl: str = dataclasses.field(init = False, default = None)
    administrationUrl: Optional[str]
    isOwner: bool = dataclasses.field(init = False, default = None)
    desription: AlbumPhotoDescription = dataclasses.field(init = False, default = None)