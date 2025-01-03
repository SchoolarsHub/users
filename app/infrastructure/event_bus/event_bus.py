from app.application.common.event_bus import EventBus
from app.domain.shared.event import Event
from app.infrastructure.brokers.message import Message
from app.infrastructure.brokers.publisher import MessagePublisher
from app.infrastructure.event_bus.converters import convert_domain_event_to_integration


class EventBusImpl(EventBus):
    def __init__(self, publisher: MessagePublisher) -> None:
        self.publisher = publisher

    async def publish(self, events: list[Event]) -> None:
        for event in events:
            await self.publisher.publish(message=self._build_message(event))

    def _build_message(self, event: Event) -> Message:
        integration_event = convert_domain_event_to_integration(event)

        return Message(message_id=integration_event.event_uuid, data=integration_event.to_dict())
