"""
Class definitions for different types of components, with certain amount of 
common inherited properties from each other. 
"""

class Component:
    '''
    Generic component
    '''
    def __init__(self, *, 
                 id=None, 
                 package=None, 
                 description=None):
        self.id = id
        self.package = package
        self.description = description

class Resistor(Component):
    '''
    Resistor definition
    '''
    def __init__(self, *, 
                 id=None, 
                 package=None, 
                 description=None, 
                 value=None, 
                 power=None):
        super.__init__(id=id, 
                 package=package, 
                 description=description)
        self.value = value
        self.power = power

