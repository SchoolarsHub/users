from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4


@dataclass(frozen=True, kw_only=True)
class IntegrationEvent:
    event_uuid: UUID = field(default=uuid4())
    event_occured_at: datetime = field(default=datetime.now(UTC))
    event_name: str = field(default="IntegrationEvent")

    def to_dict(self) -> dict[str, str]:
        return asdict(self)
