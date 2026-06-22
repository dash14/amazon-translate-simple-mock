AMZ = "application/x-amz-json-1.1"


class TestSupportedPairs:
    def test_ja_to_en(self, post, text_payload):
        response = post(text_payload("日本語テキスト", source="ja", target="en"))
        assert response.status_code == 200

    def test_en_to_ja(self, post, text_payload):
        response = post(text_payload("hello", source="en", target="ja"))
        assert response.status_code == 200

    def test_auto_to_en_with_japanese(self, post, text_payload):
        response = post(text_payload("日本語", source="auto", target="en"))
        assert response.status_code == 200

    def test_auto_to_en_with_ascii(self, post, text_payload):
        response = post(text_payload("hello", source="auto", target="en"))
        assert response.status_code == 200

    def test_auto_to_ja(self, post, text_payload):
        response = post(text_payload("hello", source="auto", target="ja"))
        assert response.status_code == 200

    def test_other_lang_pair_passthrough(self, post, text_payload):
        response = post(text_payload("bonjour", source="fr", target="ko"))
        assert response.status_code == 200
        assert response.json()["TranslatedText"] == "bonjour"


class TestAutoSourceDetection:
    def test_auto_japanese_text_source_becomes_ja(self, post, text_payload):
        response = post(text_payload("日本語テスト", source="auto", target="en"))
        assert response.status_code == 200
        assert response.json()["SourceLanguageCode"] == "ja"

    def test_auto_ascii_text_source_becomes_en(self, post, text_payload):
        response = post(text_payload("hello world", source="auto", target="ja"))
        assert response.status_code == 200
        assert response.json()["SourceLanguageCode"] == "en"

    def test_auto_mixed_text_source_becomes_ja(self, post, text_payload):
        response = post(text_payload("hello 日本語", source="auto", target="en"))
        assert response.status_code == 200
        assert response.json()["SourceLanguageCode"] == "ja"


class TestUnsupportedPairs:
    def test_unknown_source_language(self, post, text_payload):
        response = post(text_payload("hello", source="xx", target="en"))
        assert response.status_code == 400

    def test_unknown_target_language(self, post, text_payload):
        response = post(text_payload("hello", source="en", target="xx"))
        assert response.status_code == 400

    def test_unsupported_pair_type_field(self, post, text_payload):
        response = post(text_payload("hello", source="xx", target="en"))
        assert response.json()["__type"] == "UnsupportedLanguagePairException"

    def test_unsupported_pair_message_field(self, post, text_payload):
        response = post(text_payload("hello", source="xx", target="en"))
        assert "message" in response.json()

    def test_unsupported_pair_content_type(self, post, text_payload):
        response = post(text_payload("hello", source="xx", target="en"))
        assert AMZ in response.headers["content-type"]

    def test_auto_as_target_is_unsupported(self, post, text_payload):
        response = post(text_payload("hello", source="en", target="auto"))
        assert response.status_code == 400
