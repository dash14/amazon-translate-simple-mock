def test_no_text_no_document(post):
    response = post({"SourceLanguageCode": "ja", "TargetLanguageCode": "en"})
    assert response.status_code == 422


def test_text_and_document_both(post, doc_payload):
    payload = doc_payload("テスト")
    payload["Text"] = "テスト"
    response = post(payload)
    assert response.status_code == 422


def test_missing_source_language_code(post):
    response = post({"Text": "hello", "TargetLanguageCode": "ja"})
    assert response.status_code == 422


def test_missing_target_language_code(post):
    response = post({"Text": "hello", "SourceLanguageCode": "en"})
    assert response.status_code == 422


def test_empty_body(client):
    response = client.post(
        "/", content="", headers={"Content-Type": "application/x-amz-json-1.1"}
    )
    assert response.status_code == 422


def test_document_missing_content(post):
    response = post(
        {
            "Document": {"ContentType": "text/html"},
            "SourceLanguageCode": "ja",
            "TargetLanguageCode": "en",
        }
    )
    assert response.status_code == 422


def test_document_missing_content_type(post):
    response = post(
        {
            "Document": {"Content": "aGVsbG8="},
            "SourceLanguageCode": "ja",
            "TargetLanguageCode": "en",
        }
    )
    assert response.status_code == 422


def test_validation_error_response_has_detail(post):
    response = post({"SourceLanguageCode": "ja", "TargetLanguageCode": "en"})
    assert "detail" in response.json()
