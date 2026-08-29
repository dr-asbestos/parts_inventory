#!/usr/bin/python3

from cmd import Cmd
from pathlib import Path
from manager import Manager

class ManagerCLI(Cmd):
    '''todo: write me'''
    prompt = 'Mngr>> '
    intro = 'Electronic Parts Inventory Manager v1.0.0\nType "help" for available commands'
    
    def __init__(self, spacing=' '):
        super().__init__()
        self.mngr = Manager()
        self.paths = list(Path().glob('*.bin'))
        self.spacing = spacing
        self.saved = True
    
    def do_hi(self, line):
        '''Just a test command.'''
        print(line, type(line))

    def do_load(self, _):
        '''Loads database from file.'''
        self.paths = list(Path().glob('*.bin'))
        if not self.saved: # prompt user before they discard all the changes
            while (reply := input(f"Save the database before loading another? (y/n): ")) not in 'yn':
                pass
            if reply == 'y':
                self.do_save(None)
        if len(self.paths) == 0:
            print('No database files found!')
            return
        print('Select file to load (leave entry blank to abort): ')
        for i, path in enumerate(self.paths):
            print(f'{i}: {path}')
        while True:
            select = input()
            try:
                if select == '':
                    print('Load aborted.')
                    return
                select = int(select)
                if select not in range(len(self.paths)):
                    raise
                break
            except:
                print('Invalid selection!')
                continue
        
        self.mngr.db_path = self.paths[select]
        self.mngr.load_db()
        self.saved = True
    
    def do_save(self, _):
        '''Saves current database to file.'''
        if self.mngr.db_path is None:
            self.do_saveas(None)
        else:
            self.mngr.save_db()
            self.saved = True

    def do_saveas(self, _):
        '''Saves a new database to file.'''
        illegal_chars = r'<>:"/\|?*'
        while True:
            name = input('Please enter new file name: ')
            for c in illegal_chars:
                if c in name:
                    print('Illegal file name!')
                    continue

            break
        self.mngr.db_path = f'{name}.bin'
        self.do_save(None)
    
    def do_printdb(self, _):
        '''Prints whole database. For debugging purposes.'''
        print(f'Path: {self.mngr.db_path}')
        print(*(str(comp) for comp in self.mngr.db), sep='\n')

    def do_printdefs(self, _):
        '''Prints component definitions tree.'''
        self.mngr.print_component_tree()
    
    def do_add(self, _):
        '''Launches a dialogue to add a new component to the database.'''
        self.mngr.add_new_component()
        self.saved = False
    
    def do_edit(self, line):
        '''Launches a dialogue to edit an existing component.'''
        tokens = line.split()
        if len(tokens) == 0:
            tokens.append(None)
        if len(tokens) == 1:
            tokens.append(False)
        else:
            tokens[1] = tokens[1] == 'sudo'
        
        self.mngr.edit_component(tokens[0], tokens[1])
        self.saved = False

    def do_delete(self, id):
        '''Launches a dialogue to delete an existing component.'''
        self.mngr.delete_component(id)
        self.saved = False

    def do_shell(self, line):
        '''Execute arbitrary Python code and prints return value. Command `!' 
        is synonym for 'shell'. Command `!!' wraps the code in a `print()'. 
        For debugging purposes only. Don't do anything naughty. pls. '''
        try:
            if line[0] == '!': # for !!
                exec(f"print({line[1:]})")
            else:
                exec(line)
        except Exception as e:
            print(e)
    
    def do_line_spacer(self, line):
        '''Change line spacing settings. Leave entry blank for no spacing. 
        Enter `blank' for blank like spacing. Enter single character to make 
        that character a ruler. '''
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
        response to the prompt. Currently just passes.'''
        pass

    def default(self, line):
        '''Class method override. Called when the command prefix is not 
        recognized. Currently just informs the user.'''
        print(f'Unknown command: {line}')
        pass
    
    def postcmd(self, stop, line):
        '''Class method override. Called right after a command dispatch is 
        finished. Currently prints spacing line and prompts user on exit. '''
        if self.spacing is not None:
            print(self.spacing * 40)

        # prompt user if they actually want to quit and if they want to 
        # discard all the changes to the database
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
    ManagerCLI().cmdloop()