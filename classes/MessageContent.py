import dataclasses
from .UserSentImage import UserSentImage
from .UserSentSnap import UserSentSnap
from typing import Union, Any

@dataclasses.dataclass
class ConversationVisiblePhotoCommentMessageContent:
    albumPhotoId: str
    commentId: str
    photoUrl: str
    formattedText: str # Oder dict, falls du es als JSON-Objekt bekommst

@dataclasses.dataclass
class ConversationTextMessageContent:
    formattedText: str
    starred: bool

@dataclasses.dataclass
class ConversationSnapMessageContent:
    snap: UserSentSnap
    imageAccepted: bool
    sensitiveContentClassification: str

@dataclasses.dataclass
class ConversationImageMessageContent:
    starred: bool
    image: UserSentImage
    imageAccepted: bool
    sensitiveContentClassification: str

@dataclasses.dataclass
class ConversationKnuddelTransferMessageContent:
    knuddelAmount: int

@dataclasses.dataclass
class ConversationQuotedMessageContent:
    starred: bool
    formattedText: str
    nestedMessage: Any

@dataclasses.dataclass
class ConversationHiddenPhotoCommentMessageContent:
    albumPhotoId: str
    photoUrl: str
    formattedText: str

MessageContent = Union[
    ConversationVisiblePhotoCommentMessageContent,
    ConversationTextMessageContent,
    ConversationSnapMessageContent,
    ConversationImageMessageContent,
    ConversationKnuddelTransferMessageContent,
    ConversationQuotedMessageContent,
    ConversationHiddenPhotoCommentMessageContent
]