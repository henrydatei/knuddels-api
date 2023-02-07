import dataclasses
import json
import requests
from dacite import from_dict
from typing import List

from classes.ClientSettings import ClientSettings
from classes.User import User
from classes.FotomeetMatch import FotomeetMatch
from classes.FotomeetStatus import FotomeetStatus
from classes.ProfileVisitors import ProfileVisitors
from classes.SmileyDetails import SmileyDetails
from classes.Channel import Channel

@dataclasses.dataclass
class KnuddelAPI:
    username: str
    password: str
    sessionToken: str = dataclasses.field(init = False)

    def __post_init__(self) -> None:
        self.sessionToken = self.login(self.username, self.password)

    def getDeviceToken(self, username, password) -> str:
        params = {"operationName": "CreateDeviceToken", "variables": {"username": username,"password": password}, "query": 'query CreateDeviceToken($username: String!, $password: String!) {\n  login {\n    createDeviceToken(username: $username, password: $password) {\n      result\n      token\n      __typename\n    }\n    __typename\n  }\n}\n'}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params))
        req.raise_for_status()
        return req.json()
    
    def getRefreshSessionToken(self, deviceToken) -> str:
        headers={"authorization": "Bearer "+deviceToken}
        params = {"operationName":"RefreshSessionToken","variables":{"sessionInfo":{"type":"K3GraphQl","clientVersion":{"major":4,"minor":22,"patch":8,"buildInfo":"dd34485a181477347adee04f166323c39d6db397"},"platform":"Native","osInfo":{"type":"Ios","version":"14.6"},"deviceIdentifiers":["E696701F-2098-4266-A040-B84FD740A6CF"]}},"query":"query RefreshSessionToken($sessionInfo: SessionInfo!, $oldSessionToken: SessionToken) {\n  login {\n    refreshSession(sessionInfo: $sessionInfo, token: $oldSessionToken) {\n      ... on RefreshSessionSuccess {\n        expiry\n        token\n        __typename\n      }\n      ...RefreshSessionError\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment RefreshSessionError on RefreshSessionError {\n  errorMessage\n  user {\n    ...UserWithLockInfo\n    __typename\n  }\n  __typename\n}\n\nfragment UserWithLockInfo on User {\n  id\n  nick\n  lockInfo {\n    ... on UnlockedLockInfo {\n      __typename\n    }\n    ... on TemporaryLockInfo {\n      lockReason\n      lockedBy {\n        id\n        nick\n        __typename\n      }\n      lockedUntilDate\n      __typename\n    }\n    ... on PermanentLockInfo {\n      lockReason\n      lockedBy {\n        id\n        nick\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return req.json()

    def login(self, username, password) -> str:
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
    
    def getChannel(self, channelID) -> Channel:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName": "GetChannel", "variables": {"channelId": channelID}, "query": "query GetChannel($channelId: ID!) {\n  channel {\n    channel(id: $channelId) {\n      ...ActiveChannel\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ActiveChannel on Channel {\n  id\n  name\n  users {\n    ...ChannelUser\n    __typename\n  }\n  groupInfo {\n    backgroundColor {\n      ...Color\n      __typename\n    }\n    backgroundImageInfo {\n      mode\n      url\n      __typename\n    }\n    highlightColor {\n      ...Color\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ChannelUser on User {\n  id\n  nick\n  age\n  gender\n  profilePicture {\n    urlLargeSquare\n    __typename\n  }\n  __typename\n}\n\nfragment Color on Color {\n  alpha\n  blue\n  green\n  red\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return from_dict(data_class = Channel, data = req.json()['data']['channel']['channel'])
    
    def joinChannelById(self, channelID) -> Channel:
        headers={"authorization": "Bearer "+self.sessionToken}
        params = {"operationName": "JoinChannelById", "variables": {"channelId": channelID}, "query": "mutation JoinChannelById($channelId: ID!) {\n  channel {\n    joinById(id: $channelId) {\n      channel {\n        ...ActiveChannel\n        __typename\n      }\n      error {\n        ...ChannelJoinError\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ActiveChannel on Channel {\n  id\n  name\n  users {\n    ...ChannelUser\n    __typename\n  }\n  groupInfo {\n    backgroundColor {\n      ...Color\n      __typename\n    }\n    backgroundImageInfo {\n      mode\n      url\n      __typename\n    }\n    highlightColor {\n      ...Color\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ChannelUser on User {\n  id\n  nick\n  age\n  gender\n  profilePicture {\n    urlLargeSquare\n    __typename\n  }\n  __typename\n}\n\nfragment Color on Color {\n  alpha\n  blue\n  green\n  red\n  __typename\n}\n\nfragment ChannelJoinError on ChannelJoinMutationResponseError {\n  type\n  freetext\n  userNick\n  otherChannelName\n  minAge\n  maxUser\n  startTime\n  endTime\n  minKnuddels\n  minTradeableSmileys\n  minRegisteredDays\n  minStammiMonths\n  requiredGender\n  requiredStatusName\n  __typename\n}\n"}
        req = requests.post('https://api-de.knuddels.de/api-gateway/graphql', data=json.dumps(params), headers=headers)
        req.raise_for_status()
        return from_dict(data_class = Channel, data = req.json()['data']['channel']['joinById']['channel'])