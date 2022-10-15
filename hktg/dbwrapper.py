
import psycopg2
import logging
from dataclasses import dataclass
from typing import Optional

# DB tables names

class Tables:
    LOCATION = 'locations'
    ENTRIES = 'entries'
    PRODUCT = 'products'
    CONTAINER = 'containers'
    LIMIT = 'limits'
    TG_USERS = 'tg_users'
    TG_ADMINS = 'tg_admins'
    TG_REQUESTS = 'tg_requests'

import os
DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL)

def _join_dict(table: dict, separator:str=', '):
    result = []
    for k in table:
        value = "'%s'" % table[k] if isinstance(table[k], str) else str(table[k])
        result.append("%s=%s" % (k, value))
    return separator.join(result)


def _query(q: str):
    cur = conn.cursor()
    logging.debug("SQL: %s" % q)
    try:
        cur.execute(q)
    except Exception as err:
        logging.exception(err)
        conn.rollback()
        raise

    return cur

# simple queries


def get_table(name, where:dict={}):
    where_str = "WHERE %s" % _join_dict(where, ' AND ') if where else ""

    cur = _query("SELECT * FROM %s %s;" % (name, where_str))
    return cur.fetchall()


def update_value(table_name, data: dict, criteria: dict):
    cur = _query("UPDATE %s SET %s WHERE %s;" %
                       (table_name, _join_dict(data), _join_dict(criteria)))
    conn.commit()


def delete_value(table_name, criteria: dict):
    cur = _query("DELETE FROM %s WHERE %s;" %
                       (table_name, _join_dict(criteria)))
    conn.commit()


def insert_value(table_name, data: dict):
    columns = []
    values = []
    for key in data:
        columns.append(key)
        value = "'%s'" % data[key] if isinstance(data[key], str) else str(data[key])
        values.append(value)

    cur = _query("INSERT INTO %s (%s) VALUES (%s);" % (table_name, ", ".join(columns), ", ".join(values)))
    conn.commit()

# some more logic over


def find_in_table(table_name, index, comparable):

    table = get_table(table_name)
    return next((x for x in table if x[index] == comparable), None)


def update_entry(id, user_name, data):

    from datetime import datetime

    entries = get_table(Tables.ENTRIES)
    entry = next((x for x in entries if x[0] == id), None)

    data["date"] = "'%s'" % datetime.now()
    data["editor"] = "'%s'" % user_name

    if not amount:
        delete_value(Table.ENTRIES, {'id': user_data[UserDataKey.CURRENT_ID]})
    elif entry:
        update_value(Table.ENTRIES, data, {'id': id})
    else:
        insert_value(ENTRIES, data)

# def

@dataclass()
class Product:
    id : Optional[int] = None
    symbol : Optional[str] = None
    name : Optional[str] = None
    limit_container : Optional[int] = None
    limit_amount : Optional[int] = None

    def container_symbol(self, containers = None):

        if not self.limit_container:
            return None

        from hktg import util
        if not containers:
            containers = get_table(Tables.CONTAINER)
        _, cont_sym, _ = util.find_tuple_element(containers, {0: self.limit_container})
        return cont_sym

    def is_valid(self):
        return self.symbol and self.name and self.limit_container and self.limit_amount


    def to_sql(self):
        return {
            "name": self.name,
            "symbol": self.symbol,
            "limit_container": self.limit_container,
            "limit_amount": self.limit_amount,
        }

@dataclass
class Entry:
    id: Optional[int] = None
    product_id: Optional[int] = None
    location_id: Optional[int] = None
    amount: Optional[int] = None
    container_id: Optional[int] = None
    date: Optional[str] = None
    editor: Optional[str] = None

    def is_valid(self):
        return self.product_id and self.location_id and self.amount and self.container_id

    def to_sql(self):
        return {
            "product_id": self.product_id,
            "location_id": self.location_id,
            "container_id": self.container_id,
            "amount": self.amount,
        }


    def container_symbol(self, containers = None):

        if not self.container_id:
            return None

        from hktg import util
        if not containers:
            containers = get_table(Tables.CONTAINER)
        _, cont_sym, _ = util.find_tuple_element(containers, {0: self.container_id})
        return cont_sym

    def product_symbol(self, products = None):
        if not self.product_id:
            return None

        from hktg import util
        if not products:
            products = get_table(Tables.PRODUCT)
        _, pr_sym, _, _, _ = util.find_tuple_element(products, {0: self.product_id})
        return pr_sym

    def location_symbol(self, locations = None):
        if not self.location_id:
            return None

        from hktg import util
        if not locations:
            locations = get_table(Tables.LOCATION)
        _, loc_sym, _ = util.find_tuple_element(locations, {0: self.location_id})
        return loc_sym

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
