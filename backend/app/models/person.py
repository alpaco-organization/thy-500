from typing import Literal
from typing import Optional

from pydantic import BaseModel


class PersonOut(BaseModel):
    personId: Optional[str] = None
    name: str
    grid_filename: Optional[str] = None
    row: Optional[int] = None
    column: Optional[int] = None
    x: float
    y: float
    z: float
    matchCorrect: Optional[bool] = None
    feedback: Optional[str] = None


class PersonSearchOut(BaseModel):
    personId: Optional[str] = None
    name: str
    grid_filename: Optional[str] = None
    row: Optional[int] = None
    column: Optional[int] = None
    x: float
    y: float
    z: float
    matchCorrect: Optional[bool] = None
    feedback: Optional[str] = None


SearchType = Literal["identity", "fullName"]