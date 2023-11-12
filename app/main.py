import re
from base64 import b64decode, b64encode

from fastapi.responses import JSONResponse
from .init import init_fast_api
from .errors import error_responses
from .translators.en import en_translator
from .translators.ja import ja_translator
from .types import Settings, TranslatedDocument, TranslateDocumentRequest, TranslateDocumentResponse

app = init_fast_api()

translators = {
    "en": en_translator,
    "ja": ja_translator
}

@app.post("/")
async def translate(request: TranslateDocumentRequest) -> TranslateDocumentResponse:
    content = b64decode(request.Document.Content).decode('utf-8')

    if request.SourceLanguageCode == "auto":
        if re.match(r'\A[\x00-\x7F]+\Z', content):
            # すべて ASCII コード: 英語として判定する
            source_lang = "en"
        else:
            source_lang = "ja"
    else:
        source_lang = request.SourceLanguageCode

    target_lang = request.TargetLanguageCode

    if not(source_lang == "en" or source_lang == "ja") \
        or not(target_lang == "en" or target_lang == "ja"):
        return JSONResponse(
            content={
                "__type": "UnsupportedLanguagePairException",
                "message": "Amazon Translate does not support translation from the language of the source text into the requested target language"
            },
            status_code=400,
            media_type="application/x-amz-json-1.1"
        ),

    # エラー返却リクエストの判定
    for [key, error] in error_responses.items():
        # 本文中にエラー文字列があればエラーにする
        if key in content:
            return error

    if source_lang != target_lang:
        # 変換する
        converted = translators[target_lang](content, request.Document.ContentType)
    else:
        # 原文のままにする
        converted = content

    converted = b64encode(converted.encode("utf-8"))

    return TranslateDocumentResponse(
        AppliedSettings=Settings(Formality="FORMAL", Profanity=""),
        SourceLanguageCode=source_lang,
        TargetLanguageCode=target_lang,
        TranslatedDocument=TranslatedDocument(Content=converted)
    )
