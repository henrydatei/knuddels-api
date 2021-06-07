class Person():
    id = None
    nick = ""
    isOnline = ""
    canSendImages = ""
    age = ""
    albumPhotosUrl = ""
    canReceiveMessages = ""
    city = ""
    distance = ""
    gender = ""
    ignoreState = ""
    isIgnoring = ""
    profilePicture = ""
    readMe = ""
    relationshipStatus = ""
    sexualOrientation = ""
    onlineMinutes = ""
    isAppBot = ""
    isLockedByAutomaticComplaint = ""
    automaticComplaintCommand = ""
    isReportable = ""
    conversationID = ""

    def __init__ (self, id):
        self.id = id

class Text():
    text = None
    bold = ""
    italic = ""
    underline = ""

    def __init__ (self, text):
        self.text = text

class Message():
    id = None
    senderID = ""
    starred = ""
    formattedText = ""
    timestamp = ""
    image = ""
    snap = ""

    def __init__ (self, id):
        self.id = id
