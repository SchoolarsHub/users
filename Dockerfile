FROM python:3.12-slim AS python

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1


FROM python as builder

RUN apt-get update && apt-get install -y --no-install-recommends curl

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-editable

RUN uv pip install --system -r pyproject.toml


FROM builder as prod

COPY . .

EXPOSE 8000

ENTRYPOINT ["gunicorn", "app.main.entrypoint:app_factory()", "--config", "conf/gunicorn_configuration.py"]
