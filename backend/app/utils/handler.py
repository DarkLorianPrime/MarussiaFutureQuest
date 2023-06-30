from typing import Iterable

from utils.config import commands, states
from utils.models import Parameters
from utils.responses import Response
from utils.states import StateField, global_state


def message_handler(commands_list: Iterable = None, state: StateField = None):
    def decorator(fn):
        if commands_list is not None:
            commands[tuple(commands_list)] = fn

        if state is not None:
            states[state] = fn

        def wrapper():
            return fn()

        return wrapper

    return decorator


async def handle(params: Parameters):
    command = params.body.request.command.lower()
    for key_command, item in commands.items():
        for key in key_command:
            if key == command:
                return await item(params)

    state = states.get(global_state[params.body.session.user_id]["next_state"])
    if not state:
        return Response(params, text="Команда не распознана.")

    return await state(params)
