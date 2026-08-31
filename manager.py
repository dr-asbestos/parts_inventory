from comp_defs import *
import pickle
from copy import copy

class Manager:
    def __init__(self, db_path=None, db=None):
        self.db_path = db_path
        self.db = [] if db is None else db

    def load_db(self):
        '''Loads the pickled database from filepath.'''
        try:
            with open(self.db_path, mode='rb') as file:
                self.db = pickle.load(file)
                print(f"Loaded database file: {self.db_path}")
        except Exception as e:
            print(f'An error occurred when loading {self.db_path}: {e}')
            self.db_path = None

    def save_db(self):
        '''Pickles the database to filepath.'''
        try:
            with open(self.db_path, mode='wb') as file:
                pickle.dump(self.db, file)
                print(f"Saved database file: {self.db_path}")
        except Exception as e:
            print(f'An error occurred when saving {self.db_path}: {e}')
    
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
        # get a valid component name, retry if failed
        while (new_comp := get_component(input('Enter component class: '))) is None:
            pass
        new_comp = new_comp()
        for field in new_comp.get_all_fields():
            # set id automatically
            if field == 'id':
                new_comp.set_fields({'id': self.get_next_id()})
            # get a positive integer for quantity, retry if failed
            elif field == 'qty':
                while not (qty := input('Enter quantity: ')).isdigit():
                    pass
                new_comp.set_fields({'qty': int(qty)})
            # everything looks good, set the field
            else:
                val = input(f"Enter {field}: ")
                try:
                    val = float(val) # if its a number, keep it a number
                except:
                    pass
                new_comp.set_fields({field: val})

        # sanity check for the user
        while (reply := input(f"Add the following component? (y/n)\n{repr(new_comp)}\n").lower()) not in 'yn':
            pass
        # now acually add the new component
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

    def edit_component(self, id=None, field=None, value=None, sudo=False):
        '''Prompts the user for component ID and fields to edit. The entries 
        are checked for validity, and in case of success, the field's value is 
        updated accordingly. '''
        # get a valid component ID, ie one that exists, ie positive integer 
        # and present in the database
        if sudo:
            print('WARNING! ID editing is enabled, proceed at your own risk!')
        
        try:
            if id is None:
                id = input("Enter component ID: ")
            index = self.get_comp_index_by_id(int(id))
            if index == -1:
                raise
        except:
            print(f"Invalid ID or component not found: {id}")
            return
        
        print(f"Currently editing:\n{repr(self.db[index])}\nID editable: {sudo}")
        # keep asking user for fields, skip the routine and retry if one of 
        # the validity checks fails
        while True:
            if field is None: # ask if field wasnt specified or this is a retry
                field = input('Enter field name to edit, leave entry blank to finish editing: ')

            if field == '': # done editing
                break

            if field not in self.db[index].get_all_fields():
                print(f"Invalid field: {field}")
                field = None
            else:
                if field == 'id' and not sudo:
                    print("Cannot edit ID.")
                    field = None
                    continue

                if value is None:
                    value = input(f"Enter value for {field}: ")

                if (field == 'qty' or field == 'id'): # the two fields that must be an integer
                    if value.isdigit():
                        value = int(value)
                        if field == 'id' and value in (comp.id for comp in self.db):
                            print(f"ID already present: {value}")
                            field, value = None, None
                            continue
                    else:
                        print(f"Invalid value: {value}")
                        field, value = None, None
                        continue
                
                # now actually set the field
                self.db[index].set_fields({field: value})
                print(f" Set {field} to {value}")
                field, value = None, None
        print(f"Finished editing:\n{repr(self.db[index])}")

    def clone_component(self, id=None, verbose=False):
        '''Duplicate an item with a new ID.'''
        try:
            index = self.get_comp_index_by_id(int(id))
            if index == -1:
                raise
        except:
            print(f"Invalid ID or component not found: {id}")
            return

        new_comp = copy(self.db[index])
        new_comp.set_fields({'id': self.get_next_id()})
        self.db.append(new_comp)
        self.sort_db()
        print('Added new component.')
        if verbose:
            print(repr(new_comp))
        else:
            print(str(new_comp))


    def delete_component(self, id=None):
        '''Prompts the user for component ID and on positive confirmation 
        deletes the component from the database.'''
        try:
            if id is None:
                id = input("Enter component ID: ")
            index = self.get_comp_index_by_id(int(id))
            if index == -1:
                raise
        except:
            print(f"Invalid ID or component not found: {id}")
            return

        # sanity check for the user
        while (reply := input(f"Delete the following component? (y/n)\n{repr(self.db[index])}\n").lower()) not in 'yn':
            pass
        if reply == 'y':
            self.db.pop(index)
            self.sort_db()
            print('Deleted component.')
        else:
            print('Operation aborted.')

    def find_component(self, prompt, clss=None, fields=None):
        '''Returns a list of components that satisfy search paramenters.'''
        found_comps = self.db

        # filter by classes
        if clss is not None: 
            clss = list(get_component(cls) for cls in clss)
            found_comps = list(filter(lambda x: type(x) in clss, found_comps))

        # filter by fields
        def _fields_filter(x): # too complicated for lambda
            for f in x.get_all_fields():
                if f in fields:
                    return True
            return False
        if fields is not None:
            found_comps = list(filter(_fields_filter, found_comps))

        # filter by prompt
        def _prompt_filter(x): # too complicated for lambda
            _fields = x.get_all_fields() if fields is None else fields
            for f in _fields:
                if prompt in str(getattr(x, f, '')): 
                    return True
            return False
        found_comps = list(filter(_prompt_filter, found_comps))

        # print results
        print(*(str(comp) for comp in found_comps), sep='\n')

    def view_component(self, id=None, verbose=False):
        '''Prints component fields.'''
        try:
            index = self.get_comp_index_by_id(int(id))
            if index == -1:
                raise
        except:
            print(f"Invalid ID or component not found: {id}")
            return
        
        if verbose:
            print(repr(self.db[index]))
        else:
            print(str(self.db[index]))
    
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

    def print_component_tree(self, cls=Component, tab=0):
        '''Prints foramtted component definitions tree.'''
        mark = "|---" if tab > 0 else ""
        print(f"{'|   ' * (tab-1)}{mark}{cls.__name__}: {cls.__slots__}")
        for subcls in cls.__subclasses__():
            self.print_component_tree(subcls, tab+1)
            
    
