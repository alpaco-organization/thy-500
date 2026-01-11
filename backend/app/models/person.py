from typing import Literal
from typing import Optional

from pydantic import BaseModel


class PersonOut(BaseModel):
    personId: str
    name: str
    grid_filename: Optional[str] = None
    row: Optional[int] = None
    column: Optional[int] = None
    x: float
    y: float


class PersonSearchOut(BaseModel):
    personId: str
    name: str
    grid_filename: Optional[str] = None
    row: Optional[int] = None
    column: Optional[int] = None
    x: float
    y: float
    url: str


SearchType = Literal["identity", "fullName"]
