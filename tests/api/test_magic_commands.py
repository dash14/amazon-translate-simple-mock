import json
from unittest.mock import AsyncMock

AMZ = "application/x-amz-json-1.1"


class TestReturnRequestedBody:
    def test_returns_request_body_as_translated_text(self, post, text_payload):
        payload = text_payload("@return RequestedBody", source="ja", target="en")
        response = post(payload)
        assert response.status_code == 200
        result = response.json()["TranslatedText"]
        parsed = json.loads(result)
        assert parsed["Text"] == "@return RequestedBody"

    def test_return_requested_body_includes_source_language(self, post, text_payload):
        payload = text_payload("@return RequestedBody", source="ja", target="en")
        response = post(payload)
        result = response.json()["TranslatedText"]
        parsed = json.loads(result)
        assert parsed["SourceLanguageCode"] == "ja"


class TestReturnSourceLanguageCode:
    def test_overrides_source_language_code(self, post, text_payload):
        response = post(text_payload("@return SourceLanguageCode fr", source="ja", target="en"))
        assert response.status_code == 200
        assert response.json()["SourceLanguageCode"] == "fr"

    def test_overrides_auto_detection(self, post, text_payload):
        response = post(text_payload("@return SourceLanguageCode de", source="auto", target="en"))
        assert response.status_code == 200
        assert response.json()["SourceLanguageCode"] == "de"


class TestRaiseCommands:
    def test_raise_throttling_exception(self, post, text_payload):
        response = post(text_payload("@raise ThrottlingException", source="ja", target="en"))
        assert response.status_code == 429
        assert response.json()["__type"] == "ThrottlingException"

    def test_raise_internal_server_exception(self, post, text_payload):
        response = post(text_payload("@raise InternalServerException", source="ja", target="en"))
        assert response.status_code == 500
        assert response.json()["__type"] == "InternalServerException"

    def test_raise_limit_exceeded_exception(self, post, text_payload):
        response = post(text_payload("@raise LimitExceededException", source="ja", target="en"))
        assert response.status_code == 400
        assert response.json()["__type"] == "LimitExceededException"

    def test_raise_service_unavailable_exception(self, post, text_payload):
        response = post(text_payload("@raise ServiceUnavailableException", source="ja", target="en"))
        assert response.status_code == 500
        assert response.json()["__type"] == "ServiceUnavailableException"

    def test_raise_too_many_requests_exception(self, post, text_payload):
        response = post(text_payload("@raise TooManyRequestsException", source="ja", target="en"))
        assert response.status_code == 400
        assert response.json()["__type"] == "TooManyRequestsException"

    def test_raise_unsupported_language_pair_exception(self, post, text_payload):
        response = post(text_payload("@raise UnsupportedLanguagePairException", source="ja", target="en"))
        assert response.status_code == 400
        assert response.json()["__type"] == "UnsupportedLanguagePairException"

    def test_raise_response_has_message(self, post, text_payload):
        response = post(text_payload("@raise ThrottlingException", source="ja", target="en"))
        assert "message" in response.json()

    def test_raise_response_content_type_amz(self, post, text_payload):
        response = post(text_payload("@raise ThrottlingException", source="ja", target="en"))
        assert AMZ in response.headers["content-type"]


class TestSleepCommand:
    def test_sleep_zero_returns_normal_response(self, post, text_payload):
        response = post(text_payload("@sleep 0 テスト", source="ja", target="en"))
        assert response.status_code == 200
        assert "TranslatedText" in response.json()

    def test_sleep_with_raise_still_raises(self, post, text_payload):
        response = post(text_payload(
            "@sleep 0 @raise ThrottlingException",
            source="ja", target="en"
        ))
        assert response.status_code == 429

    def test_sleep_calls_asyncio_sleep(self, mocker, post, text_payload):
        mock_sleep = mocker.patch("app.main.asyncio.sleep", new_callable=AsyncMock)
        response = post(text_payload("@sleep 5 テスト", source="ja", target="en"))
        assert response.status_code == 200
        mock_sleep.assert_called_once_with(5.0)

    def test_sleep_decimal_seconds(self, mocker, post, text_payload):
        mock_sleep = mocker.patch("app.main.asyncio.sleep", new_callable=AsyncMock)
        post(text_payload("@sleep 0.5 テスト", source="ja", target="en"))
        mock_sleep.assert_called_once_with(0.5)
