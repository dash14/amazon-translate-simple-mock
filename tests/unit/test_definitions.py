from app.definitions import SUPPORT_LANGUAGES


def test_support_languages_count():
    assert len(SUPPORT_LANGUAGES) == 75


def test_required_languages_present():
    codes = list(SUPPORT_LANGUAGES.values())
    for lang in ["ja", "en", "zh", "ko", "fr", "de", "ar"]:
        assert lang in codes, f"Expected language code '{lang}' not found"


def test_auto_not_in_lang_codes():
    codes = list(SUPPORT_LANGUAGES.values())
    assert "auto" not in codes


def test_lang_codes_are_strings():
    for code in SUPPORT_LANGUAGES.values():
        assert isinstance(code, str)


def test_lang_codes_are_unique():
    codes = list(SUPPORT_LANGUAGES.values())
    assert len(codes) == len(set(codes))


def test_lang_names_are_non_empty():
    for name in SUPPORT_LANGUAGES.keys():
        assert isinstance(name, str) and len(name) > 0
