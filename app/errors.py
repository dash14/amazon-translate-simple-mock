from fastapi.responses import JSONResponse

error_responses: dict[str, JSONResponse] = {
    "ThrottlingException": JSONResponse(
        content={"__type": "ThrottlingException", "message": "Rate exceeded"},
        status_code=429,
        media_type="application/x-amz-json-1.1"
    ),
    "InternalServerException": JSONResponse(
        content={"__type": "InternalServerException", "message": "An internal server error occurred"},
        status_code=500,
        media_type="application/x-amz-json-1.1"
    ),
    "LimitExceededException": JSONResponse(
        content={"__type": "LimitExceededException", "message": "The specified limit has been exceeded"},
        status_code=400,
        media_type="application/x-amz-json-1.1"
    ),
    "ServiceUnavailableException": JSONResponse(
        content={"__type": "ServiceUnavailableException", "message": "The Amazon Translate service is temporarily unavailable"},
        status_code=500,
        media_type="application/x-amz-json-1.1"
    ),
    "TooManyRequestsException": JSONResponse(
        content={"__type": "TooManyRequestsException", "message": "You have made too many requests within a short period of time"},
        status_code=400,
        media_type="application/x-amz-json-1.1"
    ),
    "UnsupportedLanguagePairException": JSONResponse(
        content={
            "__type": "UnsupportedLanguagePairException",
            "message": "Amazon Translate does not support translation from the language of the source text into the requested target language"
        },
        status_code=400,
        media_type="application/x-amz-json-1.1"
    )
}
