import json
import re
from base64 import b64decode, b64encode

from fastapi.responses import JSONResponse
from .init import init_fast_api
from .errors import error_responses
from .translators.en import en_translator
from .translators.ja import ja_translator
from .types import TranslateRequest, TranslateResponse
from .definitions import SUPPORT_LANGUAGES

app = init_fast_api()

translators = {
    "en": en_translator,
    "ja": ja_translator
}

@app.post("/", response_model_by_alias=True, response_model_exclude_none=True)
async def translate(request: TranslateRequest) -> TranslateResponse:

    if request.text:
        content = request.text
        content_type = "text/plain"
    else: # if request.document:
        content = b64decode(request.document.content).decode("utf-8")
        content_type = request.document.content_type

    if request.source_language_code == "auto":
        if re.match(r"\A[\x00-\x7F]+\Z", content):
            # すべて ASCII コード: 英語として判定する
            source_lang = "en"
        else:
            source_lang = "ja"
    else:
        source_lang = request.source_language_code

    target_lang = request.target_language_code

    lang_codes = list(SUPPORT_LANGUAGES.values())

    if source_lang not in lang_codes or target_lang not in lang_codes:
        return JSONResponse(
            content={
                "__type": "UnsupportedLanguagePairException",
                "message": "Amazon Translate does not support translation from the language of the source text into the requested target language"
            },
            status_code=400,
            media_type="application/x-amz-json-1.1"
        )

    # エラー返却リクエストの判定
    for [key, error] in error_responses.items():
        # 本文中にエラー文字列があればエラーにする
        if key in content:
            return error

    if "EchoRequestBody" in content \
        or source_lang not in ["ja", "en", "auto"] \
        or target_lang not in ["ja", "en"]:
        converted = json.dumps(request.model_dump(by_alias=True, exclude_none=True), indent=2)
    elif source_lang != target_lang:
        # 変換する
        converted = translators[target_lang](content, content_type)
    else:
        # 原文のままにする
        converted = content

    if request.text:
        return TranslateResponse(**{
            "SourceLanguageCode": source_lang,
            "TargetLanguageCode": target_lang,
            "AppliedSettings": {
                "Brevity": request.getBrevity(),
                "Formality": request.getFormality(),
                "Profanity": request.getProfanity()
            },
            "AppliedTerminologies": map(lambda t: { "Name": t }, request.terminology_names),
            "TranslatedText": converted,
        })

    else: # if request.document:
        converted = b64encode(converted.encode("utf-8"))

        return TranslateResponse(**{
            "SourceLanguageCode": source_lang,
            "TargetLanguageCode": target_lang,
            "AppliedSettings": {
                "Formality": request.getFormality(),
                "Profanity": request.getProfanity()
            },
            "AppliedTerminologies": map(lambda t: { "Name": t }, request.terminology_names),
            "TranslatedDocument": { "Content": converted },
        })
