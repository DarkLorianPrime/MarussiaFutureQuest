from routers import common, question_creator, question_controller  # noqa

from models import Base, engine
from routers.question_controller import answer_question
from state import QuestStateList

from utils.handler import handle
from utils.models import Parameters
from utils.core import listener


async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@listener(QuestStateList)
async def webhook_endpoint(params: Parameters):
    for user_question in params.user.questions:
        if not user_question.answered:
            return await answer_question(params, user_question)
    return await handle(params)

app = listener()
