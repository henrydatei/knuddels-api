import dataclasses
from typing import List

from .FotomeetUser import FotomeetUser

@dataclasses.dataclass
class FotomeetStatus:
    currentCandidate: FotomeetUser
    prefetchImageUrls: List[str]
    isPremium: bool
    potentialMatchCount: int