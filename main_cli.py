from cmd import Cmd
from manager import Manager

class ManagerCLI(Cmd):
    '''todo: write me'''
    prompt = 'Mngr>> '
    intro = 'Electronic Parts Inventory Manager v1.0.0\nType "help" for available commands'
    
    def __init__(self, mngr):
        super().__init__()
        self.mngr = mngr
    
    def do_hi(self, line):
        '''Just a test command.'''
        print(line, type(line))

    def do_load(self, _):
        '''Loads database from file.'''
        self.mngr.load_db()
        print(f"Loaded database file: {self.mngr.db_path}")
    
    def do_printdb(self, _):
        '''Prints whole database. For debugging purposes.'''
        print(*(repr(comp) for comp in self.mngr.db), sep='\n')

    def emptyline(self):
        pass

    def default(self, line):
        print(f'Unknown command: {line}')
        pass
    
    def postloop(self):
        print('Goodbye!')
    
    def do_EOF(self, _):
        '''Quits Manager if EOF is encountered.'''
        return True
    
    def do_quit(self, _):
        '''Manually quit manager.'''
        return True
    


if __name__ == '__main__':
    ManagerCLI(Manager(db_path='inventory_test.bin')).cmdloop()