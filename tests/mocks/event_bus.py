from app.application.common.event_bus import EventBus
from app.domain.shared.event import Event


class FakeEventBus(EventBus):
    def __init__(self) -> None:
        self.events: list[Event] = []

    async def publish(self, events: list[Event]) -> None:
        for event in events:
            self.events.append(event)
