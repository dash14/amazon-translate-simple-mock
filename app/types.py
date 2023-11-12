from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Optional
from inflection import camelize

class AmazonBaseModel(BaseModel):
    model_config = ConfigDict(alias_generator=camelize)

class TranslateDocument(AmazonBaseModel):
    content: str
    content_type: str


class TranslateSettings(AmazonBaseModel):
    brevity: Optional[str] = None
    formality: Optional[str] = None
    profanity: Optional[str] = None

class TranslateRequest(AmazonBaseModel):
    settings: Optional[TranslateSettings] = None
    source_language_code: str
    target_language_code: str
    terminology_names: list[str] = Field(default_factory=list)
    text: Optional[str] = None
    document: Optional[TranslateDocument] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "Settings": {
                        "Profanity": "MASK",
                        "Formality": "FORMAL"
                    },
                    "SourceLanguageCode": "auto",
                    "TargetLanguageCode": "en",
                    "TerminologyNames": [],
                    "Document": {
                        "Content": "5piO5pel44Gu5aSp5rCX44Gv5pm044KM44Gn44GZ44CC",
                        "ContentType": "text/html"
                    }
                }
            ]
        }
    }

    def getBrevity(self) -> str:
        if not self.settings or not self.settings.brevity:
            return None
        else:
            return self.settings.brevity

    def getFormality(self) -> str:
        if not self.settings or not self.settings.formality:
            return None
        else:
            return self.settings.formality

    def getProfanity(self) -> str:
        if not self.settings or not self.settings.profanity:
            return None
        else:
            return self.settings.profanity

    @model_validator(mode='after')
    def check_text_or_document(self) -> 'TranslateRequest':
        if not self.text and not self.document:
            raise ValueError('Either Text or Document is required')
        if self.text and self.document:
            raise ValueError('Cannot specify both Text and Document')

        return self

class TranslatedTerminology(AmazonBaseModel):
    source_text: str
    target_text: str

class Terminology(AmazonBaseModel):
    name: str
    terms: list[TranslatedTerminology] = Field(default_factory=list)

class TranslatedDocument(AmazonBaseModel):
    content: str

class TranslateResponse(AmazonBaseModel):
    applied_settings: TranslateSettings
    applied_terminologies: list[Terminology] = Field(default_factory=list)
    source_language_code: str
    target_language_code: str
    translated_document: Optional[TranslatedDocument] = None
    translated_text: Optional[str] = None
