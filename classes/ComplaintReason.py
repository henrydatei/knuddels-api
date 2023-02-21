import dataclasses

@dataclasses.dataclass
class ComplaintReason:
    id: str
    name: str
    itemType: str