AMZ = "application/x-amz-json-1.1"


class TestBasicTranslation:
    def test_ja_to_en_returns_200(self, post, text_payload):
        response = post(text_payload("日本語テキスト", source="ja", target="en"))
        assert response.status_code == 200

    def test_ja_to_en_returns_translated_text(self, post, text_payload):
        response = post(text_payload("日本語テキスト", source="ja", target="en"))
        assert response.json()["TranslatedText"] != ""

    def test_en_to_ja_returns_200(self, post, text_payload):
        response = post(text_payload("hello", source="en", target="ja"))
        assert response.status_code == 200

    def test_en_to_ja_returns_translated_text(self, post, text_payload):
        response = post(text_payload("nihongo", source="en", target="ja"))
        result = response.json()["TranslatedText"]
        assert isinstance(result, str)
        assert len(result) > 0

    def test_same_language_returns_original(self, post, text_payload):
        response = post(text_payload("日本語", source="ja", target="ja"))
        assert response.status_code == 200
        assert response.json()["TranslatedText"] == "日本語"

    def test_unsupported_pair_returns_original(self, post, text_payload):
        response = post(text_payload("bonjour", source="fr", target="de"))
        assert response.status_code == 200
        assert response.json()["TranslatedText"] == "bonjour"

    def test_ja_to_fr_returns_original(self, post, text_payload):
        response = post(text_payload("日本語", source="ja", target="fr"))
        assert response.status_code == 200
        assert response.json()["TranslatedText"] == "日本語"


class TestResponseStructure:
    def test_has_translated_text(self, post, text_payload):
        response = post(text_payload("hello", source="en", target="ja"))
        assert "TranslatedText" in response.json()

    def test_has_source_language_code(self, post, text_payload):
        response = post(text_payload("hello", source="en", target="ja"))
        assert "SourceLanguageCode" in response.json()

    def test_has_target_language_code(self, post, text_payload):
        response = post(text_payload("hello", source="en", target="ja"))
        assert "TargetLanguageCode" in response.json()

    def test_has_applied_settings(self, post, text_payload):
        response = post(text_payload("hello", source="en", target="ja"))
        assert "AppliedSettings" in response.json()

    def test_has_applied_terminologies(self, post, text_payload):
        response = post(text_payload("hello", source="en", target="ja"))
        assert "AppliedTerminologies" in response.json()

    def test_no_translated_document_in_text_response(self, post, text_payload):
        response = post(text_payload("hello", source="en", target="ja"))
        assert "TranslatedDocument" not in response.json()

    def test_source_language_code_value(self, post, text_payload):
        response = post(text_payload("hello", source="en", target="ja"))
        assert response.json()["SourceLanguageCode"] == "en"

    def test_target_language_code_value(self, post, text_payload):
        response = post(text_payload("hello", source="en", target="ja"))
        assert response.json()["TargetLanguageCode"] == "ja"

    def test_response_content_type_amz(self, post, text_payload):
        response = post(text_payload("hello", source="en", target="ja"))
        assert AMZ in response.headers["content-type"]


class TestSettings:
    def test_formality_formal_reflected(self, post, text_payload):
        response = post(
            text_payload(
                "hello", source="en", target="ja", settings={"Formality": "FORMAL"}
            )
        )
        assert response.json()["AppliedSettings"]["Formality"] == "FORMAL"

    def test_formality_informal_reflected(self, post, text_payload):
        response = post(
            text_payload(
                "hello", source="en", target="ja", settings={"Formality": "INFORMAL"}
            )
        )
        assert response.json()["AppliedSettings"]["Formality"] == "INFORMAL"

    def test_profanity_mask_reflected(self, post, text_payload):
        response = post(
            text_payload(
                "hello", source="en", target="ja", settings={"Profanity": "MASK"}
            )
        )
        assert response.json()["AppliedSettings"]["Profanity"] == "MASK"

    def test_brevity_on_reflected(self, post, text_payload):
        response = post(
            text_payload("hello", source="en", target="ja", settings={"Brevity": "ON"})
        )
        assert response.json()["AppliedSettings"]["Brevity"] == "ON"

    def test_no_settings_applied_settings_keys_absent(self, post, text_payload):
        response = post(text_payload("hello", source="en", target="ja"))
        applied = response.json()["AppliedSettings"]
        assert "Formality" not in applied
        assert "Profanity" not in applied
        assert "Brevity" not in applied


class TestTerminologyNames:
    def test_single_terminology_in_response(self, post, text_payload):
        response = post(
            text_payload(
                "hello", source="en", target="ja", terminology_names=["custom"]
            )
        )
        terminologies = response.json()["AppliedTerminologies"]
        assert len(terminologies) == 1
        assert terminologies[0]["Name"] == "custom"

    def test_multiple_terminologies_in_response(self, post, text_payload):
        response = post(
            text_payload(
                "hello", source="en", target="ja", terminology_names=["t1", "t2"]
            )
        )
        terminologies = response.json()["AppliedTerminologies"]
        names = [t["Name"] for t in terminologies]
        assert "t1" in names
        assert "t2" in names

    def test_empty_terminology_names(self, post, text_payload):
        response = post(
            text_payload("hello", source="en", target="ja", terminology_names=[])
        )
        assert response.json()["AppliedTerminologies"] == []

    def test_no_terminology_names_field(self, post, text_payload):
        response = post(text_payload("hello", source="en", target="ja"))
        assert response.json()["AppliedTerminologies"] == []
