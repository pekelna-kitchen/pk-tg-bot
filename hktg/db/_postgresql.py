
import os
import logging
import psycopg2

from ._types import Tables

_DATABASE_URL = os.environ["DATABASE_URL"]
_CONNECTION = psycopg2.connect(_DATABASE_URL)

# simple query wrappers and helpers

def _join_dict(table: dict, separator:str=', '):
    result = []
    for k in table:
        if table[k]:
            value = "'%s'" % table[k] if isinstance(table[k], str) else str(table[k])
            result.append("%s=%s" % (k, value))
        else:
            logging.debug('empty value %s' % k)
    return separator.join(result)


def _query(q: str):
    cur = _CONNECTION.cursor()
    logging.debug("SQL: %s" % q)
    try:
        cur.execute(q)
    except Exception as err:
        logging.exception(err)
        _CONNECTION.rollback()
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
    _CONNECTION.commit()


def delete_value(table_name, criteria: dict):
    cur = _query("DELETE FROM %s WHERE %s;" %
                       (table_name, _join_dict(criteria)))
    _CONNECTION.commit()


def insert_value(table_name, data: dict):
    columns = []
    values = []
    for key in data:
        columns.append(key)
        value = "'%s'" % data[key] if isinstance(data[key], str) else str(data[key])
        values.append(value)

    cur = _query("INSERT INTO %s (%s) VALUES (%s);" % (table_name, ", ".join(columns), ", ".join(values)))
    _CONNECTION.commit()
