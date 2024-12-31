from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4


@dataclass(frozen=True, kw_only=True)
class Event:
    event_uuid: UUID = field(default_factory=uuid4, init=False)
    event_occured_at: datetime = field(default=datetime.now(UTC), init=False)
