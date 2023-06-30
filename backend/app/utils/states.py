from utils.config import commands

global_state_template = {1: {"next_state": ..., "args": {}}}
global_state = {}


class StateField:
    def __init__(self, value=None):
        self.value = value

    def set(self, value):
        self.value = value


class State:
    def __init__(self, user_id):
        self.user_id = user_id
        self.next_value = None
        if not global_state.get(user_id):
            global_state[user_id] = {"next_state": None, "args": {}}
        for key, value in self.__class__.__dict__.items():
            self.__dict__.update({key: value})

    def wait_state(self, param: StateField):
        global_state[self.user_id]["next_state"] = param
        self.next_value = param

    def __setattr__(self, key, value):
        if not isinstance(self.__dict__.get(key), StateField):
            return super().__setattr__(key, value)

        self.__dict__[key].set(value)
        global_state[self.user_id]["args"].update({key: value})

    def arguments(self):
        return self.__dict__

    def values(self):
        return global_state[self.user_id]["args"]

    def call(self):
        next_state = global_state[self.user_id]["next_state"]
        if not next_state:
            return

        commands[next_state](self)

    def stop_state(self):
        del global_state[self.user_id]["next_state"]
