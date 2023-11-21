import re
from pyokaka import okaka

def to_hiragana(text: str) -> str:
    return okaka.convert(text)

def ja_translator(text: str, content_type: str) -> str:
    # Convert Romaji to Hiragana
    if content_type == "text/html":
        data = re.findall(r"<[^>]*>|[^<>]+", text)
        converted = map(lambda t: to_hiragana(t) if t[0] != "<" else t , data)
        return "".join(converted)
    else:
        return to_hiragana(text)
