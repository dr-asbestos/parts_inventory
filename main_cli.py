#!/usr/bin/python3

from cmd import Cmd
from pathlib import Path
from argparse import ArgumentParser
from inspect import cleandoc
from manager import Manager

class ManagerCLI(Cmd):
    '''todo: write me'''
    prompt = 'Mngr>> '
    intro = 'Electronic Parts Inventory Manager v1.0.0\nType "help" for available commands'

    parser_edit = ArgumentParser(prog='edit')
    parser_edit.add_argument('-s', '--sudo', action='store_true', help='Allow ID editing. Use at your own risk.')
    parser_edit.add_argument('-i', '--id', type=int, help='Select item by ID. If not specified, enter dialogue.')
    parser_edit.add_argument('-f', '--field', type=str, help='Select item field, must use -i.')
    parser_edit.add_argument('-v', '--value', type=str, help='Specify new field value, must use -f.')

    parser_delete = ArgumentParser(prog='delete')
    parser_delete.add_argument('-i', '--id', type=int, help='Select item to delete by ID. If not specified, enter dialogue.')

    parser_find = ArgumentParser(prog='find', usage='find [-h] [prompt] [-f FIELDS [FIELDS ...]] [-c CLSS [CLSS ...]]')
    parser_find.add_argument('prompt', nargs='?', default='', help='Search prompt, can be blank.')
    parser_find.add_argument('-f', '--fields', nargs='+', help='Search within specified fields.')
    parser_find.add_argument('-c', '--clss', nargs='+', help='Search through specified classes.')
    # this is for when i decide i really want the subclasses too. 
    #group = parser_find.add_mutually_exclusive_group()
    #group.add_argument('-c', '--class', nargs='+', help='Search through specified classes and their subclasses.')
    #group.add_argument('-C', '--class-strict', nargs='+', help='Search through specified classes.')

    parser_view = ArgumentParser(prog='view')
    parser_view.add_argument('id', type=int, help='Select item to view by ID.')
    parser_view.add_argument('-v', '--verbose', action='store_true', help='More detailed view on the item.')

    
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

    def help_edit(self):
        '''Prints help for `do_edit'.'''
        print(cleandoc(self.do_edit.__doc__))
        self.parser_edit.print_help()
    
    def do_edit(self, line):
        '''Launches a dialogue to edit an existing component.'''
        try:
            args = self.parser_edit.parse_args(line.split())
            if args.id is None and args.field:
                self.parser_edit.error('--id required for --field')
            if args.field is None and args.value:
                self.parser_edit.error('--field required for --value')

        except SystemExit:
            pass
        else:
            self.mngr.edit_component(**args.__dict__)
            self.saved = False

    def help_delete(self):
        '''Prints help for `do_delete'.'''
        print(cleandoc(self.do_delete.__doc__))
        self.parser_delete.print_help()
    
    def do_delete(self, line):
        '''Launches a dialogue to delete an existing component.'''
        try:
            args = self.parser_delete.parse_args(line.split())
        except SystemExit:
            pass
        else:
            self.mngr.delete_component(args.id)
            self.saved = False

    def help_find(self):
        '''Prints help for `do_find'.'''
        print(cleandoc(self.do_find.__doc__))
        self.parser_find.print_help()

    def do_find(self, line):
        '''Database search function.'''
        try:
            args = self.parser_find.parse_args(line.split())
        except SystemExit:
            pass
        else:
            self.mngr.find_component(**args.__dict__)

    def help_view(self):
        '''Prints help for `do_view'.'''
        print(cleandoc(self.do_view.__doc__))
        self.parser_view.print_help()

    def do_view(self, line):
        '''Show item details.'''
        try:
            args = self.parser_view.parse_args(line.split())
        except SystemExit:
            pass
        else:
            self.mngr.view_component(**args.__dict__)

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
            while (reply := input(f"Are you sure you want to quit? (y/n): ").lower()) not in 'yn':
                pass
            if reply == 'y':
                if not self.saved:
                    while (reply := input(f"Save the database before quitting? (y/n): ").lower()) not in 'yn':
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