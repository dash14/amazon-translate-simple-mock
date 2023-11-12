from pydantic import BaseModel, Field
from typing import Optional

class Document(BaseModel):
    Content: str
    ContentType: str

class Settings(BaseModel):
    Formality: str
    Profanity: str

class TranslateDocumentRequest(BaseModel):
    Document: Document
    Settings: Optional[Settings] = None
    SourceLanguageCode: str
    TargetLanguageCode: str
    TerminologyNames: Optional[list[str]] = None

class TranslatedTerminology(BaseModel):
    SourceText: str
    TargetText: str

class Terminology(BaseModel):
    Name: str
    Terms: list[TranslatedTerminology] = Field(default_factory=list)

class TranslatedDocument(BaseModel):
    Content: str

class TranslateDocumentResponse(BaseModel):
    AppliedSettings: Settings
    AppliedTerminologies: list[Terminology] = Field(default_factory=list)
    SourceLanguageCode: str
    TargetLanguageCode: str
    TranslatedDocument: TranslatedDocument
