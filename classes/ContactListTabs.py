import dataclasses
from typing import List

from .Tabs import Tabs

@dataclasses.dataclass
class ContactListTabs:
    tabs: List[Tabs]