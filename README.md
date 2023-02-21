# Knuddels API
A wrapper for the unofficial API of the chat website knuddels.de

### Usage
- Clone the repo
- create a file with the following content
```python
from knuddelsAPI2 import KnuddelsAPI

api = KnuddelsAPI("my username", "my password")
print(api.getCurrentUserNick())
```
There are a lot more functions, I'll write a documentation soonish (help is really appreciated).

You may see two files `knuddelsAPI.py` and `function.py` in this repo, these are just old relics from before the refactoring. I'll delete them after I migrated everything. `backup-chats.py` is a script that saves all chat partners and chats on your computer but it currently uses the old `knuddelsAPI.py`. I'll migrate that in the near future.
