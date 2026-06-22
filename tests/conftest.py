import base64

import pytest
from starlette.testclient import TestClient

from app.main import app

AMZ_CONTENT_TYPE = "application/x-amz-json-1.1"


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def amz_headers():
    return {"Content-Type": AMZ_CONTENT_TYPE}


@pytest.fixture
def post(client, amz_headers):
    def _post(payload: dict, headers: dict | None = None):
        h = {**amz_headers, **(headers or {})}
        return client.post("/", json=payload, headers=h)

    return _post


@pytest.fixture
def text_payload():
    def _make(text, source="ja", target="en", settings=None, terminology_names=None):
        p = {"Text": text, "SourceLanguageCode": source, "TargetLanguageCode": target}
        if settings:
            p["Settings"] = settings
        if terminology_names is not None:
            p["TerminologyNames"] = terminology_names
        return p

    return _make


@pytest.fixture
def doc_payload():
    def _make(content, content_type="text/html", source="ja", target="en"):
        return {
            "Document": {
                "Content": base64.b64encode(content.encode()).decode(),
                "ContentType": content_type,
            },
            "SourceLanguageCode": source,
            "TargetLanguageCode": target,
        }

    return _make
