import requests
import json


def getDeviceToken(username, password):
    params = {"operationName": "CreateDeviceToken", "variables": {"username": username,"password": password}, "query": 'query CreateDeviceToken($username: String!, $password: String!) {\n  login {\n    createDeviceToken(username: $username, password: $password) {\n      result\n      token\n      __typename\n    }\n    __typename\n  }\n}\n'}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params))
    req.raise_for_status()
    return req.text

def getRefreshSessionToken(deviceToken):
    headers={"authorization": "Bearer "+deviceToken}
    params = {"operationName": "RefreshSessionToken", "variables": {"clientInfo": {"type": "K3GraphQl", "clientVersion": {"major": 4, "minor": 19, "patch": 1, "buildInfo": "5021dcd1e6adf83d1e9ce602734713efe55c844a"}, "platform": "Native", "osInfo": {"type": "Ios", "version": "13.5.1"}}}, "query": "query RefreshSessionToken($clientInfo: ClientInfo!) {\n  login {\n    refreshSession(clientInfo: $clientInfo) {\n      expiry\n      token\n      __typename\n    }\n    __typename\n  }\n}\n"}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
    req.raise_for_status()
    return req.text

def getClientSettings(sessionToken):
    headers={"authorization": "Bearer "+sessionToken}
    params = {"operationName": "GetClientSettings", "variables": {}, "query": "query GetClientSettings {\n  clientSettings {\n    settings {\n      ...AllClientSettings\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AllClientSettings on ClientSettings {\n  conversationListFilterType\n  initialJoinBehavior\n  contactListTabs {\n    tabs {\n      tab\n      active\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
    req.raise_for_status()
    return req.text

def getCurrentServerTime(sessionToken):
    headers={"authorization": "Bearer "+sessionToken}
    params = {"operationName": "CurrentServerTime", "variables": {}, "query": "query CurrentServerTime {\n  currentTime\n}\n"}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
    req.raise_for_status()
    return req.text

def MessengerOverview(sessionToken):
    headers={"authorization": "Bearer "+sessionToken}
    params = {"operationName": "MessengerOverview", "variables": {"limit": 20,"before": null}, "query": "query MessengerOverview($limit: Int = 20, $before: UtcTimestamp = null) {\n  messenger {\n    conversations(limit: $limit, before: $before) {\n      conversations {\n        ...FullConversationWithoutMessages\n        __typename\n      }\n      hasMore\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment FullConversationWithoutMessages on MessengerConversation {\n  id\n  isArchived\n  otherParticipants {\n    ...MessengerBasicUser\n    age\n    albumPhotosUrl\n    canReceiveMessages\n    city\n    distance\n    gender\n    id\n    ignoreState\n    isIgnoring\n    isOnline\n    nick\n    profilePicture {\n      urlLargeSquare\n      urlVeryLarge\n      __typename\n    }\n    readMe\n    relationshipStatus\n    sexualOrientation\n    onlineMinutes\n    __typename\n  }\n  readState {\n    markedAsUnread\n    unreadMessageCount\n    lastReadMessage {\n      id\n      __typename\n    }\n    __typename\n  }\n  latestMessage {\n    ...MessengerMessage\n    __typename\n  }\n  __typename\n}\n\nfragment MessengerBasicUser on User {\n  id\n  nick\n  isOnline\n  canSendImages\n  __typename\n}\n\nfragment MessengerMessage on MessengerMessage {\n  id\n  nestedMessage {\n    id\n    sender {\n      id\n      nick\n      __typename\n    }\n    formattedText\n    timestamp\n    type\n    image {\n      url\n      __typename\n    }\n    __typename\n  }\n  sender {\n    ...MessengerBasicUser\n    __typename\n  }\n  starred\n  formattedText\n  timestamp\n  image {\n    url\n    __typename\n  }\n  snap {\n    url\n    duration\n    decryptionKey\n    __typename\n  }\n  __typename\n}\n"}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
    req.raise_for_status()
    return req.text

def getCurrentUserNick(sessionToken):
    headers={"authorization": "Bearer "+sessionToken}
    params = {"operationName": "GetCurrentUserNick", "variables": {}, "query": "query GetCurrentUserNick {\n  user {\n    currentUser {\n      id\n      nick\n      gender\n      __typename\n    }\n    __typename\n  }\n}\n"}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
    req.raise_for_status()
    return req.text

def UpdateLastSeen(sessionToken):
    headers={"authorization": "Bearer "+sessionToken}
    params = {"operationName": "UpdateLastSeen", "variables": {"isPresent": true}, "query": "mutation UpdateLastSeen($isPresent: Boolean!) {\n  user {\n    updateLastSeenTimestamp(isPresent: $isPresent)\n    __typename\n  }\n}\n"}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
    req.raise_for_status()
    return req.text

def FotomeetMatches(sessionToken):
    headers={"authorization": "Bearer "+sessionToken}
    params = {"operationName": "matches", "variables": {"limit": 100}, "query": "query matches($limit: Int) {\n  fotomeet {\n    matches(limit: $limit) {\n      user {\n        ...MatchUser\n        __typename\n      }\n      matchedAt\n      isNew\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment MatchUser on User {\n  nick\n  age\n  distance\n  gender\n  id\n  profilePicture {\n    urlLargeSquare\n    __typename\n  }\n  city\n  conversationId\n  __typename\n}\n"}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
    req.raise_for_status()
    return req.text

def FotoMeetStatus(sessionToken):
    headers={"authorization": "Bearer "+sessionToken}
    params = {"operationName": "fotoMeetStatus", "variables":{}, "query": "query fotoMeetStatus {\n  fotomeet {\n    status {\n      ...FotomeetStatus\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment FotomeetStatus on FotomeetStatus {\n  currentCandidate {\n    ...Candidate\n    __typename\n  }\n  prefetchImageUrls\n  votingUnavailableReason\n  isPremium\n  potentialMatchCount\n  __typename\n}\n\nfragment Candidate on FotomeetUser {\n  age\n  distance\n  gender\n  id\n  isPotentialMatch\n  userInfo {\n    id\n    nick\n    __typename\n  }\n  imageUrl\n  isReportable\n  hasAlbumPhotos\n  __typename\n}\n"}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
    req.raise_for_status()
    return req.text

def UserIsAdFree(sessionToken):
    headers={"authorization": "Bearer "+sessionToken}
    params = {"operationName": "UserIsAdFree", "variables": {}, "query": "query UserIsAdFree {\n  user {\n    currentUser {\n      ...UserWithAdFree\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment UserWithAdFree on User {\n  id\n  isAdFree\n  __typename\n}\n"}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
    req.raise_for_status()
    return req.text

def profileVisitors(sessionToken):
    headers={"authorization": "Bearer "+sessionToken}
    params = {"operationName": "profileVisitors", "variables": {}, "query": "query profileVisitors {\n  user {\n    profileVisitors {\n      visitors {\n        ...ProfileVisitorsUser\n        __typename\n      }\n      visibilityStatus\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ProfileVisitorsUser on User {\n  id\n  nick\n  age\n  gender\n  city\n  profilePicture {\n    urlLargeSquare\n    __typename\n  }\n  __typename\n}\n"}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
    req.raise_for_status()
    return req.text

def AllSmileyIds(sessionToken):
    headers={"authorization": "Bearer "+sessionToken}
    params = {"operationName": "AllSmileyIds", "variables": {}, "query": "query AllSmileyIds($limit: Int) {\n  smileybox {\n    smileyList(type: AllUsable, limit: $limit) {\n      id\n      __typename\n    }\n    __typename\n  }\n}\n"}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
    req.raise_for_status()
    return req.text

def RecentSmileys(sessionToken):
    headers={"authorization": "Bearer "+sessionToken}
    params = {"operationName": "RecentSmileys", "variables": {"limit": 10}, "query": "query RecentSmileys($limit: Int) {\n  smileybox {\n    smileyList(type: RecentlyUsed, limit: $limit) {\n      ...Smiley\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment Smiley on SmileyDetails {\n  id\n  image\n  textRepresentation\n  __typename\n}\n"}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
    req.raise_for_status()
    return req.text

def InitialChannelJoin(sessionToken):
    headers={"authorization": "Bearer "+sessionToken}
    params = {"operationName": "InitialJoin", "variables": {}, "query": "mutation InitialJoin {\n  channel {\n    initialJoin {\n      channels {\n        ...ActiveChannel\n        __typename\n      }\n      error {\n        ...ChannelJoinError\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ActiveChannel on Channel {\n  id\n  name\n  users {\n    ...ChannelUser\n    __typename\n  }\n  groupInfo {\n    backgroundColor {\n      ...Color\n      __typename\n    }\n    backgroundImageInfo {\n      mode\n      url\n      __typename\n    }\n    highlightColor {\n      ...Color\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ChannelUser on User {\n  id\n  nick\n  age\n  gender\n  profilePicture {\n    urlLargeSquare\n    __typename\n  }\n  __typename\n}\n\nfragment Color on Color {\n  alpha\n  blue\n  green\n  red\n  __typename\n}\n\nfragment ChannelJoinError on ChannelJoinMutationResponseError {\n  type\n  freetext\n  userNick\n  otherChannelName\n  minAge\n  maxUser\n  startTime\n  endTime\n  minKnuddels\n  minTradeableSmileys\n  minRegisteredDays\n  minStammiMonths\n  requiredGender\n  requiredStatusName\n  __typename\n}\n"}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
    req.raise_for_status()
    return req.text

def getChannel(sessionToken, channelID):
    headers={"authorization": "Bearer "+sessionToken}
    params = {"operationName": "GetChannel", "variables": {"channelId": channelID}, "query": "query GetChannel($channelId: ID!) {\n  channel {\n    channel(id: $channelId) {\n      ...ActiveChannel\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ActiveChannel on Channel {\n  id\n  name\n  users {\n    ...ChannelUser\n    __typename\n  }\n  groupInfo {\n    backgroundColor {\n      ...Color\n      __typename\n    }\n    backgroundImageInfo {\n      mode\n      url\n      __typename\n    }\n    highlightColor {\n      ...Color\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ChannelUser on User {\n  id\n  nick\n  age\n  gender\n  profilePicture {\n    urlLargeSquare\n    __typename\n  }\n  __typename\n}\n\nfragment Color on Color {\n  alpha\n  blue\n  green\n  red\n  __typename\n}\n"}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
    req.raise_for_status()
    return req.text

def getConversationWithoutMessages(sessionToken, conversationID):
    headers={"authorization": "Bearer "+sessionToken}
    params = {"operationName": "GetConversationWithoutMessages", "variables": {"id": conversationID}, "query": "query GetConversationWithoutMessages($id: ID!) {\n  messenger {\n    conversation(id: $id) {\n      ...FullConversationWithoutMessages\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment FullConversationWithoutMessages on MessengerConversation {\n  id\n  isArchived\n  otherParticipants {\n    ...MessengerBasicUser\n    age\n    albumPhotosUrl\n    canReceiveMessages\n    city\n    distance\n    gender\n    id\n    ignoreState\n    isIgnoring\n    isOnline\n    nick\n    profilePicture {\n      urlLargeSquare\n      urlVeryLarge\n      __typename\n    }\n    readMe\n    relationshipStatus\n    sexualOrientation\n    onlineMinutes\n    __typename\n  }\n  readState {\n    markedAsUnread\n    unreadMessageCount\n    lastReadMessage {\n      id\n      __typename\n    }\n    __typename\n  }\n  latestMessage {\n    ...MessengerMessage\n    __typename\n  }\n  __typename\n}\n\nfragment MessengerBasicUser on User {\n  id\n  nick\n  isOnline\n  canSendImages\n  __typename\n}\n\nfragment MessengerMessage on MessengerMessage {\n  id\n  nestedMessage {\n    id\n    sender {\n      id\n      nick\n      __typename\n    }\n    formattedText\n    timestamp\n    type\n    image {\n      url\n      __typename\n    }\n    __typename\n  }\n  sender {\n    ...MessengerBasicUser\n    __typename\n  }\n  starred\n  formattedText\n  timestamp\n  image {\n    url\n    __typename\n  }\n  snap {\n    url\n    duration\n    decryptionKey\n    __typename\n  }\n  __typename\n}\n"}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
    req.raise_for_status()
    return req.text

def JoinChannelById(sessionToken, channelID):
    headers={"authorization": "Bearer "+sessionToken}
    params = {"operationName": "JoinChannelById", "variables": {"channelId": channelID}, "query": "mutation JoinChannelById($channelId: ID!) {\n  channel {\n    joinById(id: $channelId) {\n      channel {\n        ...ActiveChannel\n        __typename\n      }\n      error {\n        ...ChannelJoinError\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ActiveChannel on Channel {\n  id\n  name\n  users {\n    ...ChannelUser\n    __typename\n  }\n  groupInfo {\n    backgroundColor {\n      ...Color\n      __typename\n    }\n    backgroundImageInfo {\n      mode\n      url\n      __typename\n    }\n    highlightColor {\n      ...Color\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ChannelUser on User {\n  id\n  nick\n  age\n  gender\n  profilePicture {\n    urlLargeSquare\n    __typename\n  }\n  __typename\n}\n\nfragment Color on Color {\n  alpha\n  blue\n  green\n  red\n  __typename\n}\n\nfragment ChannelJoinError on ChannelJoinMutationResponseError {\n  type\n  freetext\n  userNick\n  otherChannelName\n  minAge\n  maxUser\n  startTime\n  endTime\n  minKnuddels\n  minTradeableSmileys\n  minRegisteredDays\n  minStammiMonths\n  requiredGender\n  requiredStatusName\n  __typename\n}\n"}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
    req.raise_for_status()
    return req.text

def fotoMeetVote(sessionToken, candidateID, vote): # vote = "YES" or vote = "NO"
    headers={"authorization": "Bearer "+sessionToken}
    params = {"operationName": "fotoMeetVote", "variables": {"id": candidateID, "vote": vote}, "query": "mutation fotoMeetVote($id: ID!, $vote: FotomeetVote!) {\n  fotomeet {\n    vote(id: $id, type: $vote) {\n      ...VoteResponse\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment VoteResponse on FotomeetVoteResponse {\n  error\n  newStatus {\n    ...FotomeetStatus\n    __typename\n  }\n  __typename\n}\n\nfragment FotomeetStatus on FotomeetStatus {\n  currentCandidate {\n    ...Candidate\n    __typename\n  }\n  prefetchImageUrls\n  votingUnavailableReason\n  isPremium\n  potentialMatchCount\n  __typename\n}\n\nfragment Candidate on FotomeetUser {\n  age\n  distance\n  gender\n  id\n  isPotentialMatch\n  userInfo {\n    id\n    nick\n    __typename\n  }\n  imageUrl\n  isReportable\n  hasAlbumPhotos\n  __typename\n}\n"}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
    req.raise_for_status()
    return req.text

def UserIsOnline(sessionToken, userID):
    headers={"authorization": "Bearer "+sessionToken}
    params = {"operationName": "UserIsOnline", "variables": {"id": userID}, "query": "query UserIsOnline($id: ID!) {\n  user {\n    user(id: $id) {\n      ...UserWithOnline\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment UserWithOnline on User {\n  id\n  isOnline\n  __typename\n}\n"}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
    req.raise_for_status()
    return req.text

def UserIsOnlineInChannel(sessionToken, userID):
    headers={"authorization": "Bearer "+sessionToken}
    params = {"operationName": "UserIsOnlineInChannel", "variables": {"id": userID}, "query": "query UserIsOnlineInChannel($id: ID!) {\n  user {\n    user(id: $id) {\n      ...UserWithOnlineAndChannel\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment UserWithOnlineAndChannel on User {\n  id\n  isOnline\n  latestOnlineChannelName\n  __typename\n}\n"}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
    req.raise_for_status()
    return req.text

def getConversation(sessionToken, messageCount, beforeMessageID, conversationID): # messageCount = 50, beforeMessageID = null
    headers={"authorization": "Bearer "+sessionToken}
    params = {"operationName": "GetConversation", "variables": {"messageCount": messageCount,"beforeMessageId": beforeMessageID, "id": conversationID}, "query": "query GetConversation($id: ID!, $messageCount: Int = 50, $beforeMessageId: ID = null) {\n  messenger {\n    conversation(id: $id) {\n      ...FullConversation\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment FullConversation on MessengerConversation {\n  ...FullConversationWithoutMessages\n  messages(limit: $messageCount, beforeMessageId: $beforeMessageId) {\n    messages {\n      ...MessengerMessage\n      __typename\n    }\n    hasMore\n    __typename\n  }\n  __typename\n}\n\nfragment FullConversationWithoutMessages on MessengerConversation {\n  id\n  isArchived\n  otherParticipants {\n    ...MessengerBasicUser\n    age\n    albumPhotosUrl\n    canReceiveMessages\n    city\n    distance\n    gender\n    id\n    ignoreState\n    isIgnoring\n    isOnline\n    nick\n    profilePicture {\n      urlLargeSquare\n      urlVeryLarge\n      __typename\n    }\n    readMe\n    relationshipStatus\n    sexualOrientation\n    onlineMinutes\n    __typename\n  }\n  readState {\n    markedAsUnread\n    unreadMessageCount\n    lastReadMessage {\n      id\n      __typename\n    }\n    __typename\n  }\n  latestMessage {\n    ...MessengerMessage\n    __typename\n  }\n  __typename\n}\n\nfragment MessengerBasicUser on User {\n  id\n  nick\n  isOnline\n  canSendImages\n  __typename\n}\n\nfragment MessengerMessage on MessengerMessage {\n  id\n  nestedMessage {\n    id\n    sender {\n      id\n      nick\n      __typename\n    }\n    formattedText\n    timestamp\n    type\n    image {\n      url\n      __typename\n    }\n    __typename\n  }\n  sender {\n    ...MessengerBasicUser\n    __typename\n  }\n  starred\n  formattedText\n  timestamp\n  image {\n    url\n    __typename\n  }\n  snap {\n    url\n    duration\n    decryptionKey\n    __typename\n  }\n  __typename\n}\n"}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
    req.raise_for_status()
    return req.text

def MessengerMarkConversationAsRead(sessionToken, conversationID):
    headers={"authorization": "Bearer "+sessionToken}
    params = {"operationName": "MessengerMarkConversationsAsRead", "variables": {"ids":[conversationID]}, "query": "mutation MessengerMarkConversationsAsRead($ids: [ID!]!) {\n  messenger {\n    readConversations(ids: $ids) {\n      error\n      conversation {\n        id\n        readState {\n          lastReadMessage {\n            id\n            __typename\n          }\n          markedAsUnread\n          unreadMessageCount\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
    req.raise_for_status()
    return req.text

def SendTyping(sessionToken, conversationID):
    headers={"authorization": "Bearer "+sessionToken}
    params = {"operationName": "SendTyping", "variables": {"id": conversationID}, "query": "mutation SendTyping($id: ID!) {\n  messenger {\n    notifyTyping(conversationId: $id) {\n      error\n      __typename\n    }\n    __typename\n  }\n}\n"}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
    req.raise_for_status()
    return req.text

def MessengerSendMessage(sessionToken, conversationID, message):
    headers={"authorization": "Bearer "+sessionToken}
    params = {"operationName": "MessengerSendMessage", "variables": {"id": conversationID,"text": message}, "query": "mutation MessengerSendMessage($id: ID!, $text: String!) {\n  messenger {\n    sendMessage(conversationId: $id, text: $text) {\n      error {\n        type\n        filterReason\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
    req.raise_for_status()
    return req.text

def NotifyProfileVisited(sessionToken, userID):
    headers={"authorization": "Bearer "+sessionToken}
    params = {"operationName": "NotifyProfileVisited", "variables":{"userId": userID}, "query": "mutation NotifyProfileVisited($userId: ID!) {\n  user {\n    notifyProfileVisited(userId: $userId)\n    __typename\n  }\n}\n"}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
    req.raise_for_status()
    return req.text

def getProfilePictureUrls(sessionToken, userID):
    headers={"authorization": "Bearer "+sessionToken}
    params = {"operationName": "GetProfilePictureUrls", "variables": {"userId": userID}, "query": "query GetProfilePictureUrls($userId: ID!) {\n  user {\n    user(id: $userId) {\n      id\n      profilePicture {\n        urlLargeSquare\n        urlVeryLarge\n        exists\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
    req.raise_for_status()
    return req.text

def getUserProfile(sessionToken, userID):
    headers={"authorization": "Bearer "+sessionToken}
    params = {"operationName": "GetUserForProfile", "variables": {"userId": userID}, "query": "query GetUserForProfile($userId: ID!) {\n  user {\n    user(id: $userId) {\n      ...UserForProfile\n      __typename\n    }\n    __typename\n  }\n  messenger {\n    conversationWithParticipants(otherParticipantIds: [$userId]) {\n      id\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment UserForProfile on User {\n  id\n  nick\n  age\n  gender\n  sexualOrientation\n  relationshipStatus\n  city\n  distance\n  canReceiveMessages\n  profilePicture {\n    urlLargeSquare\n    urlVeryLarge\n    exists\n    __typename\n  }\n  albumPhotosUrl\n  readMe\n  name\n  dateOfBirth\n  country\n  children\n  smoker\n  hobbies\n  music\n  movies\n  series\n  books\n  languages\n  lastOnlineTime\n  dateOfRegistration\n  status\n  supportsKnuddelsPhilosophy\n  teams\n  stammiMonths\n  latestOnlineChannelName\n  myChannelName\n  moderatedChannelName\n  moderatedMyChannelNames\n  hickeys\n  flowers\n  roses\n  chatMeetups\n  receivedHearts\n  givenHeart\n  mentorPoints\n  onlineMinutes\n  isReportable\n  __typename\n}\n"}
    req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
    req.raise_for_status()
    return req.text
