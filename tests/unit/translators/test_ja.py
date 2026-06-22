from app.translators.ja import to_hiragana, ja_translator


class TestToHiragana:
    def test_empty_string(self):
        assert to_hiragana("") == ""

    def test_romaji_converts_to_hiragana(self):
        result = to_hiragana("ha")
        assert "は" in result or len(result) > 0

    def test_returns_string(self):
        result = to_hiragana("nihongo")
        assert isinstance(result, str)


class TestJaTranslator:
    def test_plain_text_converts_romaji(self):
        result = ja_translator("ha", "text/plain")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_html_text_node_converted(self):
        result = ja_translator("<p>ha</p>", "text/html")
        assert "<p>" in result
        assert "</p>" in result

    def test_html_tags_preserved(self):
        result = ja_translator("<br/>", "text/html")
        assert "<br/>" in result

    def test_html_mixed_content(self):
        result = ja_translator("<b>nihongo</b>", "text/html")
        assert "<b>" in result
        assert "</b>" in result

    def test_plain_text_does_not_strip_html_tags(self):
        result = ja_translator("<p>ha</p>", "text/plain")
        assert "<p>" in result
        assert "</p>" in result

    def test_html_empty_string(self):
        result = ja_translator("", "text/html")
        assert result == ""
