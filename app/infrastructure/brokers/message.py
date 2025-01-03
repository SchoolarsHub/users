from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(frozen=True, kw_only=True)
class Message:
    message_id: UUID = field(default=uuid4())
    data: dict[str, str] | None = field(default=None)

    def as_dict(self) -> dict[str, str]:
        return {
            "message_id": self.message_id,
            "data": self.data,
        }