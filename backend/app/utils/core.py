from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from os import getenv

from starlette.requests import Request

from models import get_session
from service import Service
from utils.models import Body, Parameters

__app = FastAPI(
    middleware=[Middleware(CORSMiddleware,
                           allow_credentials=True,
                           allow_methods=["*"],
                           allow_headers=["*"],
                           allow_origins=["*"], )
                ])


def listener(state_class=None):

    def decorator(fn=None):
        @__app.post(f'/{getenv("URL", "webhook")}')
        async def wrapper(request: Request,
                          session: AsyncSession = Depends(get_session),
                          service: Service = Depends(Service)):
            body = Body(**await request.json())
            params = {"body": body,
                      "session": session,
                      "state": None,
                      "service": service,
                      "user": await service.get_user(body.session.user_id)}

            if state_class:
                params["state"] = state_class(body.session.user_id)

            return await fn(Parameters(**params))

        return wrapper if fn is not None else __app

    return decorator
