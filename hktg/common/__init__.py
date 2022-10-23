
from ._ask_text import AskText

from typing import List
from hktg import db


def _get_user_promotions(users=[], tg_id: int = None) -> List[db.Promotion]:

    if not users:
        users = db.get_table(db.User)

    for user in users:
        # user = db.User(*u)
        # or (phone and user.phone == phone):
        if tg_id and user.tg_id and int(user.tg_id) == int(tg_id):
            return db.get_table(db.Promotion, {'users_id': user.id})
    return []


def tg_has_role(tg_id: int, rolename: str, users=None, roles=None):  # -> bool:

    ps = _get_user_promotions(users, tg_id=tg_id)
    return next((x for x in ps if x.role(roles).name == rolename), None)
