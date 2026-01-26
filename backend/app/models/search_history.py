from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class SearchHistoryOut(BaseModel):
    searchId: Optional[str] = None
    searchType: str  # "identity" or "fullName"
    query: str
    personId: Optional[str] = None  # If search was successful
    personName: Optional[str] = None  # If search was successful
    found: bool  # Whether the search found a result
    createdAt: datetime


class SearchHistoryCreate(BaseModel):
    searchType: str
    query: str
    personId: Optional[str] = None
    personName: Optional[str] = None
    found: bool
