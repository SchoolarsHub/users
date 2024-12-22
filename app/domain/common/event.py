from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(frozen=True, kw_only=True)
class Event:
    event_uuid: UUID = field(default_factory=uuid4, init=False)
    event_occured_at: datetime = field(default_factory=datetime.now, init=False)
    event_name: str
    aggregate_name: str
    aggregate_uuid: UUID
