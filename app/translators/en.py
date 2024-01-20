import re
import pykakasi

kks = pykakasi.kakasi()

def to_romaji_line(text: str) -> str:
    items = kks.convert(text)
    terms = list(map(lambda item: item['hepburn'], items))
    return ' '.join(terms)

def to_romaji(text: str) -> str:
    lines = text.split("\n")
    items = [to_romaji_line(line) for line in lines]
    return "\n".join(items)

def en_translator(text: str, content_type: str) -> str:
    # Convert Japanese to Romaji
    if content_type == "text/html":
        data = re.findall(r"<[^>]*>|[^<>]+", text)
        converted = map(lambda t: to_romaji(t) if t[0] != "<" else t , data)
        return "".join(converted)
    else:
        return to_romaji(text)
