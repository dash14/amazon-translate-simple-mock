from app.translators.en import en_translator, to_romaji, to_romaji_line


class TestToRomajiLine:
    def test_empty_string(self):
        assert to_romaji_line("") == ""

    def test_ascii_passthrough(self):
        result = to_romaji_line("hello")
        assert "hello" in result

    def test_japanese_converts(self):
        result = to_romaji_line("日本語")
        assert result != "日本語"
        assert len(result) > 0

    def test_punctuation_no_leading_space(self):
        result = to_romaji_line("晴れです。")
        assert not result.startswith(" ")
        assert "." in result or result != ""

    def test_comma_no_leading_space(self):
        result = to_romaji_line("はれ、晴れ")
        assert ",," not in result


class TestToRomaji:
    def test_multiline_preserves_newlines(self):
        result = to_romaji("日本語\n日本語")
        assert "\n" in result

    def test_empty_string(self):
        assert to_romaji("") == ""

    def test_single_line(self):
        result = to_romaji("明日")
        assert isinstance(result, str)
        assert len(result) > 0


class TestEnTranslator:
    def test_plain_text_converts_japanese(self):
        result = en_translator("日本語", "text/plain")
        assert result != "日本語"
        assert len(result) > 0

    def test_plain_text_ascii_passthrough(self):
        result = en_translator("hello", "text/plain")
        assert "hello" in result

    def test_html_text_node_converted(self):
        result = en_translator("<p>日本語</p>", "text/html")
        assert "<p>" in result
        assert "</p>" in result
        assert "日本語" not in result

    def test_html_tags_preserved(self):
        result = en_translator("<br/>", "text/html")
        assert "<br/>" in result

    def test_html_mixed_content(self):
        result = en_translator("<b>太字</b>テキスト", "text/html")
        assert "<b>" in result
        assert "</b>" in result
        assert "太字" not in result

    def test_plain_text_does_not_strip_html_tags(self):
        result = en_translator("<p>test</p>", "text/plain")
        assert "<p>" in result
        assert "</p>" in result

    def test_html_empty_string(self):
        result = en_translator("", "text/html")
        assert result == ""

    def test_html_nested_tags(self):
        result = en_translator("<div><p>明日</p></div>", "text/html")
        assert "<div>" in result
        assert "<p>" in result
        assert "明日" not in result
