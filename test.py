from knuddelsAPI import *
from functions import *
import json

username = "yourUsername"
password = "yourPassword"
sessionToken = login(username,password)
# print(sessionToken)
persons = getPersons(sessionToken)
# print(getConversation(sessionToken, "276232853228727893"))
print(len(persons))
for person in persons:
    messages = getAllMessagesPerConversation(sessionToken, person.conversationID)
    print(person.id + " - " + person.nick + " - " + str(len(messages)) + " Nachrichten")

# messages = getAllMessagesPerConversation(sessionToken, "261426327137922645")
# for message in messages:
#     print(message.senderID + " - " + message.formattedText.text)
# print(len(messages))
