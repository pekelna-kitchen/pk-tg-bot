
from enum import Enum
from telegram.ext import ConversationHandler

import dataclasses
from dataclasses import dataclass

class State(Enum):
    CHOOSING_ACTION = 1
    CHOOSING_LOCATION = 2
    CHOOSING_PRODUCT = 3
    ENTERING_AMOUNT = 4
    ENTERING_LOCATION = 5
    ENTERING_PRODUCT = 6
    VIEWING_PRODUCTS = 7
    CHOOSING_CONTAINER = 8
    ENTERING_SYMBOL = 9
    ENTERING_TEXT = 10
    VIEWING_ENTRY = 11
    VIEWING_PRODUCT = 12
    VIEWING_USERS = 13
    VIEWING_MAP = 14
    VIEWING_USER = 15


class Action(Enum):
    HOME = 1
    BACK = 2
    CREATE = 3
    DELETE = 4
    SAVE = 5
    VIEW_PRODUCTS = 6
    VIEW_MAP = 7
    VIEW_USERS = 8
    END = ConversationHandler.END

    @staticmethod
    def description(action):
        descriptions = {
            Action.HOME: "🏠 Додому",
            Action.BACK: "< Назад",
            Action.CREATE: "➕ Створити",
            Action.DELETE: "➖ Видалити",
            Action.SAVE: "🖊️ Зберегти",
            Action.VIEW_PRODUCTS: "🔍 До складу",
            Action.VIEW_MAP: "🛞 До водіїв",
            Action.VIEW_USERS: "🧰 До користувачів",
            ConversationHandler.END: "🚪 Закінчити",
        }
        return descriptions[action]

    def __str__(self):
        return self.name
