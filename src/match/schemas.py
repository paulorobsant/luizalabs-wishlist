from typing import Any, List

from pydantic import BaseModel


# Match Request

class MatchMyConnection(BaseModel):
    data: Any

    class Config:
        orm_mode = True


class MatchMyConnections(BaseModel):
    next_connections: List[MatchMyConnection]
    past_connections: List[MatchMyConnection]


class MatchRequestCreate(BaseModel):
    user_id: str
    description: str
    keyword: str


class MatchRequestUpdate(BaseModel):
    id: Any
    user_id: Any
    data: Any = None
    status: str = None
    priority: int = None


class MatchRequestRead(BaseModel):
    id: Any
    user_id: Any
    data: Any = None
    status: str
    priority: int

    class Config:
        orm_mode = True


class MatchRequestInDB(BaseModel):
    user_id: Any
    data: dict
    status: Any
    priority: int = None


# Match

class MatchInDB(BaseModel):
    mentor_id: Any
    learner_id: Any
    start_datetime: Any
    end_datetime: Any
    status: Any
    current_step: Any
    data: Any
    is_approved: bool


class MatchUpdate(BaseModel):
    is_approved: bool = None


class MatchScheduleCreate(BaseModel):
    datetime: str
    duration: str


class MatchReplaceGuest(BaseModel):
    old_guest_id: Any
    new_guest_id: Any


# Match Term


class MatchTerm(BaseModel):
    label: str = None
    value: int = None
    is_approved: bool = None


class MatchTermCreate(MatchTerm):
    label: str
    is_approved: bool


class MatchTermRead(MatchTerm):
    label: str
    is_approved: bool


class MatchTermUpdate(MatchTerm):
    label: str = None
    is_approved: bool = None
