import re
import asyncio
from base64 import b64decode, b64encode

from fastapi.responses import JSONResponse
from fastapi import Request
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
async def translate(request: TranslateRequest, raw_request: Request) -> TranslateResponse:

    if request.text:
        content = request.text
        content_type = "text/plain"
    else: # if request.document:
        content = b64decode(request.document.content).decode("utf-8")
        content_type = request.document.content_type

    m = re.search("@return(?:\\s|&nbsp;)+SourceLanguageCode(?:\\s|&nbsp;)+(\\w+)", content)
    if m:
        source_lang = m.group(1)
    elif request.source_language_code == "auto":
        if re.match(r"\A[\x00-\x7F]+\Z", content):
            # All are ASCII codes -> Judge as English
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

    # @sleep SECONDS
    m = re.search(r"@sleep(?:\s|&nbsp;)+(\d+(?:\.\d+)?)", content)
    if m:
        sleep_sec = float(m.group(1))
        await asyncio.sleep(sleep_sec)

    # @raise EXCEPTIONS
    for [key, error] in error_responses.items():
        # If the error name is included in the content, raise the error.
        if re.search(f"@raise(?:\\s|&nbsp;)+{key}", content):
            return error

    if re.search(f"@return(?:\\s|&nbsp;)+RequestedBody", content):
        # @return RequestedBody
        # Returns the requested body as-is as a translation result.
        body = (await raw_request.body()).decode('utf-8')
        converted = body
    elif source_lang == target_lang \
        or source_lang not in ["ja", "en", "auto"] \
        or target_lang not in ["ja", "en"]:
        converted = content
    else: # source_lang != target_lang:
        converted = translators[target_lang](content, content_type)

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
