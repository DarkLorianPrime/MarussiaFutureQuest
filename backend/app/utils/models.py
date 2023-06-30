from typing import Any

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from service import Service
from utils.states import State as StateClass


class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True


class NLU(BaseModel):
    tokens: list
    entities: list


class Interfaces(BaseModel):
    screen: dict


class Meta(BaseModel):
    client_id: str
    locale: str
    timezone: str
    interfaces: Interfaces
    _city_ru: str


class Request(BaseModel):
    command: str
    original_utterance: str
    type: str
    nlu: NLU


class Application(BaseModel):
    application_id: str
    application_type: str


class User(BaseModel):
    user_id: str


class Session(BaseModel):
    session_id: str
    user_id: str
    skill_id: str
    new: bool
    message_id: int
    application: Application
    auth_token: str
    user: User


class State(BaseModel):
    session: dict
    user: dict


class Body(BaseModel):
    meta: Meta
    request: Request
    session: Session
    state: State
    version: str


class Parameters(BaseModel):
    body: Body
    session: AsyncSession
    service: Service
    state: StateClass | None
    user: Any
