import re
import pykakasi

kks = pykakasi.kakasi()

def to_romaji(text: str) -> str:
    items = kks.convert(text)
    terms = list(map(lambda item: item['hepburn'], items))
    return ' '.join(terms)

def en_translator(text: str, content_type: str) -> str:
    # 日本語をローマ字に変換する
    if content_type == "text/html":
        data = re.findall(r"<[^>]*>|[^<>]+", text)
        converted = map(lambda t: to_romaji(t) if t[0] != "<" else t , data)
        return "".join(converted)
    else:
        return to_romaji(text)
