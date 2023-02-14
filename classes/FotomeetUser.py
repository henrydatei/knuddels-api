import dataclasses
from typing import Optional

from .UserInfo import UserInfo

@dataclasses.dataclass
class FotomeetUser:
    age: int
    gender: str
    id: str
    isPotentialMatch: bool
    userInfo: Optional[UserInfo]
    imageUrl: str
    isReportable: bool
    hasAlbumPhotos: bool