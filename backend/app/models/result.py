from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ResultOut(BaseModel):
    resultId: Optional[str] = None
    personId: str
    personName: str
    matchCorrect: bool
    feedback: Optional[str] = None
    createdAt: datetime
    updatedAt: Optional[datetime] = None


class ResultCreate(BaseModel):
    personId: str
    personName: str
    matchCorrect: bool


class MatchCorrectUpdate(BaseModel):
    matchCorrect: bool


class FeedbackUpdate(BaseModel):
    feedback: str