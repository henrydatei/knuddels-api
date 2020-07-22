from knuddelsAPI import *
import json

def login(username,password):
    deviceToken = json.loads(getDeviceToken(username,password))['data']['login']['createDeviceToken']['token']
    sessionToken = json.loads(getRefreshSessionToken(deviceToken))['data']['login']['refreshSession']['token']

    return sessionToken
