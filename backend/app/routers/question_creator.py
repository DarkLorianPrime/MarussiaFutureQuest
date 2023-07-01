from state import QuestStateList
from utils.responses import Response
from utils.handler import message_handler
from utils.pydantic import Parameters


@message_handler(commands_list=["вопрос"])
async def start_adding_question(params: Parameters):
    params.state.wait_state(QuestStateList.title)
    return Response(params,
                    text="Сообщи название своего вопроса",
                    tts="Хорошо, давай добавим новый вопрос! Как назовем?")


@message_handler(state=QuestStateList.title)
async def set_question_title(params: Parameters):
    params.state.title = params.body.request.command
    params.state.wait_state(QuestStateList.text)
    return Response(params,
                    text="Сообщи текст вопроса",
                    tts="С названием определились, в чём состоит вопрос?")


@message_handler(state=QuestStateList.text)
async def set_question_text(params: Parameters):
    params.state.text = params.body.request.command
    params.state.wait_state(QuestStateList.tts)
    return Response(params,
                    text="Текст отличный. Как мне его проговаривать?",
                    tts="Сообщи, как я буду проговаривать вопрос устно (Ударения ставятся с \"+\" до буквы)")


@message_handler(state=QuestStateList.tts)
async def set_question_tts(params: Parameters):
    params.state.tts = params.body.request.command
    params.state.wait_state(QuestStateList.points)
    return Response(params,
                    tts="Как боженька смолвил.",
                    text="Сколько баллов дадут за правильный ответ на это задание?")


@message_handler(state=QuestStateList.points)
async def set_question_points(params: Parameters) -> Response:
    points_text = params.body.request.nlu.tokens[0]
    if not points_text.isdigit():
        return Response(params,
                        text="Введи число",
                        tts="Количество поинтов должно быть числом.")

    params.state.points = int(points_text)
    params.state.wait_state(QuestStateList.answer)
    return Response(params,
                    text="Какой правильный ответ на ваше задание?",
                    tts="Щедро, очень даже щедро")


@message_handler(state=QuestStateList.answer)
async def set_question_answer(params: Parameters) -> Response:
    params.state.answer = params.body.request.command
    params.state.wait_state(QuestStateList.required)
    return Response(params,
                    tts="Ого, и как я сама не догадалась?",
                    text="Обязательно ли ваше задание для получения всех баллов?")


@message_handler(state=QuestStateList.required)
async def set_question_required(params: Parameters) -> Response:
    answer_text: str = params.body.request.nlu.tokens[0].lower()
    if answer_text not in ["да", "нет"]:
        return Response(params, text="Ответ должен быть: да или нет.")

    params.state.required = answer_text == "да"
    params.state.wait_state(QuestStateList.required)
    params.state.stop_state()
    await params.service.save_question(params.state.values())
    return Response(params,
                    text="Считаю шикарный вопрос. Сейчас сохраню",
                    tts="Вопрос был сохранен.")
