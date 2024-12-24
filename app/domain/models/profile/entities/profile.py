from datetime import UTC, datetime
from typing import Self
from uuid import UUID

from app.domain.common.event import Event
from app.domain.common.unit_of_work import UnitOfWorkTracker
from app.domain.common.uowed_entity import UowedEntity
from app.domain.models.profile.entities.avatar import Avatar
from app.domain.models.profile.entities.linked_account import LinkedAccount
from app.domain.models.profile.enums.allowed_accounts import AllowedAccounts
from app.domain.models.profile.enums.allowed_extensions import AllowedExtensions
from app.domain.models.profile.enums.profile_types import ProfileTypes
from app.domain.models.profile.events.avatar_added import AvatarAdded
from app.domain.models.profile.events.avatar_deleted import AvatarDeleted
from app.domain.models.profile.events.linked_account_added import LinkedAccountAdded
from app.domain.models.profile.events.linked_account_deleted import LinkedAccountDeleted
from app.domain.models.profile.events.profile_created import ProfileCreated
from app.domain.models.profile.events.profile_deleted import ProfileDeleted
from app.domain.models.profile.exceptions.profile_exceptions import (
    AvatarNotFoundError,
    InvalidFileExtensionError,
    InvalidLinkedAccountNameError,
    InvalidProfileTypeError,
    LinkedAccountNotFoundError,
)
from app.domain.models.profile.value_objects.fullname import Fullname


class Profile(UowedEntity[UUID]):
    def __init__(
        self,
        profile_id: UUID,
        user_id: UUID,
        unit_of_work: UnitOfWorkTracker[Self],
        profile_type: ProfileTypes,
        fullname: Fullname,
        created_at: datetime,
        bio: str | None = None,
        linked_accounts: list[LinkedAccount] | None = None,
        avatars: list[Avatar] | None = None,
    ) -> None:
        super().__init__(profile_id, unit_of_work)

        self.user_id = user_id
        self.events: list[Event] = []
        self.linked_accounts = linked_accounts if linked_accounts else []
        self.avatars = avatars if avatars else []
        self.profile_type = profile_type
        self.bio = bio
        self.fullname = fullname
        self.created_at = created_at

    @classmethod
    def create_profile(
        cls: type[Self],
        user_id: UUID,
        profile_id: UUID,
        unit_of_work: UnitOfWorkTracker[Self],
        profile_type: ProfileTypes,
        fullname: Fullname,
        bio: str | None = None,
    ) -> Self:
        if profile_type not in list(ProfileTypes):
            raise InvalidProfileTypeError(
                f"Invalid profile type, it must be in {list(ProfileTypes)}, got {profile_type}"
            )

        profile = cls(
            profile_id=profile_id,
            user_id=user_id,
            unit_of_work=unit_of_work,
            profile_type=profile_type,
            bio=bio,
            fullname=fullname,
            created_at=datetime.now(UTC),
        )
        profile.mark_new()
        profile.add_event(
            ProfileCreated(
                aggregate_name="Profile",
                aggregate_uuid=profile.entity_id,
                event_name="ProfileCreated",
                profile_id=profile.entity_id,
                user_id=profile.user_id,
                profile_type=profile.profile_type,
                first_name=profile.fullname.first_name,
                last_name=profile.fullname.last_name,
                middle_name=profile.fullname.middle_name,
                bio=profile.bio,
            )
        )

        return profile

    def change_profile_bio(self, new_bio: str) -> None:
        self.bio = new_bio
        self.mark_dirty()

    def change_fullname(self, new_fullname: Fullname) -> None:
        self.fullname = new_fullname
        self.mark_dirty()

    def add_linked_account(
        self, linked_account_id: UUID, linked_account_name: AllowedAccounts, linked_account_url: str
    ) -> None:
        if linked_account_name not in list(LinkedAccount):
            raise InvalidLinkedAccountNameError(
                f"Invalid linked account name, it must be in {list(LinkedAccount)}, got {linked_account_name}"
            )

        linked_account = LinkedAccount.create_linked_account(
            profile_id=self.entity_id,
            linked_account_id=linked_account_id,
            unit_of_work=self.unit_of_work,
            linked_account_name=linked_account_name,
            linked_account_url=linked_account_url,
        )
        self.linked_accounts.append(linked_account)
        self.add_event(
            LinkedAccountAdded(
                aggregate_name="Profile",
                aggregate_uuid=self.entity_id,
                event_name="LinkedAccountAdded",
                profile_id=self.entity_id,
                user_id=self.user_id,
                linked_account_id=linked_account.entity_id,
                linked_account_name=linked_account.linked_account_name,
                linked_account_url=linked_account.linked_account_url,
            )
        )

    def add_avatar(self, avatar_id: UUID, file_name: str, file_extension: AllowedExtensions, file_size: int) -> None:
        if file_extension not in list(AllowedExtensions):
            raise InvalidFileExtensionError(
                f"Invalid file extension, it must be in {list(AllowedExtensions)}, got {file_extension}"
            )

        avatar = Avatar.create_avatar(
            profile_id=self.entity_id,
            avatar_id=avatar_id,
            unit_of_work=self.unit_of_work,
            file_name=file_name,
            file_size=file_size,
            file_extension=file_extension,
        )
        self.avatars.append(avatar)
        self.add_event(
            AvatarAdded(
                aggregate_name="Profile",
                aggregate_uuid=self.entity_id,
                event_name="AvatarAdded",
                profile_id=self.entity_id,
                user_id=self.user_id,
                avatar_id=avatar.entity_id,
                file_name=avatar.file_name,
                file_size=avatar.file_size,
                file_extension=avatar.file_extension,
            )
        )

    def delete_linked_account(self, linked_account_id: UUID) -> None:
        for linked_account in self.linked_accounts:
            if linked_account.entity_id == linked_account_id:
                linked_account.delete_linked_account()
                self.linked_accounts.remove(linked_account)
                self.add_event(
                    LinkedAccountDeleted(
                        aggregate_name="Profile",
                        aggregate_uuid=self.entity_id,
                        event_name="LinkedAccountDeleted",
                        profile_id=self.entity_id,
                        user_id=self.user_id,
                        linked_account_id=linked_account.entity_id,
                    )
                )
                break

        raise LinkedAccountNotFoundError(f"Linked account with id {linked_account_id} not found")

    def delete_avatar(self, avatar_id: UUID) -> None:
        for avatar in self.avatars:
            if avatar.entity_id == avatar_id:
                avatar.delete_avatar()
                self.avatars.remove(avatar)
                self.add_event(
                    AvatarDeleted(
                        aggregate_name="Profile",
                        aggregate_uuid=self.entity_id,
                        event_name="AvatarDeleted",
                        profile_id=self.entity_id,
                        user_id=self.user_id,
                        avatar_id=avatar.entity_id,
                    )
                )
                break

        raise AvatarNotFoundError(f"Avatar with id {avatar_id} not found")

    def delete_profile(self) -> None:
        self.mark_deleted()

        for linked_account in self.linked_accounts:
            linked_account.delete_linked_account()

        for avatar in self.avatars:
            avatar.delete_avatar()

        self.add_event(
            ProfileDeleted(
                aggregate_name="Profile",
                aggregate_uuid=self.entity_id,
                event_name="ProfileDeleted",
                profile_id=self.entity_id,
                user_id=self.user_id,
            )
        )

    def add_event(self, event: Event) -> None:
        self.events.append(event)

    def raise_events(self) -> list[Event]:
        events = self.events.copy()
        self.events.clear()
        return events
