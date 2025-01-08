from comp_defs import *
import pickle

path = 'inventory.bin'

class Manager:
    def __init__(self, path, db=None):
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


def main():
    test = get_component('bjt')() 
    print(test.get_all_fields())
    print(test.get_empty_fields())
    print(test.get_inheritance())



if __name__ == '__main__':
    main()