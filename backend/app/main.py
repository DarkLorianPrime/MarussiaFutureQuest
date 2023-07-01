from routers import common, question_creator, question_controller  # noqa

from state import QuestStateList

from utils.handler import handle
from utils.pydantic import Parameters
from utils.core import listener
from utils.responses import Response


@listener(QuestStateList)
async def webhook_endpoint(params: Parameters) -> Response:
    for user_question in params.user.questions:
        if not user_question.answered:
            return await question_controller.answer_question(params, user_question)

    return await handle(params)

app = listener()
