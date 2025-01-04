from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI


def setup_di(container: AsyncContainer, app: FastAPI) -> None:
    setup_dishka(container, app)
