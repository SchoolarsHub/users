from dishka import Provider, Scope
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

from app.application.operations.command.change_contacts import ChangeContacts
from app.application.operations.command.change_fullname import ChangeFullname
from app.application.operations.command.change_social_network_connection_reason import ChangeSocialNetworkConnectionReason
from app.application.operations.command.create_user import CreateUser
from app.application.operations.command.delete_user_permanently import DeleteUserPermanently
from app.application.operations.command.delete_user_temporarily import DeleteUserTemporarily
from app.application.operations.command.link_social_network import LinkSocialNetwork
from app.application.operations.command.recovery_user import RecoveryUser
from app.application.operations.command.unlink_social_network import UnlinkSocialNetwork
from app.application.operations.query.get_user_by_id import GetUserById
from app.domain.model.linked_account.linked_account import LinkedAccount
from app.domain.model.user.repository import UserRepository
from app.domain.model.user.user import User
from app.infrastructure.databases.postgres.gateways.generic_datamapper import GenericDataMapper
from app.infrastructure.databases.postgres.gateways.linked_account_datamapper import LinkedAccountDataMapper
from app.infrastructure.databases.postgres.gateways.user_datamapper import UserDataMapper
from app.infrastructure.databases.postgres.gateways.user_finder import UserFinder
from app.infrastructure.databases.postgres.gateways.user_repository import UserRepositoryImpl
from app.infrastructure.databases.postgres.main import setup_sqla_connection, setup_sqla_engine


def provide_command_handlers(provider: Provider) -> None:
    provider.provide(ChangeContacts, scope=Scope.REQUEST)
    provider.provide(ChangeFullname, scope=Scope.REQUEST)
    provider.provide(ChangeSocialNetworkConnectionReason, scope=Scope.REQUEST)
    provider.provide(CreateUser, scope=Scope.REQUEST)
    provider.provide(DeleteUserPermanently, scope=Scope.REQUEST)
    provider.provide(DeleteUserTemporarily, scope=Scope.REQUEST)
    provider.provide(LinkSocialNetwork, scope=Scope.REQUEST)
    provider.provide(RecoveryUser, scope=Scope.REQUEST)
    provider.provide(UnlinkSocialNetwork, scope=Scope.REQUEST)


def provide_query_handlers(provider: Provider) -> None:
    provider.provide(GetUserById, scope=Scope.REQUEST)


def provide_db_gateways(provider: Provider) -> None:
    provider.provide(UserDataMapper, scope=Scope.REQUEST, provides=GenericDataMapper[User])
    provider.provide(LinkedAccountDataMapper, scope=Scope.REQUEST, provides=GenericDataMapper[LinkedAccount])
    provider.provide(UserFinder, scope=Scope.REQUEST)
    provider.provide(UserRepositoryImpl, scope=Scope.REQUEST, provides=UserRepository)


def provide_db_factories(provider: Provider) -> None:
    provider.provide(setup_sqla_connection, scope=Scope.REQUEST, provides=AsyncConnection)
    provider.provide(setup_sqla_engine, scope=Scope.REQUEST, provides=AsyncEngine)


def provide_db_transactions_tools(provider: Provider) -> None: ...
