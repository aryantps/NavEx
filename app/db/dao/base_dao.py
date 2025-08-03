import abc
import datetime
from abc import ABC

from psycopg2 import sql

from database.drivers.postgres_v2 import PostgresDriverV2
from database.exceptions import DatabaseException

from pytz import timezone


class WhereOperator(object):

    LIKE = "LIKE"
    EQUAL_TO = "="
    IS = "IS"
    IN = "IN"
    LESS_THAN = "<"
    LESS_THAN_EQUAL_TO = "<="
    GREATER_THAN = ">"
    GREATER_THAN_EQUAL_TO = ">="


class BaseDao(ABC):

    _pagination_default_order_by_field = None

    @classmethod
    @abc.abstractmethod
    def get_table_fields(cls):
        pass

    @classmethod
    @abc.abstractmethod
    def get_table_name(cls):
        pass

    @staticmethod
    def get_where_clause(filter_dict, operator_map=None):
        if not operator_map:
            operator_map = {}
        if not filter_dict:
            return sql.SQL(""), {}
        sql_where_clauses = []
        where_placeholder_values = {}
        for k, v in filter_dict.items():
            placeholder_template = f'WHERE-{k}'
            if operator_map.get(k) == WhereOperator.LIKE:
                sql_where_clauses.append(
                    sql.SQL("LOWER({k}) {op} LOWER({v})").format(
                        k=sql.Identifier(*k.split('.')), op=sql.SQL(operator_map.get(k) or WhereOperator.EQUAL_TO),
                        v=sql.Placeholder(name=placeholder_template)
                    )
                )
            elif v is None:
                sql_where_clauses.append(
                    sql.SQL("{k} {op} {v}").format(
                        k=sql.Identifier(*k.split('.')), op=sql.SQL(operator_map.get(k) or WhereOperator.IS),
                        v=sql.SQL("NULL")
                    )
                )
                continue
            else:
                sql_where_clauses.append(
                    sql.SQL("{k} {op} {v}").format(
                        k=sql.Identifier(*k.split('.')), op=sql.SQL(operator_map.get(k) or WhereOperator.EQUAL_TO),
                        v=sql.Placeholder(name=placeholder_template)
                    )
                )
            where_placeholder_values[placeholder_template] = v

        where_clause = sql.SQL(" AND ").join(sql_where_clauses)
        where_clause = sql.SQL('WHERE {} ').format(where_clause)
        return where_clause, where_placeholder_values

    @classmethod
    def get_order_by_clause(cls, order_by_key, order_by_order):
        if order_by_key:
            order_by_clause = sql.SQL(" ORDER BY {} {}").format(
                sql.Identifier(*order_by_key.split('.')), sql.SQL(order_by_order))
        else:
            order_by_clause = sql.SQL("")
        return order_by_clause

    @classmethod
    def get_limit_clause(cls, limit):
        if limit:
            limit_clause = sql.SQL(" LIMIT {}").format(sql.Literal(limit))
        else:
            limit_clause = sql.SQL("")
        return limit_clause

    @classmethod
    def get_offset_clause(cls, offset):
        if offset:
            offset_clause = sql.SQL(" OFFSET {}").format(sql.Literal(offset))
        else:
            offset_clause = sql.SQL("")
        return offset_clause

    @classmethod
    def query(
            cls, filters, fields=None, order_by_key=None, order_by_order="DESC", limit=None, offset=None,
            operator_map=None, cursor=None, connection=None, credentials=None):
        if fields:
            fields = sql.SQL(",").join(sql.Identifier(x) for x in fields)
        else:
            fields = sql.SQL('*')

        table_name = cls.get_table_name()
        filters = BaseDao.clean(filters, cls.get_table_fields())

        where_clause, where_values = cls.get_where_clause(filters, operator_map=operator_map)
        offset_clause = cls.get_offset_clause(offset)
        limit_clause = cls.get_limit_clause(limit)
        order_by_clause = cls.get_order_by_clause(order_by_key, order_by_order)

        query = sql.SQL("select {fields} from {table_name} {where_clause} {order_by_clause} "
                        "{limit_clause} {offset_clause};").format(
            fields=fields,
            table_name=sql.Identifier(table_name),
            where_clause=where_clause,
            offset_clause=offset_clause,
            limit_clause=limit_clause,
            order_by_clause=order_by_clause
        )
        resp = cls.execute(query, where_values, cursor=cursor, connection=connection, credentials=credentials)
        return BaseDao.process_response(resp)

    @classmethod
    def custom_query(cls, select_clause, where_clause, where_values, order_by_key=None, order_by_order="DESC", limit=None,
              offset=None, cursor=None, connection=None, credentials=None):

        offset_clause = cls.get_offset_clause(offset)
        limit_clause = cls.get_limit_clause(limit)
        order_by_clause = cls.get_order_by_clause(order_by_key, order_by_order)

        query = sql.SQL("{select_clause} {where_clause} {order_by_clause} "
                        "{limit_clause} {offset_clause};").format(
            select_clause=select_clause,
            where_clause=where_clause,
            offset_clause=offset_clause,
            limit_clause=limit_clause,
            order_by_clause=order_by_clause
        )
        resp = cls.execute(query, where_values, cursor=cursor, connection=connection, credentials=credentials)
        return BaseDao.process_response(resp)

    @classmethod
    def insert(cls, insert_dict, cursor=None, connection=None, credentials=None):
        insert_dict = BaseDao.clean(insert_dict, cls.get_table_fields())
        fields = insert_dict.keys()
        query = sql.SQL("INSERT INTO {table_name} ({fields}) VALUES ({values}) RETURNING *;").format(
            table_name=sql.Identifier(cls.get_table_name()),
            fields=sql.SQL(",").join([sql.Identifier(x) for x in fields]),
            values=sql.SQL(",").join([sql.Placeholder(x) for x in fields])
        )
        return cls.execute(query, insert_dict, cursor=cursor, connection=connection, credentials=credentials)

    @classmethod
    def get_set_clause(cls, set_dict):
        sql_set_clauses = []
        set_placeholder_values = {}
        for k, v in set_dict.items():
            placeholder_template = f'SET-{k}'
            sql_set_clauses.append(
                sql.SQL("{k}={v}").format(k=sql.Identifier(k), v=sql.Placeholder(name=placeholder_template))
            )
            set_placeholder_values[placeholder_template] = v
        set_clause = sql.SQL(" , ").join(sql_set_clauses)
        return set_clause, set_placeholder_values

    @classmethod
    def update(cls, filter_dict, set_dict, operator_map=None, cursor=None, connection=None, credentials=None, clean=True):
        if clean:
            set_dict = BaseDao.clean(set_dict, cls.get_table_fields())
            filter_dict = BaseDao.clean(filter_dict, cls.get_table_fields())

        set_clause, set_placeholder_values = cls.get_set_clause(set_dict)
        where_clause, where_placeholder_values = cls.get_where_clause(filter_dict, operator_map=operator_map)

        if set_dict:
            query = sql.SQL("UPDATE {table_name} set {set_clause} {where_clause}").format(
                table_name=sql.Identifier(cls.get_table_name()),
                set_clause=set_clause,
                where_clause=where_clause
            )
            cls.execute(
                query, {**set_placeholder_values, **where_placeholder_values}, result=False, cursor=cursor,
                connection=connection, credentials=credentials)
            return True

    @classmethod
    def count(cls, filters, operator_map=None, credentials=None):
        table_name = cls.get_table_name()
        filters = BaseDao.clean(filters, cls.get_table_fields())
        where_clause, where_values = cls.get_where_clause(filters, operator_map=operator_map)
        query = sql.SQL("select count(*) from {table_name} {where_clause};").format(
            table_name=sql.Identifier(table_name),
            where_clause=where_clause
        )
        resp = cls.execute(query, where_values, credentials=credentials)
        if resp:
            resp = resp[0].get('count')
        return resp

    @classmethod
    # deprecated
    def custom_count(cls, select_clause, where_clause, where_values, credentials=None):
        try:
            join_clause = sql.SQL("")
            from_clause = select_clause.string.lower().split(' from ')
            if len(from_clause) < 2:
                raise Exception('table name not found')

            table_name = from_clause[1].split(" ")[0]
            if len(from_clause[1].split(" ")) > 1:
                join_clause = sql.SQL("".join(select_clause.string.lower().split(f'{table_name} ')[1:]))
        except Exception as e:
            raise DatabaseException('table name not found in custom query.{} {}'.format(select_clause, str(e)))

        query = sql.SQL("select count(*) from {table_name} {join_clause} {where_clause};").format(
            table_name=sql.Identifier(table_name),
            where_clause=where_clause,
            join_clause=join_clause
        )
        resp = cls.execute(query, where_values, credentials=credentials)
        if resp:
            resp = resp[0].get('count')
        return resp

    @classmethod
    def custom_count_v2(cls, select_clause, where_clause, where_values, credentials=None):
        select_clause = select_clause.string.lower().split('select ')
        select_clause = select_clause[-1]
        select_clause = select_clause.split(' from ')
        sc = select_clause[0]
        fc = select_clause[1]

        query = sql.SQL("select count({sc}) from {fc} {where_clause};").format(
            sc=sql.SQL(sc),
            fc=sql.SQL(fc),
            where_clause=where_clause
        )
        resp = cls.execute(query, where_values, credentials=credentials)
        if resp:
            resp = resp[0].get('count')
        return resp

    @staticmethod
    def get_pagination_dict(page, size, count):
        pagination = {}
        pagination['count'] = count
        pagination['size'] = int(size)
        pagination['page'] = int(page)
        pagination['next'] = (page + 1) if count > page * size else None
        pagination['previous'] = (page - 1) if page > 1 else None
        pagination['offset'] = (pagination['page'] - 1) * pagination['size']
        return pagination

    @classmethod
    def paginated_query(cls, filters, fields=None, page=1, page_size=10, order_by_key=None, order_by_order="DESC",
                        operator_map=None, credentials=None):
        filter_dict = BaseDao.clean(filters, cls.get_table_fields())
        order_by = order_by_key or cls._pagination_default_order_by_field
        count = cls.count(filter_dict, operator_map=operator_map)
        pagination = cls.get_pagination_dict(page, page_size, count)
        results = cls.query(
            filter_dict, fields=fields, order_by_key=order_by, order_by_order=order_by_order,
            limit=page_size, offset=((page-1) * page_size), operator_map=operator_map, credentials=credentials
        )
        return results, pagination

    @classmethod
    def custom_paginated_query(
            cls, select_clause, where_clause, where_values, page=1, page_size=10, order_by_key=None,
            order_by_order="DESC", credentials=None):
        order_by = order_by_key or cls._pagination_default_order_by_field
        count = cls.custom_count_v2(select_clause, where_clause, where_values)
        pagination = cls.get_pagination_dict(page, page_size, count)
        results = cls.custom_query(
            select_clause, where_clause, where_values, order_by_key=order_by_key, order_by_order=order_by_order,
            limit=page_size, offset=((page - 1) * page_size), credentials=credentials
        )
        return results, pagination

    @classmethod
    def custom_unpaginated_query(cls, select_clause, where_clause, where_values, order_by_key=None,
                                 order_by_order="DESC", credentials=None):
        order_by = order_by_key or cls._pagination_default_order_by_field

        results = cls.custom_query(
            select_clause, where_clause, where_values, order_by_key=order_by_key, order_by_order=order_by_order,
            credentials=credentials
        )
        return results

    @classmethod
    def execute(cls, sqls, data, result=True, cursor=None, connection=None, credentials=None):
        db = PostgresDriverV2(credentials=credentials)
        res = db.execute(sqls, data, resp=result, cursor=cursor, connection=connection)
        return res

    @staticmethod
    def clean(dict1, list2):
        """
        remove additional dict1 elements that are not in list2
        :param dict1:
        :param list2:
        :return:
        """
        _popped_keys = []
        for elem1 in dict1.keys():
            if elem1 not in list2:
                _popped_keys.append(elem1)
        for k in _popped_keys:
            dict1.pop(k)
        return dict1

    @staticmethod
    def is_subset(list1, list2):
        """
        check if list1 is a subset of list2
        :param lists1:
        :param list2:
        :return:
        """
        if all(x in list2 for x in list1):
            return True
        return False

    @staticmethod
    def process_response(resp):
        for dict_resp in resp:
            for k, v in dict_resp.items():
                if isinstance(v, datetime.datetime):
                    dict_resp[k] = str(BaseDao.parse_datetime(str(v)))
        return resp

    @staticmethod
    def parse_datetime(value, key=None):
        try:
            if value:
                ist_tz = timezone('Asia/Kolkata')
                date = datetime.datetime.fromisoformat(value)
                date = date.astimezone(tz=ist_tz)
                return date
        except ValueError as e:
            raise DatabaseException("{} is not a valid datetime".format(key))

    @classmethod
    def insert_many(cls, insert_dict_list, cursor=None, connection=None, credentials=None):
        insert_fields = cls.get_insert_fields(insert_dict_list)

        query = sql.SQL("INSERT INTO {} ({}) VALUES").format(
            sql.Identifier(cls.get_table_name()),
            sql.SQL(",").join(map(sql.Identifier, insert_fields))
        )
        insert_many_dict = {}
        for index, insert_dict in enumerate(insert_dict_list):
            query += sql.SQL("(") if index == 0 else sql.SQL(", (")
            for key_index, (key, value) in enumerate(insert_dict.items()):
                query += sql.Placeholder(str(index) + "_" + key)
                if key_index != len(insert_dict) - 1:
                    query += sql.SQL(",")
                insert_many_dict[str(index) + "_" + key] = value
            query += sql.SQL(")")

        query += sql.SQL(" returning *;")
        cls.execute(query, insert_many_dict, cursor=cursor, connection=connection, credentials=credentials)

    @classmethod
    def get_insert_fields(cls, insert_dict_list):
        insert_fields = cls.get_table_fields()
        insert_fields = list(insert_fields)
        insert_fields_temp = list(insert_dict_list[0].keys())

        to_delete_fields = []
        for field in insert_fields:
            if field not in insert_fields_temp:
                to_delete_fields.append(field)

        for field in to_delete_fields:
            insert_fields.pop(insert_fields.index(field))

        return tuple(insert_fields)
