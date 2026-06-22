FROM python:3.12-alpine AS builder

WORKDIR /code
RUN apk add build-base libffi-dev
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

FROM python:3.12-alpine AS prod

LABEL org.opencontainers.image.name="amazon-translate-simple-mock" \
      org.opencontainers.image.authors="dash14.ack@gmail.com" \
      org.opencontainers.image.url="https://github.com/dash14/amazon-translate-simple-mock" \
      org.opencontainers.image.source="https://github.com/dash14/amazon-translate-simple-mock"

ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY --from=builder /code/.venv /code/.venv
ENV PATH="/code/.venv/bin:$PATH"
COPY ./app /code/app
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
