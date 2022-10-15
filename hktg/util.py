
import json

from telegram import (
    InlineKeyboardButton,
    Update
)
from telegram.ext import ContextTypes

from .constants import Action

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):

        import dataclasses
        from enum import Enum

        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)

        if isinstance(o, Enum):
            return o.name

        return super().default(o)

def split_list(source: list, count: int):
    result = []
    for i in range(0, len(source), count):
        result.append(source[i:i+count])
    return result


def action_button(action: Action):

    from telegram import InlineKeyboardButton

    return InlineKeyboardButton(text=Action.description(action), callback_data=action)


# 
def find_tuple_element(tuples, comparables: dict):
    def check_tuple_elem(t):
        for key in comparables:
            if t[key] != comparables[key]:
                return False
        return True

    return next((x for x in tuples if check_tuple_elem(x)), None)

