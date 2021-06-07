from knuddelsAPI import *
from functions import *
from classes import *
import json

username = "lea16w"
password = "qwertzuiop"
totalMessagesMale = 0
totalChatsMale = 0
totalMessagesFemale = 0
totalChatsFemale = 0

sessionToken = login(username, password)
persons = getPersons(sessionToken)
maxPerson = len(persons)
currentPerson = 1

for person in persons:
    data = {}
    data["id"] = person.id
    data["nick"] = person.nick
    data["isOnline"] = person.isOnline
    data["canSendImages"] = person.canSendImages
    data["age"] = person.age
    data["albumPhotosUrl"] = person.albumPhotosUrl
    data["canReceiveMessages"] = person.canReceiveMessages
    data["city"] = person.city
    data["distance"] = person.distance
    data["gender"] = person.gender
    data["ignoreState"] = person.ignoreState
    data["isIgnoring"] = person.isIgnoring
    data["profilePicture"] = person.profilePicture
    data["readMe"] = person.readMe.text
    data["relationshipStatus"] = person.relationshipStatus
    data["sexualOrientation"] = person.sexualOrientation
    data["onlineMinutes"] = person.onlineMinutes
    data["isAppBot"] = person.isAppBot
    data["isLockedByAutomaticComplaint"] = person.isLockedByAutomaticComplaint
    data["automaticComplaintCommand"] = person.automaticComplaintCommand
    data["isReportable"] = person.isReportable
    data["conversationID"] = person.conversationID

    data['messages'] = []
    messages = getAllMessagesPerConversation(sessionToken, person.conversationID)
    maxMessage = len(messages)
    for msg in messages:
        backupProgress(currentPerson, maxPerson, maxMessage)
        msgObj = {'from': msg.senderID, 'starred': msg.starred, 'time': msg.timestamp, 'text': msg.formattedText.text, 'image': msg.image, 'snap': msg.snap}
        data['messages'].append(msgObj)

    if person.gender == "MALE":
        # male
        totalChatsMale = totalChatsMale + 1
        totalMessagesMale = totalMessagesMale + len(messages)
    else:
        totalChatsFemale = totalChatsFemale + 1
        totalMessagesFemale = totalMessagesFemale + len(messages)

    with open("chats/" + str(person.id) + ".json", 'w') as outfile:
        json.dump(data, outfile)
    currentPerson = currentPerson + 1

print("")
print("Total Chats: " + str(totalChatsMale + totalChatsFemale) + " (" + str(totalChatsMale) + " [m] und " + str(totalChatsFemale) + " [f])")
print("Total Messages: " + str(totalMessagesMale + totalMessagesFemale) + " (" + str(totalMessagesMale) + " [m] und " + str(totalMessagesFemale) + " [f])")
