import dataclasses
from typing import List

from .AlbumPhoto import AlbumPhoto

@dataclasses.dataclass
class Album:
    id: str
    title: str
    isOwner: bool
    albumPhotos: List[AlbumPhoto]