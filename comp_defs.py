"""
Class definitions for different types of components, with certain amount of 
common inherited properties from each other. 
"""

class Component:
    '''
    Generic component definition
    '''
    def __init__(self):
        self.id = None
        self.package = None
        self.description = None

    def set_field(self, field, value):
        '''Dedicated field setter method. Avoid setting fields manually.'''
        if hasattr(self, field):
            setattr(self, field, value)
        else:
            raise AttributeError(f"{self.__class__.__name__} component has no field '{field}'.")

class Resistor(Component):
    '''
    Resistor definition
    '''
    def __init__(self):
        super().__init__()
        self.value = None
        self.power = None



# testing bits on the go
test = Resistor()
test.set_field('value', 123)
print(test.value)
test.set_field('asdf', 1234)