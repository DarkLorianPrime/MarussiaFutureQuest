from typing import Callable, Type

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from os import getenv

from starlette.requests import Request

from models import get_session, create_database
from service import Service
from utils.pydantic import Body, Parameters
from utils.states import State

__app = FastAPI(
    on_startup=[create_database],
    middleware=[Middleware(CORSMiddleware,
                           allow_credentials=True,
                           allow_methods=["*"],
                           allow_headers=["*"],
                           allow_origins=["*"], )
                ])


def listener(state_class: Type[State] = None) -> Callable:
    def decorator(fn: Callable = None):
        @__app.post(f'/{getenv("URL", "webhook")}')
        async def wrapper(request: Request,
                          session: AsyncSession = Depends(get_session),
                          service: Service = Depends(Service)):
            body: Body = Body(**await request.json())
            params = {"body": body,
                      "session": session,
                      "state": None,
                      "service": service,
                      "user": await service.get_user(body.session.user_id)}

            if state_class:
                params["state"]: State = state_class(body.session.user_id)

            return await fn(Parameters(**params))

        return wrapper if fn is not None else __app

    return decorator
