from starlette.responses import JSONResponse

from utils.pydantic import Parameters

session_fields = ['session_id', 'user_id', 'message_id']


class Response(JSONResponse):
    def __init__(self, params: Parameters, *, text: str, tts: str = None):
        tts = text if tts is None else tts
        session_params = {field: params.body.session.__getattribute__(field) for field in session_fields}
        response = {"text": text, "tts": tts, "end_session": False}

        super().__init__({"response": response, "session": session_params, "version": params.body.version})
