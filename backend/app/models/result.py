from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ResultOut(BaseModel):
    resultId: Optional[str] = None
    personId: str
    personName: str
    feedback: Optional[str] = None
    createdAt: datetime


class ResultCreate(BaseModel):
    personId: str
    personName: str
    feedback: Optional[str] = None  