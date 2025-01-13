from cmd import Cmd
from manager import Manager

class ManagerCLI(Cmd):
    '''todo: write me'''
    prompt = 'Mngr>> '
    intro = 'Electronic Parts Inventory Manager v1.0.0\nType "help" for available commands'
    
    def __init__(self, mngr, spacing=' '):
        super().__init__()
        self.mngr = mngr
        self.spacing = spacing
        self.saved = True
    
    def do_hi(self, line):
        '''Just a test command.'''
        print(line, type(line))

    def do_load(self, _):
        '''Loads database from file.'''
        if not self.saved:
            while (reply := input(f"Save the database before quitting? (y/n): ")) not in 'yn':
                pass
            if reply == 'y':
                self.do_save(None)
        self.mngr.load_db()
        self.saved = True
        print(f"Loaded database file: {self.mngr.db_path}")
    
    def do_save(self, _):
        '''Saves the database to file.'''
        self.mngr.save_db()
        self.saved = True
        print(f"Saved database file: {self.mngr.db_path}")
    
    def do_printdb(self, _):
        '''Prints whole database. For debugging purposes.'''
        print(*(repr(comp) for comp in self.mngr.db), sep='\n')
    
    def do_add(self, _):
        '''Launches a dialogue to add a new component to the database.'''
        self.mngr.add_new_component()
        self.saved = False
    
    def do_edit(self, _):
        '''Launches a dialogue to edit an existing component.'''
        self.mngr.edit_component()
        self.saved = False

    def do_shell(self, line):
        '''Execute arbitrary Python code and prints return value. Command '!' 
        is synonym for 'shell'. For debugging purposes only. Don't do 
        anything naughty. pls. '''
        try:
            print(exec(line))
        except Exception as e:
            print(e)
    def do_line_spacer(self, line):
        ''''''
        if len(line) == 0:
            self.spacing = None
        elif len(line) == 1:
            self.spacing = line
        elif line == 'blank':
            self.spacing = ' '
        else:
            print(f"Invalid line spacer: {line}")

    def emptyline(self):
        '''Class method override. Called when an empty line is entered in 
        response to the prompt.'''
        pass

    def default(self, line):
        '''Class method override. Called when the command prefix is not 
        recognized.'''
        print(f'Unknown command: {line}')
        pass
    
    def postcmd(self, stop, line):
        '''Class method override. Called right after a command dispatch is 
        finished. '''
        if self.spacing is not None:
            print(self.spacing * 40)

        if stop:
            while (reply := input(f"Are you sure you want to quit? (y/n): ")) not in 'yn':
                pass
            if reply == 'y':
                if not self.saved:
                    while (reply := input(f"Save the database before quitting? (y/n): ")) not in 'yn':
                        pass
                    if reply == 'y':
                        self.do_save(None)
                return True
            else:
                return False
        return False

    def postloop(self):
        '''Class method override. Called when the application is terminating.'''
        print('Goodbye!')

    def do_EOF(self, _):
        '''Quits Manager if EOF is encountered.'''
        return True
    
    def do_quit(self, _):
        '''Manually quit manager.'''
        return True
    


if __name__ == '__main__':
    ManagerCLI(Manager(db_path='inventory_test.bin')).cmdloop()