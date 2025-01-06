"""
Class definitions for different types of components, with certain amount of 
common inherited properties from each other. 
"""

class Component:
    '''Generic component definition and functions.'''
    __slots__ = ('id', 'mount', 'desc')
    def __init__(self):
        '''Dynamically create all class attributes/fields from __slots__.'''
        for slots in (getattr(cls, '__slots__', ()) for cls in self.__class__.__mro__):
            for slot in slots:
                setattr(self, slot, None)

    def set_fields(self, fields):
        '''Takes a dictionary of fields and values, and sets this component's 
        fields and values. Raises AttribureError in case of failure.'''
        for field, value in fields.items():
            setattr(self, field, value)
    
    def get_all_fields(self):
        '''Return a list of all fields assossiated with this component.'''
        slots = []
        for cls in self.__class__.__mro__:
            slots += getattr(cls, '__slots__', [])
        return slots
    
    def get_empty_fields(self):
        '''Return a list of all fields that are None.'''
        return [field for field in self.get_all_fields() if getattr(self, field, None) is None]

    def get_inheritance(self, raw=False):
        '''Returns the inheritance chain list  of the component in form of 
        string names. Set 'raw' to True to return class references instead.'''
        if raw:
            return list(self.__class__.__mro__)
        else:
            return [cls.__name__ for cls in self.__class__.__mro__]
    
class Passive(Component):
    __slots__ = ('value', 'type')
    def __init__(self):
        super().__init__()

class Resistor(Passive):
    __slots__ = ('power',)
    def __init__(self):
        super().__init__()

class Capacitor(Passive):
    __slots__ = ('voltage',)
    def __init__(self):
        super().__init()

class Inductor(Passive):
    __slots__ = ('geometry', 'current')
    def __init__(self):
        super().__init__()

class IntegratedCircuit(Component):
    __slots__ = ('number',)
    def __init__(self):
        super().__init__()

class Analog(IntegratedCircuit):
    __slots__ = ()
    def __init__(self):
        super().__init__()

class Digital(IntegratedCircuit):
    __slots__ = ('family',)
    def __init__(self):
        super().__init__()

class Logic(Digital):
    __slots__ = ()
    def __init__(self):
        super().__init__()

class Regulator(IntegratedCircuit):
    __slots__ = ('voltage', 'current')
    def __init__(self):
        super().__init__()



# testing bits on the go
test = Resistor()
test.set_fields({'value': 123, 'power': 0.25})
test.id = 999

print(test.get_all_fields())
print(test.get_empty_fields())
print(test.get_inheritance())
print(test.get_inheritance(raw=True))

try:
    test.set_fields({'haha': 777})
except Exception as e:
    print(e)

try:
    test.haha = 777
except Exception as e:
    print(e)
