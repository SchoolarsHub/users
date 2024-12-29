from datetime import UTC, datetime
from typing import Self
from uuid import UUID

from app.domain.models.user.entities.avatar import Avatar
from app.domain.models.user.entities.linked_account import LinkedAccount
from app.domain.models.user.enums.account_statuses import AccountStatuses
from app.domain.models.user.enums.file_extensions import FileExtensions
from app.domain.models.user.enums.social_networks import SocialNetworks
from app.domain.models.user.events.avatar.avatar_added import AvatarAdded
from app.domain.models.user.events.avatar.avatar_deleted import AvatarDeleted
from app.domain.models.user.events.linked_account.social_network_linked import SocialNetworkLinked
from app.domain.models.user.events.linked_account.social_network_unlinked import SocialNetworkUnlinked
from app.domain.models.user.events.user.address_changed import AddressChanged
from app.domain.models.user.events.user.bio_changed import BioChanged
from app.domain.models.user.events.user.contacts_changed import ContactsChanged
from app.domain.models.user.events.user.status_changed import StatusChanged
from app.domain.models.user.events.user.user_created import UserCreated
from app.domain.models.user.events.user.user_deleted import UserDeleted
from app.domain.models.user.events.user.username_changed import UsernameChanged
from app.domain.models.user.exceptions.avatar_exceptions import AvatarNotFoundError, InvalidAvatarFileExtensionError
from app.domain.models.user.exceptions.linked_account_exceptions import (
    InvalidSocialNetworkError,
    LinkedAccountNotFoundError,
    LinkedAccountUrlAlreadyExistsError,
)
from app.domain.models.user.exceptions.user_exceptions import InvalidUserAccountStatusError, UserInactiveError
from app.domain.models.user.value_objects.address import Address
from app.domain.models.user.value_objects.contacts import Contacts
from app.domain.models.user.value_objects.file_data import FileData
from app.domain.shared.event import Event
from app.domain.shared.unit_of_work import UnitOfWorkTracker
from app.domain.shared.uowed_entity import UowedEntity


class User(UowedEntity[UUID]):
    def __init__(
        self,
        user_id: UUID,
        username: str,
        created_at: datetime,
        account_status: AccountStatuses,
        contacts: Contacts,
        unit_of_work: UnitOfWorkTracker,
        friends: list[Self],
        subscribers: list[Self],
        subscribed_to: list[Self],
        my_friendship_requests: list[Self],
        friendship_requests_to_me: list[Self],
        blocked_users: list[Self],
        avatars: list[Avatar],
        linked_accounts: list[LinkedAccount],
        bio: str | None = None,
        address: Address | None = None,
    ) -> None:
        super().__init__(user_id, unit_of_work)

        self.username = username
        self.created_at = created_at
        self.frineds = friends
        self.subscribers = subscribers
        self.account_status = account_status
        self.subscribed_to = subscribed_to
        self.my_friendship_requests = my_friendship_requests
        self.friendship_requests_to_me = friendship_requests_to_me
        self.blocked_users = blocked_users
        self.bio = bio
        self.avatars = avatars
        self.linked_accounts = linked_accounts
        self.address = address
        self.contacts = contacts

        self._events: list[Event] = []

    def record_event(self, event: Event) -> None:
        self._events.append(event)

    def raise_events(self) -> list[Event]:
        events = self._events.copy()
        self._events.clear()
        return events

    @classmethod
    def create_user(cls: type[Self], user_id: UUID, username: str, unit_of_work: UnitOfWorkTracker) -> Self:
        user = cls(
            user_id=user_id,
            username=username,
            created_at=datetime.now(UTC),
            unit_of_work=unit_of_work,
            account_status=AccountStatuses.ACTIVE,
        )
        user.mark_new()
        user.record_event(
            UserCreated(
                event_name="UserCreated",
                aggregate_name="User",
                aggregate_uuid=user.entity_id,
                user_id=user.entity_id,
                username=user.username,
                email=user.contacts.email,
                phone=user.contacts.phone,
                created_at=user.created_at,
                account_status=user.account_status,
                bio=user.bio,
                city=user.address.city if user.address else None,
                country=user.address.country if user.address else None,
            )
        )

        return user

    def change_account_status(self, account_status: AccountStatuses) -> None:
        if account_status not in list(AccountStatuses):
            raise InvalidUserAccountStatusError(title=f"Invalid account status: {account_status}. ")

        self.account_status = account_status
        self.mark_dirty()
        self.record_event(
            StatusChanged(
                event_name="StatusChanged",
                aggregate_name="User",
                aggregate_uuid=self.entity_id,
                user_id=self.entity_id,
                new_status=self.account_status,
            )
        )

    def change_address(self, address: Address | None = None) -> None:
        if self.account_status == AccountStatuses.INACTIVE:
            raise UserInactiveError(title=f"User {self.entity_id} is inactive. ")

        self.address = address
        self.mark_dirty()
        self.record_event(
            AddressChanged(
                event_name="AddressChanged",
                aggregate_name="User",
                aggregate_uuid=self.entity_id,
                user_id=self.entity_id,
                new_city=self.address.city if self.address else None,
                new_country=self.address.country if self.address else None,
            )
        )

    def change_username(self, username: str) -> None:
        if self.account_status == AccountStatuses.INACTIVE:
            raise UserInactiveError(title=f"User {self.entity_id} is inactive. ")

        self.username = username
        self.mark_dirty()
        self.record_event(
            UsernameChanged(
                event_name="UsernameChanged",
                aggregate_name="User",
                aggregate_uuid=self.entity_id,
                user_id=self.entity_id,
                new_username=self.username,
            )
        )

    def change_bio(self, bio: str | None = None) -> None:
        if self.account_status == AccountStatuses.INACTIVE:
            raise UserInactiveError(title=f"User {self.entity_id} is inactive. ")

        self.bio = bio
        self.mark_dirty()
        self.record_event(
            BioChanged(
                event_name="BioChanged",
                aggregate_name="User",
                aggregate_uuid=self.entity_id,
                user_id=self.entity_id,
                new_bio=self.bio,
            )
        )

    def change_contacts(self, contacts: Contacts) -> None:
        if self.account_status == AccountStatuses.INACTIVE:
            raise UserInactiveError(title=f"User {self.entity_id} is inactive. ")

        self.contacts = contacts
        self.mark_dirty()
        self.record_event(
            ContactsChanged(
                event_name="ContactsChanged",
                aggregate_name="User",
                aggregate_uuid=self.entity_id,
                user_id=self.entity_id,
                new_email=self.contacts.email,
                new_phone=self.contacts.phone,
            )
        )

    def add_avatar(self, avatar_id: UUID, file_data: FileData, content: bytes) -> None:
        if self.account_status == AccountStatuses.INACTIVE:
            raise UserInactiveError(title=f"User {self.entity_id} is inactive. ")

        if file_data.file_extension not in list(FileExtensions):
            raise InvalidAvatarFileExtensionError(title=f"Invalid file extension: {file_data.file_extension}. ")

        avatar = Avatar.create_avatar(
            user_id=self.entity_id, unit_of_work=self.unit_of_work, avatar_id=avatar_id, file_data=file_data, content=content
        )
        self.avatars.append(avatar)
        self.record_event(
            AvatarAdded(
                event_name="AvatarAdded",
                aggregate_name="User",
                aggregate_uuid=self.entity_id,
                user_id=self.entity_id,
                avatar_id=avatar.entity_id,
                filename=avatar.file_data.filename,
                file_extension=avatar.file_data.file_extension,
                file_size=avatar.file_data.file_size,
                uploaded_at=avatar.uploaded_at,
            )
        )

    def remove_avatar(self, avatar_id: UUID) -> None:
        if self.account_status == AccountStatuses.INACTIVE:
            raise UserInactiveError(title=f"User {self.entity_id} is inactive. ")

        for avatar in self.avatars:
            if avatar.avatar_id == avatar_id:
                avatar.mark_deleted()
                self.record_event(
                    AvatarDeleted(
                        event_name="AvatarDeleted",
                        aggregate_name="User",
                        aggregate_uuid=self.entity_id,
                        user_id=self.entity_id,
                        avatar_id=avatar.entity_id,
                    )
                )
                break

        raise AvatarNotFoundError(f"Avatar with id {avatar_id} not found")

    def add_linked_account(self, linked_account_id: UUID, social_netw: SocialNetworks, conn_link: str) -> None:
        if self.account_status == AccountStatuses.INACTIVE:
            raise UserInactiveError(title=f"User {self.entity_id} is inactive. ")

        if social_netw not in list(SocialNetworks):
            raise InvalidSocialNetworkError(title=f" Invalid social network: {social_netw}. ")

        for linked_account in self.linked_accounts:
            if linked_account.connection_link == conn_link:
                raise LinkedAccountUrlAlreadyExistsError(title=f"Linked account with url {conn_link} already exists. ")

        linked_account = LinkedAccount.create_linked_account(
            user_id=self.entity_id,
            unit_of_work=self.unit_of_work,
            linked_account_id=linked_account_id,
            social_network=social_netw,
            connection_link=conn_link,
        )
        self.linked_accounts.append(linked_account)
        self.record_event(
            SocialNetworkLinked(
                event_name="SocialNetworkLinked",
                aggregate_name="User",
                aggregate_uuid=self.entity_id,
                user_id=self.entity_id,
                linked_account_id=linked_account.entity_id,
                social_network_name=linked_account.social_network,
                connection_link=linked_account.connection_link,
            )
        )

    def remove_linked_account(self, linked_account_id: UUID) -> None:
        if self.account_status == AccountStatuses.INACTIVE:
            raise UserInactiveError(title=f"User {self.entity_id} is inactive. ")

        for linked_account in self.linked_accounts:
            if linked_account.linked_account_id == linked_account_id:
                linked_account.mark_deleted()
                self.record_event(
                    SocialNetworkUnlinked(
                        event_name="SocialNetworkUnlinked",
                        aggregate_name="User",
                        aggregate_uuid=self.entity_id,
                        user_id=self.entity_id,
                        linked_account_id=linked_account.entity_id,
                    )
                )
                break

        raise LinkedAccountNotFoundError(f"Linked account with id {linked_account_id} not found")

    def delete_user(self) -> None:
        if self.account_status == AccountStatuses.INACTIVE:
            raise UserInactiveError(title=f"User {self.entity_id} is inactive. ")

        self.mark_deleted()

        for avatar in self.avatars:
            avatar.delete_avatar()

        for linked_account in self.linked_accounts:
            linked_account.delete_linked_account()

        self.record_event(
            UserDeleted(
                event_name="UserDeleted",
                aggregate_name="User",
                aggregate_uuid=self.entity_id,
                user_id=self.entity_id,
            )
        )
