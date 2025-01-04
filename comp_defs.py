"""
Class definitions for different types of components, with certain amount of 
common inherited properties from each other. 
"""

class Component:
    '''Generic component definition and functions.'''
    def __init__(self):
        self.id = None
        self.mount = None
        self.desc = None

    def set_field(self, field, value):
        '''Dedicated field setter method. Avoid setting fields manually.'''
        if hasattr(self, field):
            setattr(self, field, value)
        else:
            raise AttributeError(f"{self.__class__.__name__} component has no field '{field}'.")
    
    def get_all_fields(self):
        '''Return a dictionary of all fields assossiated with this component.'''
        return vars(self)
    
    def get_empty_fields(self):
        '''Return a list of all fields that are None.'''
        return [field for field, value in self.get_all_fields().items() if value is None]

    def get_inheritance(self, raw=False):
        '''Returns the inheritance chain list  of the component in form of 
        string names. Set 'raw' to True to return class references instead.'''
        if raw:
            return list(self.__class__.__mro__)
        else:
            return [cls.__name__ for cls in self.__class__.__mro__]
        
class Passive(Component):
    def __init__(self):
        super().__init__()
        self.value = None
        self.type = None

class Resistor(Passive):
    def __init__(self):
        super().__init__()
        self.power = None

class Capacitor(Passive):
    def __init__(self):
        super().__init()
        self.voltage = None

class Inductor(Passive):
    def __init__(self):
        super().__init__()
        self.geometry = None
        self.current = None

class IntegratedCircuit(Component):
    def __init__(self):
        super().__init__()
        self.number = None
        pass #tbd

class Analog(IntegratedCircuit):
    def __init__(self):
        super().__init__()
        pass #tbd

class Digital(IntegratedCircuit):
    def __init__(self):
        super().__init__()
        self.family = None
        pass #tbd

class Logic(Digital):
    def __init__(self):
        super().__init__()
        pass #tbd

class Regulator(IntegratedCircuit):
    def __init__(self):
        super().__init__()
        self.voltage = None
        self.current = None
        pass #tbd



# testing bits on the go
test = Resistor()
test.set_field('value', 123)
test.set_field('power', 0.25)
print(test.get_all_fields())
print(test.get_empty_fields())
print(test.get_inheritance())
print(test.get_inheritance(raw=True))