
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
    VIEWING_WAREHOUSE = 7
    CHOOSING_CONTAINER = 8
    ENTERING_SYMBOL = 9
    ENTERING_TEXT = 10
    VIEWING_ENTRY = 11
    VIEWING_PRODUCT = 12
    VIEWING_PRODUCTS = 13
    END = ConversationHandler.END


class Action(Enum):
    HOME = 1
    BACK = 2
    VIEW_PRODUCTS = 3
    CREATE = 4
    DELETE = 5
    MODIFY = 6

    @staticmethod
    def description(action):
        descriptions = {
            Action.HOME: "🏠 Додому",
            Action.BACK: "< Назад",
            Action.VIEW_PRODUCTS: "🔍 До складу",
            Action.CREATE: "➕ Додати",
            Action.DELETE: "➖ Видалити",
            Action.MODIFY: "🖊️ Змінити",
            ConversationHandler.END: "🚪 Закінчити",
        }
        return descriptions[action]

    def __str__(self):
        return self.name

class UserDataKey(Enum):
    ACTION = 1
    PRODUCT = 2
    LOCATION = 3
    CONTAINER = 4
    AMOUNT = 5
    CONTAINER_SYMBOL = 6
    FIELD_TYPE = 7
    LIMIT = 8
    CURRENT_ID = 9

@dataclass
class UserData:
    action: Action | None = None
    entry_id: int | None = None
    product_id: int | None = None
    location_id: int | None = None
    container_id: int | None = None
    limit_amount: int | None = None
    text: str | None = None
    symbol: str | None = None

    def dict(self):
        return {k: str(v) for k, v in dataclasses.asdict(self).items()}

    def with_dict(self, new: dict):
        for key, value in new.items():
            setattr(self, key, value)
        return self

    def __str__(self):
        return self.to_dict()

    def with_obj(self, new: object):
        def assign_if(src, dst, key):
            setattr(self, key, value)
        for f in dataclasses.fields(self):
            value = getattr(new, f.name)
            if value:
                setattr(self, f.name, value)
        return self
