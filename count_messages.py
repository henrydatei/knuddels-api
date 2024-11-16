from knuddelsAPI import KnuddelsAPI
from tqdm import tqdm
from decouple import config

# get username and password from .env file
username = config("KNUDDELS_USERNAME")
password = config("KNUDDELS_PASSWORD")

api = KnuddelsAPI(username, password)

conversations = api.getConversations(beforeTimestamp=None)
totalMessagesMale = 0
totalChatsMale = 0
totalMessagesFemale = 0
totalChatsFemale = 0
totalMessagesOther = 0
totalChatsOther = 0

for conversation in tqdm(conversations):
    gender = conversation.otherParticipants[0].gender
    messages = api.getMessagesForConversation(conversation.id, beforeMessageID=None)
    if gender == 'MALE':
        totalChatsMale += 1
        totalMessagesMale += len(messages)
    elif gender == 'FEMALE':
        totalChatsFemale += 1
        totalMessagesFemale += len(messages)
    else:
        totalChatsOther += 1
        totalMessagesOther += len(messages)
        
print(f"Total Chats: {totalChatsMale + totalChatsFemale + totalChatsOther} ({totalChatsMale} [m], {totalChatsFemale} [f], {totalChatsOther} [o])")
print(f"Total Messages: {totalMessagesMale + totalMessagesFemale + totalMessagesOther} ({totalMessagesMale} [m], {totalMessagesFemale} [f], {totalMessagesOther} [o])")