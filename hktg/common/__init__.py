
from ._ask_text import AskText


def get_user_promotions(phone=None, tg_id=None):
    from hktg import db

    users = db.get_table(db.Tables.USERS)
    for u in users:
        user = db.User(*u)
        if user.tg_id == tg_id or user.phone == phone:
            promotions = db.get_table(db.Tables.PROMOTIONS, {'users_id': user.id})
            roles = db.get_table(db.Tables.ROLES)
            result = []
            for p in promotions:
                prom = db.Promotion(*p)
                result.append(prom.role()) 
            return result
    return []
