from knuddelsAPI import *
from functions import *

from knuddelsAPI2 import KnuddelsAPI

username = "cute mia2000w"
password = "qwertzuiop"
#username = "lea16w"
#password = "qwertzpoiuz"
sessionToken = login(username,password)
userid = "0" # James
conversationID = "287577631384732034" # with DonJon23m
albumPhotoID = "derwahremugel-pro0vl0p"
channelID = "1985598:1"
#print(MessengerMarkConversationAsRead(sessionToken, conversationID))

api = KnuddelsAPI(username, password)
print(api.sendMessageInChannel(channelID, "hi zusammen!"))