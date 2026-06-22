import json
from app.errors import error_responses

EXPECTED_ERRORS = {
    "ThrottlingException": 429,
    "InternalServerException": 500,
    "LimitExceededException": 400,
    "ServiceUnavailableException": 500,
    "TooManyRequestsException": 400,
    "UnsupportedLanguagePairException": 400,
}


def test_all_error_types_defined():
    assert set(error_responses.keys()) == set(EXPECTED_ERRORS.keys())


class TestErrorStatusCodes:
    def test_throttling_exception_status(self):
        assert error_responses["ThrottlingException"].status_code == 429

    def test_internal_server_exception_status(self):
        assert error_responses["InternalServerException"].status_code == 500

    def test_limit_exceeded_exception_status(self):
        assert error_responses["LimitExceededException"].status_code == 400

    def test_service_unavailable_exception_status(self):
        assert error_responses["ServiceUnavailableException"].status_code == 500

    def test_too_many_requests_exception_status(self):
        assert error_responses["TooManyRequestsException"].status_code == 400

    def test_unsupported_language_pair_exception_status(self):
        assert error_responses["UnsupportedLanguagePairException"].status_code == 400


class TestErrorContentType:
    def test_all_errors_have_amz_content_type(self):
        for key, response in error_responses.items():
            assert response.media_type == "application/x-amz-json-1.1", (
                f"{key} has unexpected media_type: {response.media_type}"
            )


class TestErrorBody:
    def _parse_body(self, key):
        return json.loads(error_responses[key].body)

    def test_throttling_has_type_field(self):
        body = self._parse_body("ThrottlingException")
        assert "__type" in body

    def test_throttling_has_message_field(self):
        body = self._parse_body("ThrottlingException")
        assert "message" in body

    def test_throttling_type_value(self):
        body = self._parse_body("ThrottlingException")
        assert body["__type"] == "ThrottlingException"

    def test_all_errors_have_type_and_message(self):
        for key in error_responses:
            body = self._parse_body(key)
            assert "__type" in body, f"{key} missing __type"
            assert "message" in body, f"{key} missing message"

    def test_all_errors_type_matches_key(self):
        for key in error_responses:
            body = self._parse_body(key)
            assert body["__type"] == key, f"{key} has mismatched __type: {body['__type']}"
