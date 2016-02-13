import sys


if sys.version < '3':  # Python 2
    from Tkinter import Tk, Frame, Entry, Label
    from Tkinter.ttk import Combobox
else:  # Python 3 is being used
    from tkinter import Tk, Frame, Entry, Label
    from tkinter.ttk import Combobox

from Database import InventoryDatabase


class App(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.db = InventoryDatabase('database.sql')
        self.create_widgets()

    def create_widgets(self):
        self.item_number_label = Label(text='Item Number: ')
        self.item_number_label.grid(column=1, row=1)
        self.item_number_entry = Entry()
        self.item_number_entry.grid(column=2, row=1)

        self.description_label = Label(text='Description:')
        self.description_label.grid(column=1, row=2)
        self.description_entry = Entry()
        self.description_entry.grid(column=2, row=2)

        self.quantity_label = Label(text='Quantity: ')
        self.quantity_label.grid(column=1, row=3)
        self.quantity_entry = Entry()
        self.quantity_entry.grid(column=2, row=3)

        self.min_level_label = Label(text='Min Level: ')
        self.min_level_label.grid(column=1, row=3)
        self.min_level_entry = Entry()
        self.min_level_entry.grid(column=2, row=3)

        self.max_level_label = Label(text='Max Level: ')
        self.max_level_label.grid(column=1, row=4)
        self.max_level_entry = Entry()
        self.max_level_entry.grid(column=2, row=4)

        self.packet_label = Label(text='Items Per Packet: ')
        self.packet_label.grid(column=1, row=5)
        self.packet_entry = Entry()
        self.packet_entry.grid(column=2, row=5)

        self.id_label = Label(text='ID: ')
        self.id_label.grid(column=3, row=1)
        self.id_entry = Entry()
        self.id_entry.grid(column=4, row=1)

        self.location_label = Label(text='Location: ')
        self.location_label.grid(column=3, row=2)
        self.location_entry = Combobox()
        self.location_entry.config({'value':'Office Garage'})
        self.location_entry.grid(column=4, row=2)        

        self.supplier_price_label = Label(text='Supplier Price: ')
        self.supplier_price_label.grid(column=3, row=3)
        self.supplier_price_entry = Entry()
        self.supplier_price_entry.grid(column=4, row=3)        

        self.sell_price_label = Label(text='Sell Price: ')
        self.sell_price_label.grid(column=3, row=4)
        self.sell_price_entry = Entry()
        self.location_entry.grid(column=4, row=4)        

        self.measured_by_label = Label(text='Measured By: ')
        self.measured_by_label.grid(column=3, row=5)
        self.measured_by_entry = Combobox()
        self.measured_by_entry.config({'value':'Item Metre'})
        self.measured_by_entry.grid(column=4, row=5)


root = Tk()
app = App(master=root)
app.mainloop()