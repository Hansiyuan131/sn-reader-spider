import pymysql
from pymysql import cursors
from twisted.enterprise import adbapi

class ArticlePipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'mysql123456',
            'database': 'db_mynews',
            'charset': 'utf8'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        self.cursor.execute(self.sql, (item['id'], item['title']))
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
                insert into table(id,title) values (null,%s)
            """
            return self._sql
        return self._sql

class ArticleTwistedPipeline(object):
    """ 异步存储"""

    def __init__(self):
        dbparams = {

            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'mysql123456',
            'database': 'db_mynews',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
                       insert into table(id,title) values (null,%s)
                   """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item, item)

        defer.addErrback(self.handle_error, item, spider)

        return item

    def insert_item(self, cursor, item):
        cursor.execute(self.sql, (item['id'], item['title']))

    def handle_error(self, error, item, spider):
        print('=' * 10 + "error" + '=' * 10)
        print(error)
        print('=' * 10 + "error" + '=' * 10)

from scrapy.exporters import JsonLinesItemExporter