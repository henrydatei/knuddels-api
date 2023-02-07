import dataclasses
from typing import List

from .ContactListTabs import ContactListTabs

@dataclasses.dataclass
class ClientSettings:
    conversationListFilterType: str
    initialJoinBehavior: str
    contactListTabs: ContactListTabs