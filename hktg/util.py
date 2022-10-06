
from telegram import (
    InlineKeyboardButton,
    Update
)
from telegram.ext import ContextTypes

from .constants import (
    UserData,
    UserDataKey,
    Action,
)

def split_list(source: list, count: int):
    result = []
    for i in range(0, len(source), count):
        result.append(source[i:i+count])
    return result

def reset_data(context: ContextTypes.DEFAULT_TYPE):
    if 'data' in context.user_data:
        del context.user_data['data']
    context.user_data['data'] = UserData()

def user_data(context: ContextTypes.DEFAULT_TYPE):
    if 'data' not in context.user_data:
        reset_data(context)

    return UserData(context.user_data['data'])


def action_button(action: Action, callback_data={}):

    from telegram import InlineKeyboardButton
 
    callback_data = UserData(action=action).with_dict(callback_data)
    return InlineKeyboardButton(text=Action.description(action), callback_data=callback_data)


# 
def find_tuple_element(tuples, comparables: dict):
    def check_tuple_elem(t):
        for key in comparables:
            if t[key] != comparables[key]:
                return False
        return True

    return next((x for x in tuples if check_tuple_elem(x)), None)
 

# Action.MODIFY: lambda u, c: update_mapping[query_data[UserDataKey.ACTION]](u, c)
