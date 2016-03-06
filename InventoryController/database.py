import os, sqlite3, sys, time
import unittest
from threading import Thread, Event

if sys.version < '3':  # Python 2
    from Queue import Queue, PriorityQueue  # IGNORE
    from cStringIO import StringIO
else:  # Python 3 is being used
    from queue import Queue, PriorityQueue
    from io import StringIO

from PIL import Image, ImageTk


class AsyncDatabaseManager(Thread):
    def __init__(self, directory):
        super(AsyncDatabaseManager, self).__init__()
        self.directory = directory
        if not os.path.exists(self.directory):
            open(self.directory, 'w').close()
        self.queue = PriorityQueue()
        self.event = Event()
        self.start()  # Threading module start

    def run(self):
        super(AsyncDatabaseManager, self).run()
        db = sqlite3.connect(self.directory)
        cursor = db.cursor()
        while True:
            if self.queue.empty():
                time.sleep(0.1)
                continue
            job, sql, arg, res = self.queue.get_nowait()
            if sql == '__close__':
                break
            cursor.execute(sql, arg)
            time.sleep(0.01)
            db.commit()
            if res:
                for rec in cursor:
                    res.put(rec)
                res.put('__last__')
        db.close()
        self.event.set()  # TODO: Question: Do I want the database to finish or end it when the app ends?

    def execute(self, sql, args=None, res=None, priority=2):
        self.queue.put_nowait((priority, sql, args, res))

    def select(self, sql, args=None, priority=2):
        '''
        :param: sql - command to execute
        :param: args - sql arguments
        :param: priority - 2 for system and 1 for user
        '''
        res = Queue()
        self.execute(sql, args, res, priority)
        while True:
            rec = res.get()
            if rec == '__last__':
                break
            yield rec

    def close(self):
        self.execute('__close__')


_db = AsyncDatabaseManager('database.db')


class Product:
    def __init__(self, product):
        self.id = product[0]
        self.sku = product[1]
        self.name = product[2]
        self.description = product[3]
        self.sellprice = product[4]
        self.notes = product[5]
        self.category = product[6]

    @classmethod
    def from_nothing(cls,
                     id=None,
                     sku=None,
                     name=None,
                     description=None,
                     sellprice=None,
                     notes=None,
                     category=None):
        return cls((id, sku, name, description, sellprice, notes, category))

    @classmethod
    def from_sku(cls, sku):
        command = '''SELECT * FROM product WHERE sku=?'''
        return cls(next(_db.select(command, args=(sku,))))

    def save_to_db(self):
        args = (
            self.sku,
            self.sku,
            self.name,
            self.description,
            self.sellprice,
            self.notes,
            self.category,
        )
        command = 'INSERT OR REPLACE INTO product VALUES ((SELECT id FROM product WHERE sku=?),?,?,?,?,?,?)'
        _db.select(command, args=args, priority=1)


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = AsyncDatabaseManager('test.db')

    def test_add_product(self):
        p = Product.from_nothing()
