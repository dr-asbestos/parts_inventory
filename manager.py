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
        ''' Prompts the user for name and field values for a new component. 
        The user is then presented with new component fields and confirms the 
        adition to the database. In case of positive confirmation, the new 
        component is added and `sort_db' is called. The `id' field is set 
        automatically. The `qty' field must be a positive integer. Other 
        fields are cast to float if possible. '''
        while (new_comp := get_component(input('Enter component name: '))) is None:
            pass
        new_comp = new_comp()
        for field in new_comp.get_all_fields():
            if field == 'id':
                new_comp.set_fields({'id': self.get_next_id()})
            elif field == 'qty':
                while not (qty := input('Enter quantity: ')).isdigit():
                    pass
                new_comp.set_fields({'qty': int(qty)})
            else:
                val = input(f"Enter {field}: ")
                try:
                    val = float(val)
                except:
                    pass
                new_comp.set_fields({field: val})

        while (reply := input(f"Add the following component? (y/n)\n{repr(new_comp)}\n").lower()) not in 'yn':
            pass

        if reply == 'y':
            self.db.append(new_comp)
            self.sort_db()
            print('Added new component.')
        else:
            print('Opertion aborted.')
    
    def get_comp_index_by_id(self, comp_id):
        '''Returns component's index within the database by given component 
        id. Returns -1 if component is not found.'''
        for index, comp in enumerate(self.db):
            if comp.id == comp_id:
                return index
        return -1

    def edit_component(self, sudo=False):
        
        # get a valid component ID, ie one that exists, ie positive integer 
        # and present in the database
        index = -1
        while True:
            try:
                entry = input("Enter component ID: ")
                index = self.get_comp_index_by_id(int(entry))
                if index == -1:
                    raise
                break
            except:
                print(f"Invalid ID or component not found: {entry}")
        
        
        print(f"Currently editing:\n{self.db[index]}\nID editable: {sudo}")
        while (field := input('Enter field name to edit, leave entry blank to finish editing: ')) != '':
            if field not in self.db[index].get_all_field:
                print(f"Invalid field: {field}")
            else:
                if field == 'id' and not sudo:
                    print("Cannot edit ID.")
                    continue
                val = input("Enter value for {field}: ")
                if field == 'qty' and not val.isdigit():
                    print("Invalid quantity: {val}")
                    continue
                self.db[index].set_fields({field: val})
                print(F" Set {field} to {val}")
        print(f"Finished editing:\n{self.db[index]}")

            



        

    def get_next_id(self):
        '''Returns next available component ID in the database. Calls 
        `sort_db()' before execution.'''
        self.sort_db()
        id_list = [comp.id for comp in self.db]
        next_id = len(id_list)
        for i, id in enumerate(id_list):
            if i != id:
                next_id = i
                break
        return next_id
        
