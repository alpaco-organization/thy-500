from typing import Literal
from typing import Optional

from pydantic import BaseModel


class PersonOut(BaseModel):
    personId: Optional[str] = None
    name: str
    x: float
    y: float
    z: float


class PersonSearchOut(BaseModel):
    personId: Optional[str] = None
    name: str
    x: float
    y: float
    z: float


SearchType = Literal["identity", "fullName"]
