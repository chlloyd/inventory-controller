from database import _db

if __name__ == '__main__':
    

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
        _db.add_item_from_spreadsheet(*a) # This method no longer exists
    file.close()
    _db.close()
