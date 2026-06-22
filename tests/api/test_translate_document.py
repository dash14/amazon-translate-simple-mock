import base64


class TestBasicDocumentTranslation:
    def test_ja_to_en_returns_200(self, post, doc_payload):
        response = post(doc_payload("<p>日本語テキスト</p>", source="ja", target="en"))
        assert response.status_code == 200

    def test_en_to_ja_returns_200(self, post, doc_payload):
        response = post(doc_payload("<p>nihongo</p>", source="en", target="ja"))
        assert response.status_code == 200

    def test_has_translated_document(self, post, doc_payload):
        response = post(doc_payload("<p>日本語</p>", source="ja", target="en"))
        assert "TranslatedDocument" in response.json()

    def test_no_translated_text_in_document_response(self, post, doc_payload):
        response = post(doc_payload("<p>日本語</p>", source="ja", target="en"))
        assert "TranslatedText" not in response.json()

    def test_translated_content_is_base64_decodable(self, post, doc_payload):
        response = post(doc_payload("<p>日本語</p>", source="ja", target="en"))
        content = response.json()["TranslatedDocument"]["Content"]
        decoded = base64.b64decode(content)
        assert len(decoded) > 0

    def test_html_tags_preserved_in_translation(self, post, doc_payload):
        response = post(doc_payload("<p>日本語</p>", source="ja", target="en"))
        content = response.json()["TranslatedDocument"]["Content"]
        decoded = base64.b64decode(content).decode("utf-8")
        assert "<p>" in decoded
        assert "</p>" in decoded

    def test_plain_text_document(self, post, doc_payload):
        response = post(doc_payload("日本語", content_type="text/plain", source="ja", target="en"))
        assert response.status_code == 200
        content = response.json()["TranslatedDocument"]["Content"]
        decoded = base64.b64decode(content).decode("utf-8")
        assert "日本語" not in decoded


class TestDocumentResponseStructure:
    def test_has_source_language_code(self, post, doc_payload):
        response = post(doc_payload("<p>test</p>", source="ja", target="en"))
        assert "SourceLanguageCode" in response.json()

    def test_has_target_language_code(self, post, doc_payload):
        response = post(doc_payload("<p>test</p>", source="ja", target="en"))
        assert "TargetLanguageCode" in response.json()

    def test_has_applied_settings(self, post, doc_payload):
        response = post(doc_payload("<p>test</p>", source="ja", target="en"))
        assert "AppliedSettings" in response.json()

    def test_brevity_not_in_document_applied_settings(self, post, doc_payload):
        response = post(doc_payload("<p>test</p>", source="ja", target="en"))
        applied = response.json()["AppliedSettings"]
        assert "Brevity" not in applied

    def test_formality_reflected_in_document(self, post, doc_payload):
        payload = doc_payload("<p>test</p>", source="ja", target="en")
        payload["Settings"] = {"Formality": "FORMAL"}
        response = post(payload)
        assert response.json()["AppliedSettings"]["Formality"] == "FORMAL"
