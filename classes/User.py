import dataclasses
from typing import List, Optional

from .ProfilePicture import ProfilePicture
from .AlbumPhoto import AlbumPhoto
from .Album import Album

@dataclasses.dataclass
class User:
    id: str = dataclasses.field(init = False, default = None)
    nick: str = dataclasses.field(init = False, default = None)
    gender: str = dataclasses.field(init = False, default = None)
    age: int = dataclasses.field(init = False, default = None)
    city: str = dataclasses.field(init = False, default = None)
    conversationId: str = dataclasses.field(init = False, default = None)
    profilePicture: ProfilePicture = dataclasses.field(init = False, default = None)
    sexualOrientation: str = dataclasses.field(init = False, default = None)
    relationshipStatus: str = dataclasses.field(init = False, default = None)
    canReceiveMessages: bool = dataclasses.field(init = False, default = None)
    albumPhotosUrl: str = dataclasses.field(init = False, default = None)
    readMe: Optional[str]
    name: str = dataclasses.field(init = False, default = None)
    dateOfBirth: Optional[str]
    country: str = dataclasses.field(init = False, default = None)
    smoker: Optional[str]
    hobbies: List[str] = dataclasses.field(init = False, default = None)
    music: List[str] = dataclasses.field(init = False, default = None)
    movies: List[str] = dataclasses.field(init = False, default = None)
    series: List[str] = dataclasses.field(init = False, default = None)
    books: List[str] = dataclasses.field(init = False, default = None)
    languages: List[str] = dataclasses.field(init = False, default = None)
    lastOnlineTime: Optional[str]
    dateOfRegistration: Optional[str]
    status: Optional[str]
    supportsKnuddelsPhilosophy: bool = dataclasses.field(init = False, default = None)
    stammiMonths: int = dataclasses.field(init = False, default = None)
    latestOnlineChannelName: Optional[str]
    myChannelName: str = dataclasses.field(init = False, default = None)
    moderatedChannelName: str = dataclasses.field(init = False, default = None)
    hickeys: int = dataclasses.field(init = False, default = None)
    flowers: int = dataclasses.field(init = False, default = None)
    roses: int = dataclasses.field(init = False, default = None)
    chatMeetups: int = dataclasses.field(init = False, default = None)
    givenHeart: str = dataclasses.field(init = False, default = None)
    mentorPoints: int = dataclasses.field(init = False, default = None)
    onlineMinutes: int = dataclasses.field(init = False, default = None)
    isReportable: bool = dataclasses.field(init = False, default = None)
    isOnline: bool = dataclasses.field(init = False, default = None)
    canSendImages: bool = dataclasses.field(init = False, default = None)
    ignoreState: str = dataclasses.field(init = False, default = None)
    isIgnoring: bool = dataclasses.field(init = False, default = None)
    albumPhotos: List[AlbumPhoto] = dataclasses.field(init = False, default = None)
    albums: List[Album] = dataclasses.field(init = False, default = None)
    albumProfilePhoto: AlbumPhoto = dataclasses.field(init = False, default = None)
    isAppBot: bool = dataclasses.field(init = False, default = None)
    menteeStatus: str = dataclasses.field(init = False, default = None)
    authenticityClassification: str = dataclasses.field(init = False, default = None)