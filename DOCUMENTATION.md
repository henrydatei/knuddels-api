# Knuddels API — Documentation

A detailed reference for the unofficial Knuddels GraphQL API wrapper.

> **Note:** This is a reverse-engineered wrapper around Knuddels' private GraphQL API at `https://api-de.knuddels.de/mono/graphql`. The API is undocumented and may change without notice.

---

## Table of Contents

1. [Installation](#installation)
2. [Authentication & Session](#authentication--session)
3. [API Reference](#api-reference)
   - [Session / Settings](#session--settings)
   - [User & Profile](#user--profile)
   - [Messenger (Private Messages)](#messenger-private-messages)
   - [Channels](#channels)
   - [Fotomeet](#fotomeet)
   - [Contacts & Social](#contacts--social)
   - [Album & Photos](#album--photos)
   - [Moderation](#moderation)
   - [Smileys](#smileys)
4. [Data Classes](#data-classes)
5. [Known Quirks & Gotchas](#known-quirks--gotchas)

---

## Installation

```bash
pip install requests dacite python-dotenv
git clone https://github.com/henrydatei/knuddels-api.git
cd knuddels-api
```

Basic usage:

```python
from knuddelsAPI import KnuddelsAPI

api = KnuddelsAPI(username="YourNick", password="YourPassword")
user = api.getCurrentUserNick()
print(user.nick)
```

---

## Authentication & Session

Login is a **three-step process** handled automatically by the constructor:

1. **`logincheck`** — Posts credentials to `https://www.knuddels.de/logincheck.html`, returns a short-lived JWT.
2. **`createSessionToken`** — Exchanges the JWT for a session token via GraphQL (`CreateSessionToken`). Sends client/device metadata that mimics an iOS app.
3. **`activateSessionToken`** — Activates the session token via GraphQL (`ActivateSession`).

The resulting `sessionToken` is stored in `self.sessionToken` and attached as `Authorization: Bearer <token>` to every subsequent request.

```python
# All three steps happen automatically:
api = KnuddelsAPI(username="Nick", password="Pass")
# api.sessionToken is now ready to use
```

### Internal Methods

| Method | Description |
|--------|-------------|
| `logincheck(username, password) → str` | Returns a short-lived JWT from the login endpoint |
| `createSessionToken(logincheckToken) → str` | Exchanges JWT for a session token |
| `activateSessionToken(sessionToken) → None` | Activates the session; must be called before using the token |
| `login(username, password) → str` | Runs all three steps; called by `__post_init__` |

---

## API Reference

### Session / Settings

#### `getClientSettings() → ClientSettings`
Returns the current user's app settings.

```python
settings = api.getClientSettings()
print(settings.initialJoinBehavior)  # e.g. "JoinLastChannel"
```

**Returns:** [`ClientSettings`](#clientsettings)

---

#### `getCurrentServerTime() → str`
Returns the server's current UTC timestamp as a string.

```python
t = api.getCurrentServerTime()
print(t)  # e.g. "2024-01-15T12:34:56Z"
```

---

#### `getCurrentUserNick() → User`
Returns basic info about the logged-in user (id, nick, gender).

```python
me = api.getCurrentUserNick()
print(me.nick, me.gender)
```

**Returns:** [`User`](#user) (partial — only `id`, `nick`, `gender` are populated)

---

#### `updateLastSeen() → bool`
Updates the "last seen" timestamp, marking the user as present. Call this periodically to stay shown as online.

```python
api.updateLastSeen()
```

---

### User & Profile

#### `getUserProfile(userID) → Tuple[User, Conversation]`
Fetches full profile data for a user and opens/returns the conversation with them.

```python
user, conv = api.getUserProfile("12345678")
print(user.nick, user.age, user.city)
print(conv.id)  # use this for sendMessage()
```

**Parameters:**
- `userID` (str): The user's numeric ID

**Returns:** Tuple of [`User`](#user) (full profile fields) and [`Conversation`](#conversation)

---

#### `isUserOnline(userID) → bool`
Checks whether a user is currently online.

```python
if api.isUserOnline("12345678"):
    print("User is online")
```

---

#### `isUserOnlineAndLastChannel(userID) → Tuple[bool, str]`
Returns both online status and the name of the channel the user was last seen in.

```python
online, channel = api.isUserOnlineAndLastChannel("12345678")
print(f"Online: {online}, Last channel: {channel}")
```

---

#### `notifyProfileVisited(userID) → None`
Sends a profile-visit notification to the user (they will see you in their visitors list).

```python
api.notifyProfileVisited("12345678")
```

---

#### `getProfilePictureUrls(userID) → ProfilePicture`
Returns large and very-large profile picture URLs for a user.

```python
pic = api.getProfilePictureUrls("12345678")
print(pic.urlLargeSquare)
print(pic.urlVeryLarge)
print(pic.exists)  # False if user has no profile picture
```

**Returns:** [`ProfilePicture`](#profilepicture)

---

#### `getProfilePictureCustomSize(userID, size=40) → ProfilePicture`
Returns a profile picture URL at a custom square size (pixels).

```python
pic = api.getProfilePictureCustomSize("12345678", size=120)
print(pic.urlCustomSizeSquare)
```

**Parameters:**
- `userID` (str)
- `size` (int, default 40): Square size in CSS pixels; actual resolution is `size × pixelDensity` (2×)

---

#### `getProfilePictureByUserId(userID, size=60) → ProfilePicture`
Similar to `getProfilePictureCustomSize` but uses a separate operation name.

---

#### `getUserKnuddel(userID) → int`
Returns the current Knuddel balance of a user.

```python
knuddels = api.getUserKnuddel("12345678")
print(f"Has {knuddels} Knuddels")
```

---

#### `getUserMacroBox(userID) → User`
Fetches the data shown in the "macro box" (mini-popup) for a user — nick, age, gender, city, ignore state, etc.

**Returns:** [`User`](#user) (partial)

---

#### `getUserFriendState(userID) → str`
Returns the friendship status with a user.

```python
state = api.getUserFriendState("12345678")
# Possible values: "NO_FRIEND", "FRIEND", "FRIEND_REQUEST_SENT", "FRIEND_REQUEST_RECEIVED"
print(state)
```

---

#### `getCommonFriends(userID) → dict`
Returns a list of friends you have in common with a user.

> ⚠️ Requires at least one common friend to return meaningful data. Returns a raw dict.

---

#### `profileVisitors() → ProfileVisitors`
Returns a list of users who recently visited your profile.

```python
visitors = api.profileVisitors()
print(visitors.visibilityStatus)  # "VISIBLE" or "HIDDEN"
for v in visitors.visitors:
    print(v.nick)
```

**Returns:** [`ProfileVisitors`](#profilevisitors)

---

#### `isUserAdFree() → bool`
Checks if the logged-in user has an active ad-free subscription.

---

### Messenger (Private Messages)

#### `getConversations(beforeTimestamp=None) → List[Conversation]`
Returns all conversations, paginated automatically. Pass `None` to start from the most recent.

```python
conversations = api.getConversations(beforeTimestamp=None)
for conv in conversations:
    print(conv.id, conv.otherParticipants[0].nick)
```

**Parameters:**
- `beforeTimestamp` (Optional[str]): UTC timestamp for pagination cursor; pass the timestamp of the oldest conversation from the previous page

**Returns:** List of [`Conversation`](#conversation) — automatically fetches all pages via recursion

---

#### `getConversation(conversationID) → Conversation`
Fetches metadata for a single conversation (participants, read state, latest message) without fetching all messages.

```python
conv = api.getConversation("conv_abc123")
print(conv.readState.unreadMessageCount)
```

**Returns:** [`Conversation`](#conversation)

---

#### `getMessagesForConversation(conversationID, beforeMessageID=None, messageCount=50, recursionDepth=0) → List[Message]`
Fetches all messages in a conversation, paginated automatically (max recursion depth: 10).

```python
messages = api.getMessagesForConversation("conv_abc123", beforeMessageID=None)
for msg in messages:
    if hasattr(msg.content, "formattedText"):
        print(f"{msg.sender.nick}: {msg.content.formattedText}")
```

**Parameters:**
- `conversationID` (str)
- `beforeMessageID` (Optional[str]): Message ID for pagination
- `messageCount` (int, default 50): Messages per page
- `recursionDepth` (int): Internal counter; do not set manually

**Returns:** List of [`Message`](#message)

> ⚠️ `msg.content` is a polymorphic type — check `__typename` or use `isinstance()` to determine the actual content type. See [MessageContent types](#messagecontent-types).

---

#### `sendMessage(conversationID, message) → None`
Sends a text message in a private conversation.

```python
api.sendMessage("conv_abc123", "Hello!")
```

> ⚠️ A successful HTTP response (no exception) does **not** guarantee the message was delivered. Knuddels may silently filter messages for spam, contact-filter, or ignore reasons. Check `recentMessages` after sending if delivery confirmation matters.

---

#### `sendTyping(conversationID) → None`
Sends a "typing..." indicator to the other participant.

```python
api.sendTyping("conv_abc123")
```

---

#### `markConversationAsRead(conversationID) → None`
Marks all messages in a conversation as read.

---

#### `markConversationAsUnread(conversationID) → None`
Marks a conversation as unread (the blue dot re-appears).

---

#### `archiveConversation(conversationID) → None`
Archives a conversation (removes it from the main inbox).

> ⚠️ If you call `sendMessage` and immediately `archiveConversation`, there is a race condition: the send commit may reset `visibility` back to `VISIBLE`. Add a short delay (~1s) between the two calls if needed.

---

#### `unArchiveConversation(conversationID) → None`
Moves a conversation back to the main inbox.

---

#### `getContactFilterSettings() → Tuple[ContactFilterSettings, ContactFilterSettingsConstraints]`
Returns the current message filter settings (allowed genders, age range, photo requirement, etc.) and the constraints (min/max allowed age values).

```python
settings, constraints = api.getContactFilterSettings()
print(settings.allowedGender)   # e.g. "ALL", "MALE", "FEMALE"
print(settings.minAge, settings.maxAge)
print(constraints.minAge, constraints.maxAge)
```

**Returns:** Tuple of [`ContactFilterSettings`](#contactfiltersettings), [`ContactFilterSettingsConstraints`](#contactfiltersettingsconstraints)

---

#### `allowImages(userID) → None`
Grants a specific user permission to send you images.

---

#### `canSendImages(userID) → bool`
Checks whether a user is currently allowed to send you images.

---

### Channels

#### `initialChannelJoin() → List[Channel]`
Performs the initial channel join when opening the app — joins the channel(s) configured in the user's settings and returns them.

```python
channels = api.initialChannelJoin()
for ch in channels:
    print(ch.id, ch.name, len(ch.users), "users")
```

**Returns:** List of [`Channel`](#channel)

---

#### `getChannel(channelID) → Channel`
Fetches current state of a channel (users, group info).

```python
ch = api.getChannel("channel_id_here")
print(ch.name, ch.onlineUserCount)
```

**Returns:** [`Channel`](#channel)

---

#### `joinChannelById(channelID) → Channel`
Joins a channel by its ID.

```python
ch = api.joinChannelById("channel_id_here")
```

**Returns:** [`Channel`](#channel)

> ℹ️ If joining fails (age restriction, Knuddel requirement, etc.), the underlying GraphQL response contains a `ChannelJoinError` with these fields: `type`, `freetext`, `minAge`, `maxUser`, `minKnuddels`, `minTradeableSmileys`, `minRegisteredDays`, `minStammiMonths`, `requiredGender`, `requiredStatusName`.

---

#### `sendMessageInChannel(channelID, text) → None`
Sends a public chat message in a channel.

```python
api.sendMessageInChannel("channel_id_here", "Hello everyone!")
```

---

#### `getChannelListOverview() → List[ChannelCategory]`
Returns the full channel browser — categories, channel groups, and individual channels with online user counts.

```python
categories = api.getChannelListOverview()
for cat in categories:
    print(cat.name)
    for group in cat.channelGroups:
        print(f"  {group.name}")
        for ch in group.channels:
            print(f"    {ch.name}: {ch.onlineUserCount} online")
```

**Returns:** List of [`ChannelCategory`](#channelcategory)

---

### Fotomeet

Knuddels' Tinder-like photo rating feature.

#### `getFotoMeetStatus() → FotomeetStatus`
Returns the current Fotomeet session — the next candidate to vote on, prefetch image URLs, and overall status.

```python
status = api.getFotoMeetStatus()
if status.currentCandidate:
    print(status.currentCandidate.userInfo.nick)
    print(status.currentCandidate.imageUrl)
```

**Returns:** [`FotomeetStatus`](#fotomeetstatus)

---

#### `fotoMeetVote(userID, vote) → FotomeetVoteResponse`
Votes on a Fotomeet candidate.

```python
response = api.fotoMeetVote("fotomeet_user_id", "YES")
# or
response = api.fotoMeetVote("fotomeet_user_id", "NO")
print(response.error)       # None if successful
```

**Parameters:**
- `userID` (str): The Fotomeet user ID (from `FotomeetStatus.currentCandidate.id` — **not** the regular user ID)
- `vote` (Literal["YES", "NO"])

**Returns:** [`FotomeetVoteResponse`](#fotomeetvoteresponse)

---

#### `getFotomeetMatches() → List[FotomeetMatch]`
Returns your current Fotomeet matches (mutual YES votes).

```python
matches = api.getFotomeetMatches()
for m in matches:
    print(m.user.nick, m.matchedAt, "new:", m.isNew)
```

**Returns:** List of [`FotomeetMatch`](#fotomeetmatch)

---

### Contacts & Social

#### `getContacts(type) → List[User]`
Returns a contact list of the given type.

```python
watchlist = api.getContacts("Watchlist")
fotomeet  = api.getContacts("Fotomeet")
mentees   = api.getContacts("Mentee")
latest    = api.getContacts("Latest")
```

**Parameters:**
- `type` (Literal["Watchlist", "Fotomeet", "Mentee", "Latest"])

**Returns:** List of [`User`](#user) (partial — nick, profile picture, online status, readMe, canReceiveMessages)

---

#### `ignoreUser(userID) → None`
Ignores a user for 6 hours (their messages won't be shown to you).

---

#### `unIgnoreUser(userID) → None`
Removes the temporary ignore on a user.

---

#### `privateIgnoreUser(userID) → None`
Permanently and privately ignores a user (they are not notified).

---

#### `blockUser(userID) → None`
Permanently blocks a user (they can no longer message you).

---

#### `unBlockUser(userID) → None`
Removes a block.

---

### Album & Photos

#### `getAlbumInfoForProfile(userID) → User`
Returns a user object with their album photos and albums populated.

```python
user = api.getAlbumInfoForProfile("12345678")
for photo in user.albumPhotos:
    print(photo.thumbnailUrl)
for album in user.albums:
    print(album.title, len(album.albumPhotos), "photos")
```

**Returns:** [`User`](#user) with `albumPhotos`, `albums`, and `albumProfilePhoto` fields

---

#### `getAlbumPhotoComments(albumPhotoID) → List[AlbumPhotoComment]`
Returns all comments on a specific album photo.

```python
comments = api.getAlbumPhotoComments("photo_id_here")
for c in comments:
    print(f"{c.sender.nick}: {c.text}")
```

**Returns:** List of [`AlbumPhotoComment`](#albumphotocomment)

---

### Moderation

#### `getReasons() → List[ComplaintReason]`
Returns the available complaint/report reasons for the "Profile" context.

```python
reasons = api.getReasons()
for r in reasons:
    print(r.id, r.name, r.itemType)
```

**Returns:** List of [`ComplaintReason`](#complaintreason)

---

#### `reportUser(userID, reasonID, text) → None`
Files a complaint against a user.

```python
reasons = api.getReasons()
spam_reason = next(r for r in reasons if "spam" in r.name.lower())
api.reportUser("12345678", spam_reason.id, "Sent me spam messages")
```

---

### Smileys

#### `allSmileyIds() → List[SmileyDetails]`
Returns all smiley IDs usable by the current user.

```python
smileys = api.allSmileyIds()
print(f"{len(smileys)} smileys available")
```

**Returns:** List of [`SmileyDetails`](#smileydetails) — only `id` is populated

---

#### `getReactionSmileys() → List[SmileyDetails]`
Returns smileys available for message reactions, including their image URL and text representation.

```python
reactions = api.getReactionSmileys()
for s in reactions:
    print(s.id, s.textRepresentation, s.image)
```

**Returns:** List of [`SmileyDetails`](#smileydetails) — `id`, `image`, and `textRepresentation` are populated

---

## Data Classes

All data classes are plain Python `@dataclass` objects defined in the `classes/` folder.

### `User`
The central user object. Not all fields are populated in every context — depends on which method returned it.

| Field | Type | Notes |
|-------|------|-------|
| `id` | `str` | Numeric user ID |
| `nick` | `str` | Display name |
| `gender` | `str` | `"MALE"`, `"FEMALE"`, `"UNKNOWN"` |
| `age` | `int` | Age in years |
| `city` | `str` | |
| `profilePicture` | `ProfilePicture` | |
| `isOnline` | `bool` | |
| `canReceiveMessages` | `bool` | False if contact filter blocks you |
| `canSendImages` | `bool` | |
| `readMe` | `Optional[str]` | User's "about me" text |
| `conversationId` | `str` | Direct conversation ID with this user |
| `dateOfBirth` | `Optional[str]` | ISO date string |
| `dateOfRegistration` | `Optional[str]` | ISO date string |
| `lastOnlineTime` | `Optional[str]` | ISO timestamp |
| `country` | `str` | |
| `sexualOrientation` | `str` | |
| `relationshipStatus` | `str` | |
| `stammiMonths` | `int` | Months as paying member |
| `onlineMinutes` | `int` | Total online time in minutes |
| `latestOnlineChannelName` | `Optional[str]` | |
| `myChannelName` | `str` | User's own channel name |
| `moderatedChannelName` | `str` | Channel they moderate |
| `hickeys` | `int` | |
| `flowers` | `int` | |
| `roses` | `int` | |
| `chatMeetups` | `int` | |
| `givenHeart` | `str` | Nick of user they gave a heart to |
| `receivedHearts` | `int` | |
| `mentorPoints` | `int` | |
| `ignoreState` | `str` | `"NOT_IGNORING"`, `"IGNORING"`, `"IGNORED_BY"` |
| `isIgnoring` | `bool` | |
| `isReportable` | `bool` | |
| `isAppBot` | `bool` | |
| `menteeStatus` | `str` | |
| `authenticityClassification` | `str` | e.g. `"HUMAN"`, `"BOT_LIKE"` |
| `status` | `Optional[str]` | Knuddels status level |
| `albumPhotos` | `List[AlbumPhoto]` | Only set by `getAlbumInfoForProfile` |
| `albums` | `List[Album]` | Only set by `getAlbumInfoForProfile` |
| `albumProfilePhoto` | `AlbumPhoto` | Only set by `getAlbumInfoForProfile` |

---

### `Conversation`

| Field | Type | Notes |
|-------|------|-------|
| `id` | `str` | Use this for all messenger operations |
| `isArchived` | `bool` | |
| `visibility` | `str` | `"VISIBLE"`, `"ARCHIVED"`, `"HIDDEN"` |
| `otherParticipants` | `List[User]` | Usually one user |
| `readState` | `ReadState` | |
| `latestConversationMessage` | `Message` | |

---

### `Message`

| Field | Type | Notes |
|-------|------|-------|
| `id` | `str` | |
| `timestamp` | `str` | ISO timestamp |
| `sender` | `User` | Partial user object (id, nick, isOnline, canSendImages) |
| `content` | `MessageContent` | Polymorphic — see below |

---

### MessageContent Types

`Message.content` is one of the following types, distinguished by `__typename`:

| `__typename` | Class | Key Fields |
|---|---|---|
| `ConversationTextMessageContent` | `ConversationTextMessageContent` | `formattedText: str`, `starred: bool` |
| `ConversationImageMessageContent` | `ConversationImageMessageContent` | `image: UserSentImage`, `imageAccepted: bool`, `sensitiveContentClassification: str`, `starred: bool` |
| `ConversationSnapMessageContent` | `ConversationSnapMessageContent` | `snap: UserSentSnap`, `imageAccepted: bool` |
| `ConversationQuotedMessageContent` | `ConversationQuotedMessageContent` | `formattedText: str`, `nestedMessage`, `starred: bool` |
| `ConversationKnuddelTransferMessageContent` | `ConversationKnuddelTransferMessageContent` | `knuddelAmount: int` |
| `ConversationVisiblePhotoCommentMessageContent` | `ConversationVisiblePhotoCommentMessageContent` | `albumPhotoId: str`, `commentId: str`, `photoUrl: str`, `formattedText: str` |
| `ConversationHiddenPhotoCommentMessageContent` | `ConversationHiddenPhotoCommentMessageContent` | `albumPhotoId: str`, `photoUrl: str`, `formattedText: str` |

Example for safe content access:
```python
from classes.MessageContent import ConversationTextMessageContent, ConversationImageMessageContent

for msg in messages:
    if isinstance(msg.content, ConversationTextMessageContent):
        print(msg.content.formattedText)
    elif isinstance(msg.content, ConversationImageMessageContent):
        print("Image:", msg.content.image.url)
```

---

### `Channel`

| Field | Type |
|-------|------|
| `id` | `str` |
| `name` | `str` |
| `users` | `List[User]` |
| `groupInfo` | `ChannelGroupInfo` |
| `onlineUserCount` | `int` |

---

### `ChannelCategory`

| Field | Type |
|-------|------|
| `id` | `str` |
| `name` | `str` |
| `channelGroups` | `List[ChannelGroup]` |

---

### `ChannelGroup`

| Field | Type |
|-------|------|
| `id` | `str` |
| `name` | `str` |
| `info` | `ChannelGroupInfo` |
| `channels` | `List[Channel]` |
| `onlineContacts` | `List[User]` |

---

### `ChannelGroupInfo`

| Field | Type |
|-------|------|
| `backgroundColor` | `Color` |
| `backgroundImageInfo` | `Optional[ChannelBackgroundImageInfo]` |
| `highlightColor` | `Color` |

---

### `Color`

RGBA color value.

| Field | Type | Range |
|-------|------|-------|
| `red` | `int` | 0–255 |
| `green` | `int` | 0–255 |
| `blue` | `int` | 0–255 |
| `alpha` | `int` | 0–255 |

---

### `ProfilePicture`

| Field | Type | Notes |
|-------|------|-------|
| `urlLargeSquare` | `str` | Fixed large square thumbnail |
| `urlVeryLarge` | `str` | Full-size image |
| `urlCustomSizeSquare` | `str` | Only set by custom-size methods |
| `exists` | `bool` | `False` if user has no profile picture |

---

### `ReadState`

| Field | Type |
|-------|------|
| `markedAsUnread` | `bool` |
| `unreadMessageCount` | `int` |
| `lastReadMessage` | `Optional[Message]` |

---

### `FotomeetStatus`

| Field | Type | Notes |
|-------|------|-------|
| `currentCandidate` | `FotomeetUser` | Next user to vote on |
| `prefetchImageUrls` | `List[str]` | URLs to preload |
| `isPremium` | `bool` | |
| `potentialMatchCount` | `int` | Remaining candidates |

---

### `FotomeetUser`

| Field | Type | Notes |
|-------|------|-------|
| `id` | `str` | Fotomeet-specific ID — use this for `fotoMeetVote()` |
| `age` | `int` | |
| `gender` | `str` | |
| `isPotentialMatch` | `bool` | |
| `userInfo` | `Optional[UserInfo]` | Contains `id` and `nick` |
| `imageUrl` | `str` | |
| `isReportable` | `bool` | |
| `hasAlbumPhotos` | `bool` | |

---

### `FotomeetMatch`

| Field | Type |
|-------|------|
| `user` | `User` |
| `matchedAt` | `str` |
| `isNew` | `bool` |

---

### `FotomeetVoteResponse`

| Field | Type |
|-------|------|
| `error` | `Optional[str]` |
| `newStatus` | `FotomeetStatus` |

---

### `ProfileVisitors`

| Field | Type | Notes |
|-------|------|-------|
| `visibilityStatus` | `str` | `"VISIBLE"` or `"HIDDEN"` (hidden if not premium) |
| `visitors` | `List[User]` | |

---

### `ClientSettings`

| Field | Type | Notes |
|-------|------|-------|
| `conversationListFilterType` | `str` | e.g. `"ALL"` |
| `initialJoinBehavior` | `str` | e.g. `"JoinLastChannel"` |
| `contactListTabs` | `ContactListTabs` | |

---

### `ContactFilterSettings`

| Field | Type |
|-------|------|
| `allowedGender` | `str` |
| `minAge` | `int` |
| `maxAge` | `int` |
| `profilePhotoRequired` | `bool` |
| `alwaysAllowStammis` | `bool` |
| `enableMessageSmoothing` | `bool` |
| `onlyVerifiedMembers` | `bool` |

---

### `ContactFilterSettingsConstraints`

| Field | Type |
|-------|------|
| `minAge` | `int` |
| `maxAge` | `int` |

---

### `AlbumPhotoComment`

| Field | Type |
|-------|------|
| `id` | `str` |
| `text` | `str` |
| `timestamp` | `str` |
| `sender` | `User` |

---

### `ComplaintReason`

| Field | Type |
|-------|------|
| `id` | `str` |
| `name` | `str` |
| `itemType` | `str` |

---

### `SmileyDetails`

| Field | Type | Notes |
|-------|------|-------|
| `id` | `str` | Smiley ID |
| `image` | `str` | URL — only set by `getReactionSmileys()` |
| `textRepresentation` | `str` | e.g. `:)` — only set by `getReactionSmileys()` |

---

### `UserSentImage`

| Field | Type |
|-------|------|
| `url` | `str` |

---

### `UserSentSnap`

| Field | Type | Notes |
|-------|------|-------|
| `url` | `str` | Encrypted image URL |
| `photoId` | `str` | |
| `duration` | `int` | View duration in seconds |
| `decryptionKey` | `str` | AES key for decrypting the image |

---

## Known Quirks & Gotchas

### 1. `formattedText` is a JSON-encoded object

Knuddels sometimes returns `formattedText` as a JSON string like `'{"text":{"text":"Hello"}}'` instead of a plain string. The wrapper handles this automatically via `_extract_plain_text()`. If you bypass the wrapper and query the API directly, you'll need to handle this yourself:

```python
import json

def extract_text(value):
    if isinstance(value, str) and value.startswith("{"):
        try:
            parsed = json.loads(value)
            inner = parsed.get("text")
            if isinstance(inner, dict):
                return inner.get("text", "")
            return inner or ""
        except Exception:
            pass
    return value
```

---

### 2. GraphQL `error: null` ≠ mutation succeeded

The API returns HTTP 200 with `"error": null` even when a mutation had no effect. Known cases:
- **`sendMessage`**: Message silently dropped by spam filter or contact filter
- **`archiveConversation`**: Race condition with an incoming `sendMessage` can reset `visibility` back to `VISIBLE`

Always verify state-changing operations with a subsequent read query if correctness matters.

---

### 3. Session tokens expire

Session tokens are not permanent. Long-running bots should handle re-authentication. There is no explicit `logout()` method — simply create a new `KnuddelsAPI` instance.

---

### 4. Fotomeet IDs vs. User IDs

`FotomeetUser.id` (used for `fotoMeetVote()`) is **not** the same as the regular `User.id`. Use `FotomeetUser.userInfo.id` to get the regular user ID if you need to look up the user's profile.

---

### 5. `getChannelListOverview` returns only 5 groups per category

The query uses `groupAmount: 5` — each category shows at most 5 channel groups. There is no pagination for channel categories in the current implementation.

---

### 6. Channel Groups and their sub-channels

Some channel groups (e.g. "Flirt") appear under different category names depending on the user's age/region. The `name` field of the group is the canonical identifier; the category it appears under may vary.

---

### 7. `getConversations` pagination

Pagination is done by `beforeTimestamp`, not by offset. The recursion goes backward in time starting from the latest conversation. With very large inboxes, the max recursion depth (10 pages × 50 conversations = 500) may be hit.
