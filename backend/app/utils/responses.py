from starlette.responses import JSONResponse

from utils.models import Parameters

derived_session_fields = ['session_id', 'user_id', 'message_id']

class Response(JSONResponse):
    def __init__(self, params: Parameters, *, text: str, tts: str = None):
        text = text
        tts = text if tts is None else tts
        super().__init__({"response": {"text": text, "tts": tts, "end_session": False},
                          "session": {derived_key: params.body.session.__getattribute__(derived_key)
                                      for derived_key in derived_session_fields},
                          "version": params.body.version
                          })
