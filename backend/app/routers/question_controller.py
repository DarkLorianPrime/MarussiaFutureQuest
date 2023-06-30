from utils.handler import message_handler
from utils.models import Parameters
from utils.responses import Response

win_sound = "<speaker audio=marusia-sounds/game-win-2>"
win_lose = "<speaker audio=marusia-sounds/game-loss-1>"


@message_handler(commands_list=["категория"])
async def select_category(params: Parameters):
    text = "Я задам 8 простых вопросов и по ним мы поймем куда тебе стоит двигаться." \
           "\nСкажи \"жду вопросы\", если хочешь начать"
    tts = "Ты хочешь узнать какую категорию взять на вездек+оде? Ну давай попробуем!"

    if params.user.questions:
        text = "Ты уже начал прохождение теста"
        tts = "Ты уже начал прохождение теста"

    return Response(params, text=text, tts=tts)


@message_handler(commands_list=["жду вопросы"])
async def wait_questions(params: Parameters):
    if params.user.questions:
        text = "Ты уже начал прохождение теста"
        tts = "Ты уже начал прохождение теста"
        return Response(params, tts=tts, text=text)

    first_question = await params.service.get_question(params.user.questions)

    if first_question is None:
        text = "В базе еще нет вопросов. Ты можешь добавить их командой: вопрос"
        tts = "Кажется в базе нет вопросов..."
        return Response(params, tts=tts, text=text)

    text = f"Вопрос категории: {first_question.title}\n{first_question.text}"
    tts = first_question.tts

    await params.service.set_question_user(params.user, first_question)

    return Response(params, tts=tts, text=text)


async def answer_question(params: Parameters, question):
    await params.service.answer_question(params.user, question, params.body.request.command)
    next_question = await params.service.get_question(map(lambda x: x.question_id, params.user.questions))

    if next_question:
        text = f"Вопрос категории: {next_question.title}\n{next_question.text}"
        tts = next_question.tts

        await params.service.set_question_user(params.user, next_question)

        return Response(params, tts=tts, text=text)

    max_points = await params.service.get_required_points()

    if max_points > params.user.points:
        text = f"{win_lose}К сожалению, вы не набрали минимальное количество баллов в тесте. Сбросить результат: сброс"
        tts = f"{win_lose}К сожалению, вы не набрали минимальное количество баллов в тесте."
    else:
        text = f"{win_sound}Поздравляю с успешным прохождением теста. Вы - по праву IT специалист."
        tts = f"{win_sound}Поздравляю с успешным прохождением теста."

    return Response(params, text=text, tts=tts)
