# Knuddels API
A wrapper for the unofficial API of the chat website knuddels.de

### Usage
- Clone the repo
- Create a file with the following content
```python
from knuddelsAPI import KnuddelsAPI

api = KnuddelsAPI("my username", "my password")
print(api.getCurrentUserNick())
```
There are a lot more functions, I'll write a documentation soonish (help is really appreciated), but most function names are pretty self-explanatory. Just have a look at the source code.

### Example
Create an `.env` file with the following content:
```
KNUDDELS_USERNAME="username"
KNUDDELS_PASSWORD="password"
```
and run `count_messages.py`. It will count with how many people you exchanged how many messages.