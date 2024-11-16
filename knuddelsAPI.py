import dataclasses
import json
import requests
from dacite import from_dict
from typing import List, Tuple, Literal, Optional

from classes.ClientSettings import ClientSettings
from classes.User import User
from classes.FotomeetMatch import FotomeetMatch
from classes.FotomeetStatus import FotomeetStatus
from classes.FotomeetVoteResponse import FotomeetVoteResponse
from classes.ProfileVisitors import ProfileVisitors
from classes.SmileyDetails import SmileyDetails
from classes.Channel import Channel
from classes.ProfilePicture import ProfilePicture
from classes.Conversation import Conversation
from classes.Message import Message
from classes.ChannelCategory import ChannelCategory
from classes.ContactFilterSettings import ContactFilterSettings
from classes.ContactFilterSettingsConstraints import ContactFilterSettingsConstraints
from classes.AlbumPhotoComment import AlbumPhotoComment
from classes.ComplaintReason import ComplaintReason

@dataclasses.dataclass
class KnuddelsAPI:
    username: str
    password: str
    sessionToken: str = dataclasses.field(init = False)

    def __post_init__(self) -> None:
        self.sessionToken = self.login(self.username, self.password)

    def getDeviceToken(self, username: str, password: str) -> str:
        params = {"operationName": "CreateDeviceToken", "variables": {"username": username,"password": password}, "query": 'query CreateDeviceToken($username: String!, $password: String!) {\n  login {\n    createDeviceToken(username: $username, password: $password) {\n      result\n      token\n      __typename\n    }\n    __typename\n  }\n}\n'}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params))
        req.raise_for_status()
        return req.json()
    
    def getRefreshSessionToken(self, deviceToken: str) -> str:
        headers={"authorization": "Bearer "+deviceToken}
        params = {"operationName":"RefreshSessionToken","variables":{"sessionInfo":{"type":"K3GraphQl","clientVersion":{"major":4,"minor":22,"patch":8,"buildInfo":"dd34485a181477347adee04f166323c39d6db397"},"platform":"Native","osInfo":{"type":"Ios","version":"14.6"},"deviceIdentifiers":["E696701F-2098-4266-A040-B84FD740A6CF"]}},"query":"query RefreshSessionToken($sessionInfo: SessionInfo!, $oldSessionToken: SessionToken) {\n  login {\n    refreshSession(sessionInfo: $sessionInfo, token: $oldSessionToken) {\n      ... on RefreshSessionSuccess {\n        expiry\n        token\n        __typename\n      }\n      ...RefreshSessionError\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment RefreshSessionError on RefreshSessionError {\n  errorMessage\n  user {\n    ...UserWithLockInfo\n    __typename\n  }\n  __typename\n}\n\nfragment UserWithLockInfo on User {\n  id\n  nick\n  lockInfo {\n    ... on UnlockedLockInfo {\n      __typename\n    }\n    ... on TemporaryLockInfo {\n      lockReason\n      lockedBy {\n        id\n        nick\n        __typename\n      }\n      lockedUntilDate\n      __typename\n    }\n    ... on PermanentLockInfo {\n      lockReason\n      lockedBy {\n        id\n        nick\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return req.json()

    def login(self, username: str, password: str) -> str:
        deviceToken = self.getDeviceToken(username,password)['data']['login']['createDeviceToken']['token']
        sessionToken = self.getRefreshSessionToken(deviceToken)['data']['login']['refreshSession']['token']
        return sessionToken
    
    def getClientSettings(self) -> ClientSettings:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName": "GetClientSettings", "variables": {}, "query": "query GetClientSettings {\n  clientSettings {\n    settings {\n      ...AllClientSettings\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AllClientSettings on ClientSettings {\n  conversationListFilterType\n  initialJoinBehavior\n  contactListTabs {\n    tabs {\n      tab\n      active\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return from_dict(data_class = ClientSettings, data = req.json()['data']['clientSettings']['settings'])
    
    def getCurrentServerTime(self) -> str:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName": "CurrentServerTime", "variables": {}, "query": "query CurrentServerTime {\n  currentTime\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return req.json()['data']['currentTime']
    
    def getCurrentUserNick(self) -> User:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName": "GetCurrentUserNick", "variables": {}, "query": "query GetCurrentUserNick {\n  user {\n    currentUser {\n      id\n      nick\n      gender\n      __typename\n    }\n    __typename\n  }\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return from_dict(data_class = User, data = req.json()['data']['user']['currentUser'])
    
    def updateLastSeen(self) -> bool:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName": "UpdateLastSeen", "variables": {"isPresent": True}, "query": "mutation UpdateLastSeen($isPresent: Boolean!) {\n  user {\n    updateLastSeenTimestamp(isPresent: $isPresent)\n    __typename\n  }\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return req.json()['data']['user']['updateLastSeenTimestamp']
    
    def getFotomeetMatches(self) -> List[FotomeetMatch]:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName": "matches", "variables": {"limit": 100}, "query": "query matches($limit: Int) {\n  fotomeet {\n    matches(limit: $limit) {\n      user {\n        ...MatchUser\n        __typename\n      }\n      matchedAt\n      isNew\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment MatchUser on User {\n  nick\n  age\n  distance\n  gender\n  id\n  profilePicture {\n    urlLargeSquare\n    __typename\n  }\n  city\n  conversationId\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return [from_dict(data_class = FotomeetMatch, data = match) for match in req.json()['data']['fotomeet']['matches']]
    
    def getFotoMeetStatus(self) -> FotomeetStatus:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName": "fotoMeetStatus", "variables":{}, "query": "query fotoMeetStatus {\n  fotomeet {\n    status {\n      ...FotomeetStatus\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment FotomeetStatus on FotomeetStatus {\n  currentCandidate {\n    ...Candidate\n    __typename\n  }\n  prefetchImageUrls\n  votingUnavailableReason\n  isPremium\n  potentialMatchCount\n  __typename\n}\n\nfragment Candidate on FotomeetUser {\n  age\n  distance\n  gender\n  id\n  isPotentialMatch\n  userInfo {\n    id\n    nick\n    __typename\n  }\n  imageUrl\n  isReportable\n  hasAlbumPhotos\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return from_dict(data_class = FotomeetStatus, data = req.json()['data']['fotomeet']['status'])
    
    def fotoMeetVote(self, userID: str, vote: Literal["YES", "NO"]) -> FotomeetVoteResponse:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName": "fotoMeetVote", "variables": {"id": userID, "vote": vote}, "query": "mutation fotoMeetVote($id: ID!, $vote: FotomeetVote!) {\n  fotomeet {\n    vote(id: $id, type: $vote) {\n      ...VoteResponse\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment VoteResponse on FotomeetVoteResponse {\n  error\n  newStatus {\n    ...FotomeetStatus\n    __typename\n  }\n  __typename\n}\n\nfragment FotomeetStatus on FotomeetStatus {\n  currentCandidate {\n    ...Candidate\n    __typename\n  }\n  prefetchImageUrls\n  votingUnavailableReason\n  isPremium\n  potentialMatchCount\n  __typename\n}\n\nfragment Candidate on FotomeetUser {\n  age\n  distance\n  gender\n  id\n  isPotentialMatch\n  userInfo {\n    id\n    nick\n    __typename\n  }\n  imageUrl\n  isReportable\n  hasAlbumPhotos\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return from_dict(data_class = FotomeetVoteResponse, data = req.json()['data']['fotomeet']['vote'])
    
    def isUserAdFree(self) -> bool:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName": "UserIsAdFree", "variables": {}, "query": "query UserIsAdFree {\n  user {\n    currentUser {\n      ...UserWithAdFree\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment UserWithAdFree on User {\n  id\n  isAdFree\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return req.json()['data']['user']['currentUser']['isAdFree']
    
    def profileVisitors(self) -> ProfileVisitors:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName": "profileVisitors", "variables": {}, "query": "query profileVisitors {\n  user {\n    profileVisitors {\n      visitors {\n        ...ProfileVisitorsUser\n        __typename\n      }\n      visibilityStatus\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ProfileVisitorsUser on User {\n  id\n  nick\n  age\n  gender\n  city\n  profilePicture {\n    urlLargeSquare\n    __typename\n  }\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return from_dict(data_class = ProfileVisitors, data = req.json()['data']['user']['profileVisitors'])
    
    def allSmileyIds(self) -> List[SmileyDetails]:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName": "AllSmileyIds", "variables": {}, "query": "query AllSmileyIds($limit: Int) {\n  smileybox {\n    smileyList(type: AllUsable, limit: $limit) {\n      id\n      __typename\n    }\n    __typename\n  }\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return [from_dict(data_class = SmileyDetails, data = smiley) for smiley in req.json()['data']['smileybox']['smileyList']]
    
    def initialChannelJoin(self) -> List[Channel]:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName": "InitialJoin", "variables": {}, "query": "mutation InitialJoin {\n  channel {\n    initialJoin {\n      channels {\n        ...ActiveChannel\n        __typename\n      }\n      error {\n        ...ChannelJoinError\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ActiveChannel on Channel {\n  id\n  name\n  users {\n    ...ChannelUser\n    __typename\n  }\n  groupInfo {\n    backgroundColor {\n      ...Color\n      __typename\n    }\n    backgroundImageInfo {\n      mode\n      url\n      __typename\n    }\n    highlightColor {\n      ...Color\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ChannelUser on User {\n  id\n  nick\n  age\n  gender\n  profilePicture {\n    urlLargeSquare\n    __typename\n  }\n  __typename\n}\n\nfragment Color on Color {\n  alpha\n  blue\n  green\n  red\n  __typename\n}\n\nfragment ChannelJoinError on ChannelJoinMutationResponseError {\n  type\n  freetext\n  userNick\n  otherChannelName\n  minAge\n  maxUser\n  startTime\n  endTime\n  minKnuddels\n  minTradeableSmileys\n  minRegisteredDays\n  minStammiMonths\n  requiredGender\n  requiredStatusName\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return [from_dict(data_class = Channel, data = channel) for channel in req.json()['data']['channel']['initialJoin']['channels']]
    
    def getChannel(self, channelID: str) -> Channel:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName": "GetChannel", "variables": {"channelId": channelID}, "query": "query GetChannel($channelId: ID!) {\n  channel {\n    channel(id: $channelId) {\n      ...ActiveChannel\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ActiveChannel on Channel {\n  id\n  name\n  users {\n    ...ChannelUser\n    __typename\n  }\n  groupInfo {\n    backgroundColor {\n      ...Color\n      __typename\n    }\n    backgroundImageInfo {\n      mode\n      url\n      __typename\n    }\n    highlightColor {\n      ...Color\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ChannelUser on User {\n  id\n  nick\n  age\n  gender\n  profilePicture {\n    urlLargeSquare\n    __typename\n  }\n  __typename\n}\n\nfragment Color on Color {\n  alpha\n  blue\n  green\n  red\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return from_dict(data_class = Channel, data = req.json()['data']['channel']['channel'])
    
    def joinChannelById(self, channelID: str) -> Channel:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName": "JoinChannelById", "variables": {"channelId": channelID}, "query": "mutation JoinChannelById($channelId: ID!) {\n  channel {\n    joinById(id: $channelId) {\n      channel {\n        ...ActiveChannel\n        __typename\n      }\n      error {\n        ...ChannelJoinError\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ActiveChannel on Channel {\n  id\n  name\n  users {\n    ...ChannelUser\n    __typename\n  }\n  groupInfo {\n    backgroundColor {\n      ...Color\n      __typename\n    }\n    backgroundImageInfo {\n      mode\n      url\n      __typename\n    }\n    highlightColor {\n      ...Color\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ChannelUser on User {\n  id\n  nick\n  age\n  gender\n  profilePicture {\n    urlLargeSquare\n    __typename\n  }\n  __typename\n}\n\nfragment Color on Color {\n  alpha\n  blue\n  green\n  red\n  __typename\n}\n\nfragment ChannelJoinError on ChannelJoinMutationResponseError {\n  type\n  freetext\n  userNick\n  otherChannelName\n  minAge\n  maxUser\n  startTime\n  endTime\n  minKnuddels\n  minTradeableSmileys\n  minRegisteredDays\n  minStammiMonths\n  requiredGender\n  requiredStatusName\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return from_dict(data_class = Channel, data = req.json()['data']['channel']['joinById']['channel'])
    
    def isUserOnline(self, userID: str) -> bool:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName": "UserIsOnline", "variables": {"id": userID}, "query": "query UserIsOnline($id: ID!) {\n  user {\n    user(id: $id) {\n      ...UserWithOnline\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment UserWithOnline on User {\n  id\n  isOnline\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return req.json()['data']['user']['user']['isOnline']
    
    def isUserOnlineAndLastChannel(self, userID: str) -> Tuple[bool, str]:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName": "UserIsOnlineInChannel", "variables": {"id": userID}, "query": "query UserIsOnlineInChannel($id: ID!) {\n  user {\n    user(id: $id) {\n      ...UserWithOnlineAndChannel\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment UserWithOnlineAndChannel on User {\n  id\n  isOnline\n  latestOnlineChannelName\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return (req.json()['data']['user']['user']['isOnline'], req.json()['data']['user']['user']['latestOnlineChannelName'])
    
    def notifyProfileVisited(self, userID: str) -> None:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName": "NotifyProfileVisited", "variables":{"userId": userID}, "query": "mutation NotifyProfileVisited($userId: ID!) {\n  user {\n    notifyProfileVisited(userId: $userId)\n    __typename\n  }\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()

    def getProfilePictureUrls(self, userID: str) -> ProfilePicture:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName": "GetProfilePictureUrls", "variables": {"userId": userID}, "query": "query GetProfilePictureUrls($userId: ID!) {\n  user {\n    user(id: $userId) {\n      id\n      profilePicture {\n        urlLargeSquare\n        urlVeryLarge\n        exists\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return from_dict(data_class = ProfilePicture, data = req.json()['data']['user']['user']['profilePicture'])
    
    def getUserProfile(self, userID: str) -> Tuple[User, Conversation]:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName": "GetUserForProfile", "variables": {"userId": userID}, "query": "query GetUserForProfile($userId: ID!) {\n  user {\n    user(id: $userId) {\n      ...UserForProfile\n      __typename\n    }\n    __typename\n  }\n  messenger {\n    conversationWithParticipants(otherParticipantIds: [$userId]) {\n      id\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment UserForProfile on User {\n  id\n  nick\n  age\n  gender\n  sexualOrientation\n  relationshipStatus\n  city\n  distance\n  canReceiveMessages\n  profilePicture {\n    urlLargeSquare\n    urlVeryLarge\n    exists\n    __typename\n  }\n  albumPhotosUrl\n  readMe\n  name\n  dateOfBirth\n  country\n  children\n  smoker\n  hobbies\n  music\n  movies\n  series\n  books\n  languages\n  lastOnlineTime\n  dateOfRegistration\n  status\n  supportsKnuddelsPhilosophy\n  teams\n  stammiMonths\n  latestOnlineChannelName\n  myChannelName\n  moderatedChannelName\n  moderatedMyChannelNames\n  hickeys\n  flowers\n  roses\n  chatMeetups\n  receivedHearts\n  givenHeart\n  mentorPoints\n  onlineMinutes\n  isReportable\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return (from_dict(data_class = User, data = req.json()['data']['user']['user']), from_dict(data_class = Conversation, data = req.json()['data']['messenger']['conversationWithParticipants']))
    
    def getContacts(self, type: Literal["Watchlist", "Fotomeet", "Mentee", "Latest"]) -> List[User]:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName":"GetContacts","variables":{"filter":{"type":type}},"query":"query GetContacts($filter: ContactListFilter) {\n  user {\n    contactList(filter: $filter) {\n      contacts {\n        ...ContactsUser\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ContactsUser on User {\n  id\n  nick\n  profilePicture {\n    urlLargeSquare\n    __typename\n  }\n  isOnline\n  readMe\n  canReceiveMessages\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return [from_dict(data_class = User, data = user) for user in req.json()['data']['user']['contactList']['contacts']]
    
    def getConversations(self, beforeTimestamp: Optional[str]) -> List[Conversation]:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName": "MessengerOverview", "variables": {"limit": 50,"before": beforeTimestamp}, "query": "query MessengerOverview($limit: Int = 20, $before: UtcTimestamp = null) {\n  messenger {\n    conversations(limit: $limit, before: $before) {\n      conversations {\n        ...FullConversationWithoutMessages\n        __typename\n      }\n      hasMore\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment FullConversationWithoutMessages on MessengerConversation {\n  id\n  isArchived\n  otherParticipants {\n    ...MessengerBasicUser\n    age\n    albumPhotosUrl\n    canReceiveMessages\n    city\n    distance\n    gender\n    id\n    ignoreState\n    isIgnoring\n    isOnline\n    nick\n    profilePicture {\n      urlLargeSquare\n      urlVeryLarge\n      __typename\n    }\n    readMe\n    relationshipStatus\n    sexualOrientation\n    onlineMinutes\n    __typename\n  }\n  readState {\n    markedAsUnread\n    unreadMessageCount\n    lastReadMessage {\n      id\n      __typename\n    }\n    __typename\n  }\n  latestMessage {\n    ...MessengerMessage\n    __typename\n  }\n  __typename\n}\n\nfragment MessengerBasicUser on User {\n  id\n  nick\n  isOnline\n  canSendImages\n  __typename\n}\n\nfragment MessengerMessage on MessengerMessage {\n  id\n  nestedMessage {\n    id\n    sender {\n      id\n      nick\n      __typename\n    }\n    formattedText\n    timestamp\n    type\n    image {\n      url\n      __typename\n    }\n    __typename\n  }\n  sender {\n    ...MessengerBasicUser\n    __typename\n  }\n  starred\n  formattedText\n  timestamp\n  image {\n    url\n    __typename\n  }\n  snap {\n    url\n    duration\n    decryptionKey\n    __typename\n  }\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        
        conversations = [from_dict(data_class = Conversation, data = conversation) for conversation in req.json()['data']['messenger']['conversations']['conversations']]

        if req.json()['data']['messenger']['conversations']['hasMore']:
            conversations += self.getConversations(beforeTimestamp = conversations[0].latestMessage.timestamp)

        return conversations
    
    def getConversation(self, conversationID: str) -> Conversation:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName": "GetConversationWithoutMessages", "variables": {"id": conversationID}, "query": "query GetConversationWithoutMessages($id: ID!) {\n  messenger {\n    conversation(id: $id) {\n      ...FullConversationWithoutMessages\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment FullConversationWithoutMessages on MessengerConversation {\n  id\n  isArchived\n  otherParticipants {\n    ...MessengerBasicUser\n    age\n    albumPhotosUrl\n    canReceiveMessages\n    city\n    distance\n    gender\n    id\n    ignoreState\n    isIgnoring\n    isOnline\n    nick\n    profilePicture {\n      urlLargeSquare\n      urlVeryLarge\n      __typename\n    }\n    readMe\n    relationshipStatus\n    sexualOrientation\n    onlineMinutes\n    __typename\n  }\n  readState {\n    markedAsUnread\n    unreadMessageCount\n    lastReadMessage {\n      id\n      __typename\n    }\n    __typename\n  }\n  latestMessage {\n    ...MessengerMessage\n    __typename\n  }\n  __typename\n}\n\nfragment MessengerBasicUser on User {\n  id\n  nick\n  isOnline\n  canSendImages\n  __typename\n}\n\nfragment MessengerMessage on MessengerMessage {\n  id\n  nestedMessage {\n    id\n    sender {\n      id\n      nick\n      __typename\n    }\n    formattedText\n    timestamp\n    type\n    image {\n      url\n      __typename\n    }\n    __typename\n  }\n  sender {\n    ...MessengerBasicUser\n    __typename\n  }\n  starred\n  formattedText\n  timestamp\n  image {\n    url\n    __typename\n  }\n  snap {\n    url\n    duration\n    decryptionKey\n    __typename\n  }\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return from_dict(data_class = Conversation, data = req.json()['data']['messenger']['conversation'])
    
    def getMessagesForConversation(self, conversationID: str, beforeMessageID: Optional[str], messageCount: int = 50) -> List[Message]:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName": "GetConversation", "variables": {"messageCount": messageCount,"beforeMessageId": beforeMessageID, "id": conversationID}, "query": "query GetConversation($id: ID!, $messageCount: Int = 50, $beforeMessageId: ID = null) {\n  messenger {\n    conversation(id: $id) {\n      ...FullConversation\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment FullConversation on MessengerConversation {\n  ...FullConversationWithoutMessages\n  messages(limit: $messageCount, beforeMessageId: $beforeMessageId) {\n    messages {\n      ...MessengerMessage\n      __typename\n    }\n    hasMore\n    __typename\n  }\n  __typename\n}\n\nfragment FullConversationWithoutMessages on MessengerConversation {\n  id\n  isArchived\n  otherParticipants {\n    ...MessengerBasicUser\n    age\n    albumPhotosUrl\n    canReceiveMessages\n    city\n    distance\n    gender\n    id\n    ignoreState\n    isIgnoring\n    isOnline\n    nick\n    profilePicture {\n      urlLargeSquare\n      urlVeryLarge\n      __typename\n    }\n    readMe\n    relationshipStatus\n    sexualOrientation\n    onlineMinutes\n    __typename\n  }\n  readState {\n    markedAsUnread\n    unreadMessageCount\n    lastReadMessage {\n      id\n      __typename\n    }\n    __typename\n  }\n  latestMessage {\n    ...MessengerMessage\n    __typename\n  }\n  __typename\n}\n\nfragment MessengerBasicUser on User {\n  id\n  nick\n  isOnline\n  canSendImages\n  __typename\n}\n\nfragment MessengerMessage on MessengerMessage {\n  id\n  nestedMessage {\n    id\n    sender {\n      id\n      nick\n      __typename\n    }\n    formattedText\n    timestamp\n    type\n    image {\n      url\n      __typename\n    }\n    __typename\n  }\n  sender {\n    ...MessengerBasicUser\n    __typename\n  }\n  starred\n  formattedText\n  timestamp\n  image {\n    url\n    __typename\n  }\n  snap {\n    url\n    duration\n    decryptionKey\n    __typename\n  }\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        
        messages = [from_dict(data_class = Message, data = message) for message in req.json()['data']['messenger']['conversation']['messages']['messages']]
        
        if req.json()['data']['messenger']['conversation']['messages']['hasMore']:
            messages += self.getMessagesForConversation(conversationID, beforeMessageID = messages[0].id, messageCount = messageCount)
            
        return messages
    
    def sendTyping(self, conversationID: str) -> None:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName": "SendTyping", "variables": {"id": conversationID}, "query": "mutation SendTyping($id: ID!) {\n  messenger {\n    notifyTyping(conversationId: $id) {\n      error\n      __typename\n    }\n    __typename\n  }\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        
    def sendMessage(self, conversationID: str, message: str) -> None:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName": "MessengerSendMessage", "variables": {"id": conversationID,"text": message}, "query": "mutation MessengerSendMessage($id: ID!, $text: String!) {\n  messenger {\n    sendMessage(conversationId: $id, text: $text) {\n      error {\n        type\n        filterReason\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        
    def markConversationAsRead(self, conversationID: str) -> None:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName": "MessengerMarkConversationsAsRead", "variables": {"ids":[conversationID]}, "query": "mutation MessengerMarkConversationsAsRead($ids: [ID!]!) {\n  messenger {\n    readConversations(ids: $ids) {\n      error\n      conversation {\n        id\n        readState {\n          lastReadMessage {\n            id\n            __typename\n          }\n          markedAsUnread\n          unreadMessageCount\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        
    def markConversationAsUnread(self, conversationID: str) -> None:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName":"MessengerMarkConversationAsUnread","variables":{"id":conversationID},"query":"mutation MessengerMarkConversationAsUnread($id: ID!) {\n  messenger {\n    markConversationUnread(id: $id) {\n      error\n      conversation {\n        id\n        readState {\n          lastReadConversationMessage {\n            id\n            __typename\n          }\n          markedAsUnread\n          unreadMessageCount\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        
    def getChannelListOverview(self) -> List[ChannelCategory]:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName":"GetChannelListOverview","variables":{"groupAmount":5,"pixelDensity":2},"query":"query GetChannelListOverview($groupAmount: Int!, $pixelDensity: Float!) {\n  channel {\n    channelAds(limit: 3) {\n      ...ChannelAd\n      __typename\n    }\n    categories {\n      ...ChannelCategory\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ChannelAd on ChannelAd {\n  adCampaignId\n  channelGroup {\n    id\n    name\n    info {\n      ...ChannelGroupInfo\n      __typename\n    }\n    channels {\n      id\n      onlineUserCount\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ChannelGroupInfo on ChannelGroupInfo {\n  previewImageUrl\n  backgroundColor {\n    ...Color\n    __typename\n  }\n  __typename\n}\n\nfragment Color on Color {\n  alpha\n  blue\n  green\n  red\n  __typename\n}\n\nfragment ChannelCategory on ChannelCategory {\n  id\n  name\n  channelGroups(first: $groupAmount) {\n    id\n    name\n    info {\n      ...ChannelGroupInfo\n      __typename\n    }\n    channels {\n      id\n      name\n      onlineUserCount\n      onlineContacts {\n        ...ChannelListContact\n        __typename\n      }\n      __typename\n    }\n    onlineContacts {\n      ...ChannelListContact\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ChannelListContact on User {\n  id\n  profilePicture {\n    urlCustomSizeSquare(pixelDensity: $pixelDensity, size: 40)\n    __typename\n  }\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return [from_dict(data_class = ChannelCategory, data = category) for category in req.json()['data']['channel']['categories']]
    
    def getContactFilterSettings(self) -> Tuple[ContactFilterSettings, ContactFilterSettingsConstraints]:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName":"GetContactFilterSettings","variables":{},"query":"query GetContactFilterSettings {\n  messenger {\n    contactFilterSettings {\n      settings {\n        ...ContactFilterSettingsFragment\n        __typename\n      }\n      constraints {\n        minAge\n        maxAge\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ContactFilterSettingsFragment on ContactFilterSettings {\n  allowedGender\n  minAge\n  maxAge\n  profilePhotoRequired\n  alwaysAllowStammis\n  enableMessageSmoothing\n  onlyVerifiedMembers\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return from_dict(data_class = ContactFilterSettings, data = req.json()['data']['messenger']['contactFilterSettings']['settings']), from_dict(data_class = ContactFilterSettingsConstraints, data = req.json()['data']['messenger']['contactFilterSettings']['constraints'])
    
    def getUserFriendState(self, userID: str) -> str:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName":"UserFriendState","variables":{"userId":userID},"query":"query UserFriendState($userId: ID!) {\n  user {\n    user(id: $userId) {\n      id\n      friendState\n      __typename\n    }\n    __typename\n  }\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return req.json()["data"]["user"]["user"]["friendState"]
    
    # TODO: need acoount with common friends
    def getCommonFriends(self, userID: str) -> dict:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName":"CommonFriends","variables":{"userId":userID,"pixelDensity":2},"query":"query CommonFriends($userId: ID!, $pixelDensity: Float!) {\n  contacts {\n    commonFriends(userId: $userId) {\n      ... on InternalError {\n        unused\n        __typename\n      }\n      ... on FriendsHiddenByPrivacy {\n        unused\n        __typename\n      }\n      ... on FriendList {\n        friends {\n          ...CommonFriend\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment CommonFriend on User {\n  id\n  nick\n  profilePicture {\n    urlCustomSizeSquare(pixelDensity: $pixelDensity, size: 40)\n    __typename\n  }\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return req.json()["data"]["contacts"]["commonFriends"]["friends"]
    
    def getProfilePictureCustomSize(self, userID: str, size: int = 40) -> ProfilePicture:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName":"GetProfilePictureCustomSize","variables":{"userId":userID,"size":size,"pixelDensity":2},"query":"query GetProfilePictureCustomSize($userId: ID!, $pixelDensity: Float!, $size: Int!) {\n  user {\n    user(id: $userId) {\n      id\n      profilePicture {\n        urlCustomSizeSquare(pixelDensity: $pixelDensity, size: $size)\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return from_dict(data_class = ProfilePicture, data = req.json()["data"]["user"]["user"]["profilePicture"])
    
    def getReactionSmileys(self) -> List[SmileyDetails]:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName":"ReactionSmileys","variables":{},"query":"query ReactionSmileys {\n  smileybox {\n    reactionSmileys {\n      id\n      image\n      textRepresentation\n      __typename\n    }\n    __typename\n  }\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return [from_dict(data_class = SmileyDetails, data = smiley) for smiley in req.json()["data"]["smileybox"]["reactionSmileys"]]
    
    def getAlbumInfoForProfile(self, userID: str) -> User:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName":"GetAlbumInfoForProfile","variables":{"userId":userID},"query":"query GetAlbumInfoForProfile($userId: ID!) {\n  user {\n    user(id: $userId) {\n      albumPhotos(limit: 12) {\n        id\n        thumbnailUrl\n        __typename\n      }\n      albums {\n        ...Album\n        __typename\n      }\n      albumProfilePhoto {\n        ...AlbumDetailPhoto\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment Album on Album {\n  id\n  title\n  isOwner\n  albumPhotos {\n    ...AlbumDetailPhoto\n    __typename\n  }\n  __typename\n}\n\nfragment AlbumDetailPhoto on AlbumPhoto {\n  id\n  thumbnailUrl\n  photoUrl\n  administrationUrl\n  description {\n    formattedText\n    rawText\n    __typename\n  }\n  isOwner\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return from_dict(data_class = User, data = req.json()["data"]["user"]["user"])
    
    def getUserKnuddel(self, userID: str) -> int:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName":"UserKnuddel","variables":{"id":userID},"query":"query UserKnuddel($id: ID!) {\n  user {\n    user(id: $id) {\n      ...UserKnuddel\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment UserKnuddel on User {\n  id\n  knuddelAmount\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return req.json()["data"]["user"]["user"]["knuddelAmount"]
    
    def getAlbumPhotoComments(self, albumPhotoID: str) -> List[AlbumPhotoComment]:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName":"AlbumPhotoComments","variables":{"albumPhotoId":albumPhotoID,"pixelDensity":2},"query":"query AlbumPhotoComments($albumPhotoId: ID!, $pixelDensity: Float!) {\n  user {\n    albumPhotoComments(albumPhotoId: $albumPhotoId) {\n      ...AlbumPhotoComment\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AlbumPhotoComment on AlbumPhotoComment {\n  id\n  text\n  timestamp\n  sender {\n    id\n    nick\n    profilePicture {\n      urlCustomSizeSquare(pixelDensity: $pixelDensity, size: 40)\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return [from_dict(data_class = AlbumPhotoComment, data = comment) for comment in req.json()["data"]["user"]["albumPhotoComments"]]
    
    def getUserMacroBox(self, userID: str) -> User:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName":"GetUserForMacroBox","variables":{"userId":userID,"pixelDensity":2},"query":"query GetUserForMacroBox($userId: ID!, $pixelDensity: Float!) {\n  user {\n    user(id: $userId) {\n      ...MacroBoxUser\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment MacroBoxUser on User {\n  id\n  nick\n  age\n  gender\n  profilePicture {\n    urlCustomSizeSquare(pixelDensity: $pixelDensity, size: 60)\n    __typename\n  }\n  city\n  ignoreState\n  isReportable\n  isAppBot\n  menteeStatus\n  authenticityClassification\n  canReceiveMessages\n  conversationId\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return from_dict(data_class = User, data = req.json()["data"]["user"]["user"])
    
    def getProfilePictureByUserId(self, userID: str, size: int = 60) -> ProfilePicture:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName":"GetProfilePictureByUserId","variables":{"size":size,"userId":userID,"pixelDensity":2},"query":"query GetProfilePictureByUserId($userId: ID!, $pixelDensity: Float!, $size: Int = 40) {\n  user {\n    user(id: $userId) {\n      id\n      profilePicture {\n        urlCustomSizeSquare(pixelDensity: $pixelDensity, size: $size)\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return from_dict(data_class = ProfilePicture, data = req.json()["data"]["user"]["user"]["profilePicture"])
    
    def getReasons(self) -> List[ComplaintReason]:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName":"GetReasons","variables":{"context":"Profile"},"query":"query GetReasons($context: ComplaintReasonContext!) {\n  complaints {\n    complaintReasons(context: $context) {\n      id\n      name\n      itemType\n      __typename\n    }\n    __typename\n  }\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return [from_dict(data_class = ComplaintReason, data = reason) for reason in req.json()["data"]["complaints"]["complaintReasons"]]
    
    def reportUser(self, userID: str, reasonID: str, text: str) -> None:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName":"CreateUserComplaint","variables":{"explanation":text,"reasonId":reasonID,"userId":userID},"query":"mutation CreateUserComplaint($userId: ID!, $explanation: String!, $reasonId: ID!) {\n  complaints {\n    reportUser(explanation: $explanation, reasonId: $reasonId, userId: $userId) {\n      error\n      __typename\n    }\n    __typename\n  }\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        
    def ignoreUser(self, userID: str) -> None:
        """
            Ignore a user, so you won't see his messages anymore for the next 6 hours.
        """
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName":"IgnoreUser","variables":{"userId":userID},"query":"mutation IgnoreUser($userId: ID!) {\n  user {\n    ignore(userId: $userId) {\n      error\n      __typename\n    }\n    __typename\n  }\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        
    def unIgnoreUser(self, userID: str) -> None:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName":"UnIgnore","variables":{"id":userID},"query":"mutation UnIgnore($id: ID!) {\n  user {\n    unignore(userId: $id) {\n      error\n      __typename\n    }\n    __typename\n  }\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        
    def privateIgnoreUser(self, userID: str) -> None:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName":"PrivateIgnore","variables":{"id":userID},"query":"mutation PrivateIgnore($id: ID!) {\n  user {\n    privateIgnore(userId: $id) {\n      error\n      __typename\n    }\n    __typename\n  }\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        
    def blockUser(self, userID: str) -> None:
        """
            Block a user, so you won't see his messages anymore.
        """
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName":"BlockUser","variables":{"userId":userID},"query":"mutation BlockUser($userId: ID!) {\n  user {\n    block(userId: $userId) {\n      error\n      __typename\n    }\n    __typename\n  }\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        
    def unBlockUser(self, userID: str) -> None:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName":"UnBlock","variables":{"id":userID},"query":"mutation UnBlock($id: ID!) {\n  user {\n    unblock(userId: $id) {\n      error\n      __typename\n    }\n    __typename\n  }\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        
    def archiveConversation(self, conversationID: str) -> None:
        """
            Removes a conversation from your inbox.
        """
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName":"ArchiveConversation","variables":{"id":conversationID},"query":"mutation ArchiveConversation($id: ID!) {\n  messenger {\n    archiveConversation(id: $id) {\n      error\n      conversation {\n        id\n        isArchived\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        
    def unArchiveConversation(self, conversationID: str) -> None:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName":"UnArchiveConversation","variables":{"id":conversationID},"query":"mutation UnArchiveConversation($id: ID!) {\n  messenger {\n    unarchiveConversation(id: $id) {\n      error\n      conversation {\n        id\n        isArchived\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        
    def allowImages(self, userID: str) -> None:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName":"AllowImages","variables":{"userId":userID},"query":"mutation AllowImages($userId: ID!) {\n  user {\n    allowImages(userId: $userId) {\n      error\n      __typename\n    }\n    __typename\n  }\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        
    def canSendImages(self, userID: str) -> bool:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName":"CanSendImages","variables":{"userId":userID},"query":"query CanSendImages($userId: ID!) {\n  user {\n    user(id: $userId) {\n      id\n      canSendImages\n      __typename\n    }\n    __typename\n  }\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return req.json()["data"]["user"]["user"]["canSendImages"]
    
    def sendMessageInChannel(self, channelID: str, text: str) -> None:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName":"SendMessage","variables":{"channelId":channelID,"text":text},"query":"mutation SendMessage($channelId: ID!, $text: String!) {\n  channel {\n    sendMessage(id: $channelId, text: $text) {\n      error\n      __typename\n    }\n    __typename\n  }\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()