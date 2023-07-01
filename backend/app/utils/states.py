from typing import Any, Dict

global_state = {}


class StateField:
    def __init__(self, value: Any = None):
        self.value = value

    def set(self, value):
        self.value = value


class State:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.next_value = None

        if not global_state.get(user_id):
            global_state[user_id] = {"next_state": None, "args": {}}

        for key, value in self.__class__.__dict__.items():
            self.__dict__.update({key: value})

    def wait_state(self, param: StateField) -> None:
        global_state[self.user_id]["next_state"] = param
        self.next_value = param

    def __setattr__(self, key: str, value: Any) -> Any | None:
        if not isinstance(self.__dict__.get(key), StateField):
            return super().__setattr__(key, value)

        self.__dict__[key].set(value)
        global_state[self.user_id]["args"].update({key: value})

    def arguments(self) -> Dict[str, Any]:
        return self.__dict__

    def values(self) -> Dict[str, Any]:
        return global_state[self.user_id]["args"]

    def stop_state(self) -> None:
        del global_state[self.user_id]["next_state"]
