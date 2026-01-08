from typing import Literal

from pydantic import BaseModel


class PersonOut(BaseModel):
    personId: str
    name: str
    x: float
    y: float


class PersonSearchOut(BaseModel):
    name: str
    x: float
    y: float
    url: str


SearchType = Literal["identity", "fullName"]
