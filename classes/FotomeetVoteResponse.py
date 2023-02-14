import dataclasses
from typing import Optional

from .FotomeetStatus import FotomeetStatus

@dataclasses.dataclass
class FotomeetVoteResponse:
    error: Optional[str]
    newStatus: FotomeetStatus