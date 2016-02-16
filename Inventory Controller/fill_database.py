import Database

if __name__ == '__main__':
    
    db = Database.InventoryDatabase('database.db')
    file = open('database_file.txt','r')
    firstline = True
    print('lets begin')
    for line in file.read().split('\n'):
        if firstline:
            firstline = False
            continue
        a = line.split('$')
        if a == ['']:
            break
        db.add_item_from_spreadsheet(*a)

    file.close()
    db.close()
