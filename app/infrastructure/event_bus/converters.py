from app.domain.model.linked_account.events import ConnectionReasonChanged, LinkedAccountCreated, LinkedAccountDeleted
from app.domain.model.user.events import (
    EmailChanged,
    FullnameChanged,
    UserActivated,
    UserCreated,
    UserPermanentlyDeleted,
    UserRecoveried,
    UserTemporarilyDeleted,
)
from app.domain.shared.event import Event
from app.infrastructure.event_bus.integration_events.integration_event import IntegrationEvent
from app.infrastructure.event_bus.integration_events.linked_account_events import (
    ConnectionReasonChangedIntegration,
    LinkedAccountCreatedIntegration,
    LinkedAccountDeletedIntegration,
)
from app.infrastructure.event_bus.integration_events.user_events import (
    EmailChangedIntegration,
    FullnameChangedIntegration,
    UserActivatedIntegration,
    UserCreatedIntegration,
    UserPermanentlyDeletedIntegration,
    UserRecoveriedIntegration,
    UserTemporarilyDeletedIntegration,
)


def convert_domain_event_to_integration(event: Event) -> IntegrationEvent:
    match event:
        case UserCreated():
            return UserCreatedIntegration.from_domain_event(event)

        case UserPermanentlyDeleted():
            return UserPermanentlyDeletedIntegration.from_domain_event(event)

        case UserRecoveried():
            return UserRecoveriedIntegration.from_domain_event(event)

        case UserTemporarilyDeleted():
            return UserTemporarilyDeletedIntegration.from_domain_event(event)

        case UserActivated():
            return UserActivatedIntegration.from_domain_event(event)

        case FullnameChanged():
            return FullnameChangedIntegration.from_domain_event(event)

        case EmailChanged():
            return EmailChangedIntegration.from_domain_event(event)

        case LinkedAccountCreated():
            return LinkedAccountCreatedIntegration.from_domain_event(event)

        case LinkedAccountDeleted():
            return LinkedAccountDeletedIntegration.from_domain_event(event)

        case ConnectionReasonChanged():
            return ConnectionReasonChangedIntegration.from_domain_event(event)
