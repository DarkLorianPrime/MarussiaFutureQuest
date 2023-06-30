from utils.states import StateField, State


class QuestStateList(State):
    title = StateField()
    text = StateField()
    tts = StateField()
    points = StateField()
    answer = StateField()
    required = StateField()
