FROM python:3.14-alpine@sha256:c6ead215bfd31f1e433d968853b7a769989117115b728874824e6c0a27cb96fc AS builder

WORKDIR /code
RUN apk add build-base libffi-dev
COPY --from=ghcr.io/astral-sh/uv:0.11.23@sha256:d0a0a753ab981624b49c97abc98821c1c09f4ca69d1ef5cee69c501be3d88479 /uv /usr/local/bin/uv

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

FROM python:3.14-alpine@sha256:c6ead215bfd31f1e433d968853b7a769989117115b728874824e6c0a27cb96fc AS prod

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
