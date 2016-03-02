import sys

if sys.version < '3':  # Python 2
    from Tkinter import Tk, Frame, Entry, Label, Button
    from Tkinter.ttk import Combobox, Treeview
else:  # Python 3 is being used
    from tkinter import Tk, Frame, Entry, Label, Button
    from tkinter.ttk import Combobox, Treeview

from database import InventoryDatabase


class RecordController(Frame):
    def __init__(self, master, *args, **kwargs):
        super(RecordController, self).__init__(master, *args, **kwargs)
        self.master = master
        self.current_record = 0
        self.create_widgets()

    def create_widgets(self):
        self.record_label = Label(self, text='Records')
        self.record_label.grid(column=1, row=1)
        self.to_beginning_button = Button(self, text='|<')
        self.to_beginning_button.grid(column=2, row=1)
        self.to_backone_button = Button(self, text='<')
        self.to_backone_button.grid(column=3, row=1)

        self.search_field = Entry(self)
        self.search_field.grid(column=4, row=1)

        self.to_fowardone_button = Button(self, text='>')
        self.to_fowardone_button.grid(column=5, row=1)
        self.to_end_button = Button(self, text='>|')
        self.to_end_button.grid(column=6, row=1)

    def on_get_record_button_press(self, event):
        if event.widget.text == '|<':
            self.current_record = 0
        elif event.widget.text == '<':
            self.current_record -= 1
            if self.current_record < 0:
                self.current_record = 0
        elif event.widget.text == '>':
            self.current_record += 1
        elif event.widget.text == '>|':
            self.current_record += 1  # TODO This isnt right for now


class App(Frame):
    def __init__(self, master, *args, **kwargs):
        super(App, self).__init__(master, *args, **kwargs)
        self.master = master
        self.db = InventoryDatabase('database.db')
        self.create_widgets()

    def create_widgets(self):
        self.item_number_label = Label(self, text='Item Number: ')
        self.item_number_label.grid(column=1, row=1)
        self.item_number_entry = Entry(self)
        self.item_number_entry.grid(column=2, row=1)

        self.description_label = Label(self, text='Description:')
        self.description_label.grid(column=1, row=2)
        self.description_entry = Entry(self)
        self.description_entry.grid(column=2, row=2)

        self.quantity_label = Label(self, text='Quantity: ')
        self.quantity_label.grid(column=1, row=3)
        self.quantity_entry = Entry(self)
        self.quantity_entry.grid(column=2, row=3)

        self.min_level_label = Label(self, text='Min Level: ')
        self.min_level_label.grid(column=1, row=3)
        self.min_level_entry = Entry(self)
        self.min_level_entry.grid(column=2, row=3)

        self.max_level_label = Label(self, text='Max Level: ')
        self.max_level_label.grid(column=1, row=4)
        self.max_level_entry = Entry(self)
        self.max_level_entry.grid(column=2, row=4)

        self.packet_label = Label(self, text='Items Per Packet: ')
        self.packet_label.grid(column=1, row=5)
        self.packet_entry = Entry(self)
        self.packet_entry.grid(column=2, row=5)

        self.id_label = Label(self, text='ID: ')
        self.id_label.grid(column=3, row=1)
        self.id_entry = Entry(self)
        self.id_entry.grid(column=4, row=1)

        self.location_label = Label(self, text='Location: ')
        self.location_label.grid(column=3, row=2)
        self.location_entry = Combobox(self)
        self.location_entry.config({'value': 'Office Garage'})
        self.location_entry.grid(column=4, row=2)

        self.supplier_price_label = Label(self, text='Supplier Price: ')
        self.supplier_price_label.grid(column=3, row=3)
        self.supplier_price_entry = Entry(self)
        self.supplier_price_entry.grid(column=4, row=3)

        self.sell_price_label = Label(self, text='Sell Price: ')
        self.sell_price_label.grid(column=3, row=4)
        self.sell_price_entry = Entry(self)
        self.location_entry.grid(column=4, row=4)

        self.measured_by_label = Label(self, text='Measured By: ')
        self.measured_by_label.grid(column=3, row=5)
        self.measured_by_entry = Combobox(self)
        self.measured_by_entry.config({'value': 'Item Metre'})
        self.measured_by_entry.grid(column=4, row=5)

        self.image_label = Label(self, text='Image')
        self.image_label.grid(column=3, row=6)
        # Give fixed height and width

        self.supplers_label = Label(self, text='Suppliers')
        self.supplers_label.grid(column=1, row=7)
        self.supplers_table = Treeview(self)
        self.supplers_table.grid(column=1, row=8, columnspan=4)

        self.record_controller = RecordController(self)
        self.record_controller.grid(column=1, row=9, columnspan=4)

    def destroy(self):
        self.db.close()
        super(App, self).destroy()


root = Tk()
root.geometry('800x600')
root.update()
root.minsize(root.winfo_width(), root.winfo_height())
root.maxsize(root.winfo_width(), root.winfo_height())
App(root).pack(fill='both', side='top', expand=True)
root.mainloop()
