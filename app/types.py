from pydantic import BaseModel, Field
from typing import Optional

class Document(BaseModel):
    Content: str
    ContentType: str

class TranslateSettings(BaseModel):
    Formality: Optional[str] = None
    Profanity: Optional[str] = None

class TranslateDocumentRequest(BaseModel):
    Document: Document
    Settings: Optional[TranslateSettings] = None
    SourceLanguageCode: str
    TargetLanguageCode: str
    TerminologyNames: list[str] = Field(default_factory=list)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "Document": {
                        "Content": "5piO5pel44Gu5aSp5rCX44Gv5pm044KM44Gn44GZ44CC",
                        "ContentType": "text/html"
                    },
                    "Settings": {
                        "Profanity": "MASK",
                        "Formality": "FORMAL"
                    },
                    "SourceLanguageCode": "auto",
                    "TargetLanguageCode": "en",
                    "TerminologyNames": []
                }
            ]
        }
    }

    def getFormality(self) -> str:
        if not self.Settings or not self.Settings.Formality:
            return "FORMAL"
        else:
            return self.Settings.Formality

    def getProfanity(self) -> str:
        if not self.Settings or not self.Settings.Profanity:
            return None
        else:
            return self.Settings.Profanity

class TranslatedTerminology(BaseModel):
    SourceText: str
    TargetText: str

class Terminology(BaseModel):
    Name: str
    Terms: list[TranslatedTerminology] = Field(default_factory=list)

class TranslatedDocument(BaseModel):
    Content: str

class TranslateDocumentResponse(BaseModel):
    AppliedSettings: TranslateSettings
    AppliedTerminologies: list[Terminology] = Field(default_factory=list)
    SourceLanguageCode: str
    TargetLanguageCode: str
    TranslatedDocument: TranslatedDocument
