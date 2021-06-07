from knuddelsAPI import *
from classes import *
import json

def login(username,password):
    deviceToken = json.loads(getDeviceToken(username,password))['data']['login']['createDeviceToken']['token']
    # print(deviceToken)
    data = getRefreshSessionToken(deviceToken)
    # print(data)
    sessionToken = json.loads(data)['data']['login']['refreshSession']['token']

    return sessionToken

def getPersons(sessionToken, beforeTimestamp = None):
    persons = []
    data = json.loads(MessengerOverview(sessionToken, beforeTimestamp))
    for conversation in data["data"]["messenger"]["conversations"]["conversations"]:
        person = conversation["otherParticipants"][0]
        try:
            readmeBlock = json.loads(person["readMe"])
        except Exception as e:
            readme = Text("")
        try:
            text = readmeBlock["text"]["text"]
            bold = readmeBlock["text"]["bold"]
            italic = readmeBlock["text"]["italic"]
            readme = Text(text)
            readme.bold = bold
            readme.italic = italic
        except Exception as e:
            readme = Text("")
        p = Person(person["id"])
        try:
            p.nick = person["nick"]
        except Exception as e:
            pass
        try:
            p.isOnline = person["isOnline"]
        except Exception as e:
            pass
        try:
            p.canSendImages = person["canSendImages"]
        except Exception as e:
            pass

        try:
            p.age = person["age"]
        except Exception as e:
            pass
        try:
            p.albumPhotosUrl = person["albumPhotosUrl"]
        except Exception as e:
            pass
        try:
            p.canReceiveMessages = person["canReceiveMessages"]
        except Exception as e:
            pass
        try:
            p.city = person["city"]
        except Exception as e:
            pass
        try:
            p.distance = person["distance"]
        except Exception as e:
            pass
        try:
            p.gender = person["gender"]
        except Exception as e:
            pass
        try:
            p.ignoreState = person["ignoreState"]
        except Exception as e:
            pass
        try:
            p.isIgnoring = person["isIgnoring"]
        except Exception as e:
            pass
        try:
            p.profilePicture = person["profilePicture"]
        except Exception as e:
            pass
        try:
            p.readMe = readme
        except Exception as e:
            pass
        try:
            p.relationshipStatus = person["relationshipStatus"]
        except Exception as e:
            pass
        try:
            p.sexualOrientation = person["sexualOrientation"]
        except Exception as e:
            pass
        try:
            p.onlineMinutes = person["onlineMinutes"]
        except Exception as e:
            pass
        try:
            p.isAppBot = person["isAppBot"]
        except Exception as e:
            pass
        try:
            p.isLockedByAutomaticComplaint = person["isLockedByAutomaticComplaint"]
        except Exception as e:
            pass
        try:
            p.automaticComplaintCommand = person["automaticComplaintCommand"]
        except Exception as e:
            pass
        try:
            p.isReportable = person["isReportable"]
        except Exception as e:
            pass
        try:
            p.conversationID = conversation["id"]
        except Exception as e:
            pass
        persons.append(p)

    hasMore = data["data"]["messenger"]["conversations"]["hasMore"]
    if hasMore:
        timestamp = data["data"]["messenger"]["conversations"]["conversations"][0]["latestMessage"]["timestamp"]
        print("found more chats " + str(timestamp))
        morePersons = getPersons(sessionToken, timestamp)
        persons.extend(morePersons)
    return persons

def getAllMessagesPerConversation(sessionToken, conversationID, beforeMessageID = None):
    messages = []
    data = json.loads(getConversation(sessionToken, conversationID, beforeMessageID))
    for message in data["data"]["messenger"]["conversation"]["messages"]["messages"]:
        m = Message(message["id"])
        try:
            m.senderID = message["sender"]["id"]
        except Exception as e:
            pass
        try:
            m.starred = message["starred"]
        except Exception as e:
            pass
        textBlock = json.loads(message["formattedText"])
        try:
            # Single Message
            t = Text(textBlock["text"]["text"].strip())
            t.bold = textBlock["text"]["bold"]
            t.italic = textBlock["text"]["italic"]
            m.formattedText = t
        except Exception as e:
            try:
                # Multiple Messages
                completeText = ""
                completeBold = False
                completeItalic = False
                for item in textBlock["list"]["items"]:
                    try:
                        completeText = completeText + " " + item["text"]["text"]
                        completeBold = completeBold or item["text"]["bold"]
                        completeItalic = completeItalic or item["text"]["italic"]
                    except Exception as e:
                        pass
                t = Text(completeText.replace("\n", "").strip())
                t.bold = completeBold
                t.italic = completeItalic
                m.formattedText = t
            except Exception as e:
                m.formattedText = Text("") 
        try:
            m.timestamp = message["timestamp"]
        except Exception as e:
            pass
        try:
            m.image = message["image"]
        except Exception as e:
            pass
        try:
            m.snap = message["snap"]
        except Exception as e:
            pass
        messages.append(m)
    hasMore = data["data"]["messenger"]["conversation"]["messages"]["hasMore"]
    if hasMore:
        try:
            id = data["data"]["messenger"]["conversations"]["messages"]["messages"][0]["id"]
            print("found more chats " + str(id))
            moreMessages = getAllMessagesPerConversation(sessionToken, conversationID, id)
        except Exception as e:
            moreMessages = []
        messages.extend(moreMessages)

    return messages

def backupProgress(currentPerson, maxPerson, maxMessage):
    print("Personen: {}/{}, Nachrichten der aktuellen Person: {}".format(currentPerson, maxPerson, maxMessage), end = "\r", flush = True)
