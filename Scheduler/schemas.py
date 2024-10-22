from typing import List, Union
from pydantic import BaseModel

class EventBase(BaseModel):
    name: str
    date: str
    area: str


class Event(EventBase):
    id: int
    class Config:
        orm_mode = True