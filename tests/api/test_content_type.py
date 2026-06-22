AMZ = "application/x-amz-json-1.1"
JSON = "application/json"

PAYLOAD = {
    "Text": "hello",
    "SourceLanguageCode": "en",
    "TargetLanguageCode": "ja",
}


def test_amz_content_type_accepted(client):
    response = client.post("/", json=PAYLOAD, headers={"Content-Type": AMZ})
    assert response.status_code == 200


def test_plain_json_content_type_accepted(client):
    response = client.post("/", json=PAYLOAD, headers={"Content-Type": JSON})
    assert response.status_code == 200


def test_response_content_type_amz_when_request_amz(client):
    response = client.post("/", json=PAYLOAD, headers={"Content-Type": AMZ})
    assert AMZ in response.headers["content-type"]


def test_response_content_type_json_when_request_json(client):
    response = client.post("/", json=PAYLOAD, headers={"Content-Type": JSON})
    assert JSON in response.headers["content-type"]
