from comp_defs import *
import pickle

path = 'inventory.bin'
test_path = 'inventory_test.bin'

class Manager:
    def __init__(self, path=None, db=None):
        self.db_path = path
        self.db = db

    def load_db(self):
        try:
            with open(self.db_path, mode='rb') as file:
                self.db = pickle.load(file)
        except Exception as e:
            print(e)

    def save_db(self):
        try:
            with open(self.db_path, mode='wb') as file:
                pickle.dump(self.db, file)
        except Exception as e:
            print(e)
    
    def sort_db(self):
        if isinstance(self.db, list):
            self.db.sort(key=lambda x: x.id)


def main():
    test = get_component('opamp')() 
    print(test.get_all_fields())
    print(test.get_empty_fields())
    print(test.get_inheritance())
    test.id = 1234
    print(test.get_fields_dict())



if __name__ == '__main__':
    main()