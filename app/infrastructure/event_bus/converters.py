from app.domain.model.linked_account.events import ConnectionReasonChanged, LinkedAccountCreated, LinkedAccountDeleted
from app.domain.model.user.events import (
    ContactsChanged,
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
    ContactsChangedIntegration,
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
            return UserCreatedIntegration(
                user_id=event.user_id,
                firstname=event.firstname,
                lastname=event.lastname,
                middlename=event.middlename,
                status=event.status,
                event_uuid=event.event_uuid,
                event_occured_at=event.event_occured_at,
            )

        case UserPermanentlyDeleted():
            return UserPermanentlyDeletedIntegration(user_id=event.user_id, event_uuid=event.event_uuid, event_occured_at=event.event_occured_at)

        case UserRecoveried():
            return UserRecoveriedIntegration(
                user_id=event.user_id, status=event.status, event_uuid=event.event_uuid, event_occured_at=event.event_occured_at
            )

        case UserTemporarilyDeleted():
            return UserTemporarilyDeletedIntegration(
                user_id=event.user_id,
                status=event.status,
                deleted_at=event.deleted_at,
                event_uuid=event.event_uuid,
                event_occured_at=event.event_occured_at,
            )

        case UserActivated():
            return UserActivatedIntegration(
                user_id=event.user_id, status=event.status, event_uuid=event.event_uuid, event_occured_at=event.event_occured_at
            )

        case FullnameChanged():
            return FullnameChangedIntegration(
                user_id=event.user_id,
                firstname=event.firstname,
                lastname=event.lastname,
                middlename=event.middlename,
                event_uuid=event.event_uuid,
                event_occured_at=event.event_occured_at,
            )

        case ContactsChanged():
            return ContactsChangedIntegration(
                user_id=event.user_id, email=event.email, phone=event.phone, event_uuid=event.event_uuid, event_occured_at=event.event_occured_at
            )

        case LinkedAccountCreated():
            return LinkedAccountCreatedIntegration(
                linked_account_id=event.linked_account_id,
                social_network=event.social_network,
                connected_for=event.connected_for,
                event_uuid=event.event_uuid,
                event_occured_at=event.event_occured_at,
            )

        case LinkedAccountDeleted():
            return LinkedAccountDeletedIntegration(
                linked_account_id=event.linked_account_id, event_uuid=event.event_uuid, event_occured_at=event.event_occured_at
            )

        case ConnectionReasonChanged():
            return ConnectionReasonChangedIntegration(
                linked_account_id=event.linked_account_id,
                connected_for=event.connected_for,
                event_uuid=event.event_uuid,
                event_occured_at=event.event_occured_at,
            )
