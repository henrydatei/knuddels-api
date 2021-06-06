class Person():
    id = None
    nick = None
    isOnline = None
    canSendImages = None
    age = None
    albumPhotosUrl = None
    canReceiveMessages = None
    city = None
    distance = None
    gender = None
    ignoreState = None
    isIgnoring = None
    profilePicture = None
    readMe = None
    relationshipStatus = None
    sexualOrientation = None
    onlineMinutes = None
    isAppBot = None
    isLockedByAutomaticComplaint = None
    automaticComplaintCommand = None
    isReportable = None
    conversationID = None

    def __init__ (self, id):
        self.id = id

class Text():
    text = None
    bold = None
    italic = None
    underline = None

    def __init__ (self, text):
        self.text = text

class Message():
    id = None
    senderID = None
    starred = None
    formattedText = None
    timestamp = None
    image = None
    snap = None

    def __init__ (self, id):
        self.id = id
