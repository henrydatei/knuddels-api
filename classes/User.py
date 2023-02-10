import dataclasses
from typing import List

from .ProfilePicture import ProfilePicture

@dataclasses.dataclass
class User:
    id: str
    nick: str
    gender: str = dataclasses.field(init = False, default = None)
    age: int = dataclasses.field(init = False, default = None)
    city: str = dataclasses.field(init = False, default = None)
    conversationId: str = dataclasses.field(init = False, default = None)
    profilePicture: ProfilePicture = dataclasses.field(init = False, default = None)
    sexualOrientation: str = dataclasses.field(init = False, default = None)
    relationshipStatus: str = dataclasses.field(init = False, default = None)
    canReceiveMessages: bool = dataclasses.field(init = False, default = None)
    albumPhotosUrl: str = dataclasses.field(init = False, default = None)
    readMe: str = dataclasses.field(init = False, default = None)
    name: str = dataclasses.field(init = False, default = None)
    dateOfBirth: str = dataclasses.field(init = False, default = None)
    country: str = dataclasses.field(init = False, default = None)
    smoker: str = dataclasses.field(init = False, default = None)
    hobbies: List[str] = dataclasses.field(init = False, default = None)
    music: List[str] = dataclasses.field(init = False, default = None)
    movies: List[str] = dataclasses.field(init = False, default = None)
    series: List[str] = dataclasses.field(init = False, default = None)
    books: List[str] = dataclasses.field(init = False, default = None)
    languages: List[str] = dataclasses.field(init = False, default = None)
    lastOnlineTime: str = dataclasses.field(init = False, default = None)
    dateOfRegistration: str = dataclasses.field(init = False, default = None)
    status: str = dataclasses.field(init = False, default = None)
    supportsKnuddelsPhilosophy: bool = dataclasses.field(init = False, default = None)
    stammiMonths: int = dataclasses.field(init = False, default = None)
    latestOnlineChannelName: str = dataclasses.field(init = False, default = None)
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