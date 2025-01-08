from comp_defs import *
import pickle

path = 'inventory.bin'
test_path = 'inventory_test.bin'

class Manager:
    def __init__(self, db_path=None, db=None):
        self.db_path = db_path
        self.db = [] if db is None else db

    def load_db(self):
        '''Loads the pickled database from filepath.'''
        try:
            with open(self.db_path, mode='rb') as file:
                self.db = pickle.load(file)
        except Exception as e:
            print(e)

    def save_db(self):
        '''Pickles the database to filepath.'''
        try:
            with open(self.db_path, mode='wb') as file:
                pickle.dump(self.db, file)
        except Exception as e:
            print(e)
    
    def sort_db(self):
        '''Sorts the loaded database in-situ by component ID.'''
        if isinstance(self.db, list):
            self.db.sort(key=lambda x: x.id)

    def add_new_component(self):
        '''TODO: refactor me. 
        Prompts the user for name and field values for a new component 
        and adds it to the database. '''
        new_comp = None
        while new_comp is None:
            new_comp = get_component(input('Component name: '))
        new_comp = new_comp() 
        for field in new_comp.get_all_fields():
            new_comp.set_fields({field: input(f"Enter {field}: ")})
        self.db.append(new_comp)
        print(f"Added: {repr(new_comp)}")
        

def main():
    test_mngr = Manager(db_path=test_path)
    test_mngr.load_db()
    #print(test_mngr.db)
    print(*test_mngr.db, sep='\n')
    test_mngr.db[1].id = 777
    print(*test_mngr.db, sep='\n')

    quit()


    mngr = Manager(db_path=test_path)
    while input('do stuff?') == 'y':
        mngr.add_new_component()

    mngr.save_db()

    new_mngr = Manager(db_path=test_path)
    new_mngr.load_db()

    print(*(repr(comp) for comp in new_mngr.db), sep='\n')





    '''
    test = get_component('opamp')() 
    print(test.get_all_fields())
    print(test.get_empty_fields())
    print(test.get_inheritance())
    test.id = 1234
    print(test.get_fields_dict())
    '''



if __name__ == '__main__':
    main()