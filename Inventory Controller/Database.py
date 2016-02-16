import os, sqlite3, sys, time

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
            cursor.execute(sql)
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

class InventoryDatabase(AsyncDatabaseManager):
    def __init__(self, directory):
        super().__init__(directory)

    def add_item(self,
                 id='', 
                 sku='', 
                 name='', 
                 description='', 
                 sellprice='', 
                 notes='',
                 category=0):
        command = '''INSERT INTO product(id, sku, name, description, sellprice, notes, category) VALUES({id},"{sku}","{name}","{description}",{sellprice},"{notes}",{category})'''.format(
            id=id,
            sku=sku,
            name=name,
            description=description,
            sellprice=sellprice,
            notes=notes,
            category=category)
        try:
            print(command)
        except Exception:
            pass
        self.execute(command)

    def add_item_from_spreadsheet(self, id, sku, quantity, purchases, sellprice, startdate, name, category):
        self.add_item(id, sku, name, '', sellprice, '')


    def get_product_image(self, SKU):
        image = next(self.select('SELECT image FROM product WHERE sku={}'.format(SKU)))
        data = StringIO(str(image))
        pic = ImageTk.PhotoImage(Image.open(data))
        # Need to think of this
        patface = Tkinter.Label(func, image=pic)
        patface.grid(row=0, column=1)


    def get_product_from_id(self, id):
        command="""SELECT * FROM product WHERE id={}""".format(id)
        product = self.select(command)
