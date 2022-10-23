
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

def create_button(text, callback_data):

    from hktg import db
    from telegram import InlineKeyboardButton

    if not text:
        text = "➕"
    types = (db.Location, db.Container, db.Product)
    if isinstance(text, types):
        text = text.desc()
    return InlineKeyboardButton(text, callback_data=callback_data)
