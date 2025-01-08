from dishka import AnyOf, AsyncContainer, Provider, Scope, make_async_container
from faststream.rabbit.annotations import RabbitBroker
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

from app.application.common.event_bus import EventBus
from app.application.common.persistence.user_gateway import UserGateway
from app.application.common.unit_of_work import UnitOfWork
from app.application.operations.command.user.change_email import ChangeEmail
from app.application.operations.command.user.change_fullname import ChangeFullname
from app.application.operations.command.user.create_user import CreateUser
from app.application.operations.command.user.delete_user_permanently import DeleteUserPermanently
from app.application.operations.command.user.delete_user_temporarily import DeleteUserTemporarily
from app.application.operations.command.user.recovery_user import RecoveryUser
from app.application.operations.query.get_user_by_id import GetUserById
from app.domain.model.user.factory import UserFactory
from app.domain.model.user.repository import UserRepository
from app.domain.shared.unit_of_work import UnitOfWorkTracker
from app.infrastructure.brokers.publisher import MessagePublisher
from app.infrastructure.brokers.rabbit.config import RabbitConfig
from app.infrastructure.brokers.rabbit.main import AMQPBroker, setup_amqp_broker
from app.infrastructure.brokers.rabbit.publisher import MessagePublisherImpl
from app.infrastructure.config import Config
from app.infrastructure.databases.postgres.config import PostgresConfig
from app.infrastructure.databases.postgres.gateways.user_finder import UserFinder
from app.infrastructure.databases.postgres.gateways.user_reader import UserReader
from app.infrastructure.databases.postgres.gateways.user_repository import UserRepositoryImpl
from app.infrastructure.databases.postgres.main import setup_datamappers, setup_sqla_connection, setup_sqla_engine
from app.infrastructure.databases.postgres.registry import Registry
from app.infrastructure.databases.postgres.unit_of_work import UnitOfWorkImpl
from app.infrastructure.event_bus.event_bus import EventBusImpl


def setup_async_container(registry: Registry, config: Config) -> AsyncContainer:
    provider = Provider()

    setup_datamappers(registry=registry)
    setup_provider(provider=provider)

    return make_async_container(
        provider,
        context={
            RabbitConfig: config.rabbit,
            PostgresConfig: config.postgres,
            Registry: registry,
        },
    )


def setup_provider(provider: Provider) -> None:
    provide_command_handlers(provider=provider)
    provide_broker(provider=provider)
    provide_event_bus(provider=provider)
    provide_db(provider=provider)
    provide_db_uow(provider=provider)
    provide_db_factories(provider=provider)
    provide_config(provider=provider)
    provide_query_handlers(provider=provider)


def provide_config(provider: Provider) -> None:
    provider.from_context(scope=Scope.APP, provides=RabbitConfig)
    provider.from_context(scope=Scope.APP, provides=PostgresConfig)


def provide_command_handlers(provider: Provider) -> None:
    provider.provide(ChangeEmail, scope=Scope.REQUEST)
    provider.provide(ChangeFullname, scope=Scope.REQUEST)
    provider.provide(CreateUser, scope=Scope.REQUEST)
    provider.provide(DeleteUserPermanently, scope=Scope.REQUEST)
    provider.provide(DeleteUserTemporarily, scope=Scope.REQUEST)
    provider.provide(RecoveryUser, scope=Scope.REQUEST)


def provide_query_handlers(provider: Provider) -> None:
    provider.provide(GetUserById, scope=Scope.REQUEST)


def provide_broker(provider: Provider) -> None:
    provider.provide(AMQPBroker, scope=Scope.APP, provides=AMQPBroker)
    provider.provide(setup_amqp_broker, scope=Scope.APP, provides=RabbitBroker)


def provide_event_bus(provider: Provider) -> None:
    provider.provide(EventBusImpl, scope=Scope.REQUEST, provides=EventBus)
    provider.provide(MessagePublisherImpl, scope=Scope.REQUEST, provides=MessagePublisher)


def provide_db(provider: Provider) -> None:
    provider.provide(setup_sqla_engine, scope=Scope.APP, provides=AsyncEngine)
    provider.provide(setup_sqla_connection, scope=Scope.REQUEST, provides=AsyncConnection)


def provide_db_uow(provider: Provider) -> None:
    provider.from_context(scope=Scope.APP, provides=Registry)
    provider.provide(UnitOfWorkImpl, scope=Scope.REQUEST, provides=AnyOf[UnitOfWork, UnitOfWorkTracker])


def provide_db_factories(provider: Provider) -> None:
    provider.provide(UserRepositoryImpl, scope=Scope.REQUEST, provides=UserRepository)
    provider.provide(UserFactory, scope=Scope.REQUEST, provides=UserFactory)
    provider.provide(UserFinder, scope=Scope.REQUEST, provides=UserFinder)
    provider.provide(UserReader, scope=Scope.REQUEST, provides=UserGateway)
