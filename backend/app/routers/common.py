from utils.responses import Response
from utils.handler import message_handler
from utils.models import Parameters


@message_handler(commands_list=["старт", "начать", "начало"])
async def send_hello(params: Parameters):
    text = "Привет! Для продолжения напиши \"Категория\""
    return Response(params, text=text)


@message_handler(commands_list=["вездеход"])
async def send_vezdecode(params: Parameters):
    tts = "Привет вездек+одерам!"
    text = "Привет вездекодерам!"
    return Response(params, text=text, tts=tts)


@message_handler(commands_list=["сброс"])
async def reset_questions(params: Parameters):
    await params.service.reset_user(params.user)
    return Response(params, text="Все задания сброшены.")
