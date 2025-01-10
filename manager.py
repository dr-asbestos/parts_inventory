from comp_defs import *
import pickle

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
        '''TODO: refactor me to work with cli layer. 
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

    def get_next_id(self):
        self.sort_db()
        id_list = [comp.id for comp in self.db]
        next_id = len(id_list)
        for i, id in enumerate(id_list):
            if i != id:
                next_id = i
                break
        return next_id
        
