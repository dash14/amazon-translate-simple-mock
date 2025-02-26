FROM python:3.12-alpine as builder

LABEL org.opencontainers.image.name "amazon-translate-simple-mock"
LABEL org.opencontainers.image.authors "dash14.ack@gmail.com"
LABEL org.opencontainers.image.url https://github.com/dash14/amazon-translate-simple-mock
LABEL org.opencontainers.image.source https://github.com/dash14/amazon-translate-simple-mock

WORKDIR /code
RUN apk add build-base libffi-dev
RUN pip install --upgrade pip && pip install poetry==1.8.5
COPY pyproject.toml poetry.lock ./
RUN poetry export --without-hashes -f requirements.txt > requirements.txt
RUN pip install -r requirements.txt

FROM python:3.12-alpine as prod
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY ./app /code/app
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
