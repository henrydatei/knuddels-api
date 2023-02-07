import dataclasses

from .UserInfo import UserInfo

@dataclasses.dataclass
class FotomeetUser:
    age: int
    gender: str
    id: str
    isPotentialMatch: bool
    userInfo: UserInfo
    imageUrl: str
    isReportable: bool
    hasAlbumPhotos: bool