from dishka import AsyncContainer, Provider, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI


def provider_factory() -> Provider:
    return Provider()


def setup_container(provider: Provider) -> AsyncContainer:
    return make_async_container(provider)


def setup_di(container: AsyncContainer, app: FastAPI) -> None:
    setup_dishka(container, app)
