import re
import pykakasi
from functools import reduce

kks = pykakasi.kakasi()

def space_appender(cum, term) -> str:
    if not term:
        return cum
    if len(cum) == 0:
        return [term]
    if re.search(r'\A[\.,?!]\Z', term):
        return [*cum, term]
    else: # with symbol
        return [*cum, ' ', term]

def to_romaji_line(text: str) -> str:
    items = kks.convert(text)
    terms = list(map(lambda item: str.strip(item['hepburn']), items))
    texts = reduce(space_appender, terms, [])
    return ''.join(texts)

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
