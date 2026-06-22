import pytest
from pydantic import ValidationError

from app.types import (
    TranslateRequest,
    TranslateResponse,
)


def make_request(**kwargs):
    return TranslateRequest.model_validate(kwargs)


class TestTranslateRequestValidation:
    def test_text_only_valid(self):
        req = make_request(
            Text="hello", SourceLanguageCode="en", TargetLanguageCode="ja"
        )
        assert req.text == "hello"
        assert req.document is None

    def test_document_only_valid(self):
        req = make_request(
            Document={"Content": "aGVsbG8=", "ContentType": "text/html"},
            SourceLanguageCode="en",
            TargetLanguageCode="ja",
        )
        assert req.text is None
        assert req.document is not None

    def test_text_and_document_raises(self):
        with pytest.raises(ValidationError):
            make_request(
                Text="hello",
                Document={"Content": "aGVsbG8=", "ContentType": "text/html"},
                SourceLanguageCode="en",
                TargetLanguageCode="ja",
            )

    def test_neither_text_nor_document_raises(self):
        with pytest.raises(ValidationError):
            make_request(SourceLanguageCode="en", TargetLanguageCode="ja")

    def test_camelcase_source_language_code(self):
        req = make_request(Text="hi", SourceLanguageCode="en", TargetLanguageCode="ja")
        assert req.source_language_code == "en"

    def test_camelcase_target_language_code(self):
        req = make_request(Text="hi", SourceLanguageCode="en", TargetLanguageCode="ja")
        assert req.target_language_code == "ja"

    def test_terminology_names_default_empty(self):
        req = make_request(Text="hi", SourceLanguageCode="en", TargetLanguageCode="ja")
        assert req.terminology_names == []

    def test_terminology_names_set(self):
        req = make_request(
            Text="hi",
            SourceLanguageCode="en",
            TargetLanguageCode="ja",
            TerminologyNames=["custom1", "custom2"],
        )
        assert req.terminology_names == ["custom1", "custom2"]

    def test_settings_optional(self):
        req = make_request(Text="hi", SourceLanguageCode="en", TargetLanguageCode="ja")
        assert req.settings is None

    def test_settings_formality(self):
        req = make_request(
            Text="hi",
            SourceLanguageCode="en",
            TargetLanguageCode="ja",
            Settings={"Formality": "FORMAL"},
        )
        assert req.settings.formality == "FORMAL"

    def test_settings_brevity(self):
        req = make_request(
            Text="hi",
            SourceLanguageCode="en",
            TargetLanguageCode="ja",
            Settings={"Brevity": "ON"},
        )
        assert req.settings.brevity == "ON"

    def test_settings_profanity(self):
        req = make_request(
            Text="hi",
            SourceLanguageCode="en",
            TargetLanguageCode="ja",
            Settings={"Profanity": "MASK"},
        )
        assert req.settings.profanity == "MASK"


class TestGetterMethods:
    def test_get_brevity_none_when_no_settings(self):
        req = make_request(Text="hi", SourceLanguageCode="en", TargetLanguageCode="ja")
        assert req.getBrevity() is None

    def test_get_brevity_none_when_settings_without_brevity(self):
        req = make_request(
            Text="hi",
            SourceLanguageCode="en",
            TargetLanguageCode="ja",
            Settings={"Formality": "FORMAL"},
        )
        assert req.getBrevity() is None

    def test_get_brevity_value_when_set(self):
        req = make_request(
            Text="hi",
            SourceLanguageCode="en",
            TargetLanguageCode="ja",
            Settings={"Brevity": "ON"},
        )
        assert req.getBrevity() == "ON"

    def test_get_formality_none_when_no_settings(self):
        req = make_request(Text="hi", SourceLanguageCode="en", TargetLanguageCode="ja")
        assert req.getFormality() is None

    def test_get_formality_value_when_set(self):
        req = make_request(
            Text="hi",
            SourceLanguageCode="en",
            TargetLanguageCode="ja",
            Settings={"Formality": "INFORMAL"},
        )
        assert req.getFormality() == "INFORMAL"

    def test_get_profanity_none_when_no_settings(self):
        req = make_request(Text="hi", SourceLanguageCode="en", TargetLanguageCode="ja")
        assert req.getProfanity() is None

    def test_get_profanity_value_when_set(self):
        req = make_request(
            Text="hi",
            SourceLanguageCode="en",
            TargetLanguageCode="ja",
            Settings={"Profanity": "MASK"},
        )
        assert req.getProfanity() == "MASK"


class TestTranslateResponseSerialization:
    def test_response_camelcase_output(self):
        resp = TranslateResponse.model_validate(
            {
                "SourceLanguageCode": "ja",
                "TargetLanguageCode": "en",
                "TranslatedText": "hello",
                "AppliedSettings": {},
                "AppliedTerminologies": [],
            }
        )
        data = resp.model_dump(by_alias=True, exclude_none=True)
        assert "TranslatedText" in data
        assert "SourceLanguageCode" in data
        assert "TargetLanguageCode" in data

    def test_translated_document_excluded_when_none(self):
        resp = TranslateResponse.model_validate(
            {
                "SourceLanguageCode": "ja",
                "TargetLanguageCode": "en",
                "TranslatedText": "hello",
                "AppliedSettings": {},
                "AppliedTerminologies": [],
            }
        )
        data = resp.model_dump(by_alias=True, exclude_none=True)
        assert "TranslatedDocument" not in data
