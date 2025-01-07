"""
Class definitions for different types of components, with certain amount of 
common inherited properties from each other. 
"""
def get_component(name):
    '''Returns a comonent class based on the given lowercase no-space string.'''
    match name:
        case 'component' | 'generic' | '':
            return Component
        case 'passive':
            return Passive
        case 'r' | 'res' | 'resistor':
            return Resistor
        case 'c' | 'cap' | 'capacitor':
            return Capacitor
        case 'i' | 'ind' | 'inductor':
            return Inductor
        case 'rv' | 'vr' | 'pot' | 'potentiometer':
            return Potentiometer
        case 'ic' | 'integrated_circuit':
            return IntegratedCircuit
        case 'analog' | 'analogue':
            return Analog
        case 'comp' | 'comparator':
            return Comparator
        case 'opamp' | 'amplifier' | 'operational_amplifier':
            return OpAmp
        case 'digital':
            return Digital
        case 'logic':
            return Logic
        case 'reg' | 'regulator' | 'linear_regulator':
            return Regulator
        case 'transistor': #i am not adding 'Q' as that is used for many different devices
            return Transistor
        case 'bjt' | 'bipolar':
            return BJT
        case 'mosfet' | 'nfet' | 'pfet' | 'nmos' | 'pmos' | 'field_effect':
            return MOSFET
        case _:
            return None


class Component:
    '''Generic component definition and functions.'''
    __slots__ = ('id', 'package', 'mount', 'desc')
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

class Potentiometer(Passive):
    __slots__ = ('taper',)
    def __init__(self):
        super().__init__()

class IntegratedCircuit(Component):
    __slots__ = ('part_number',)
    def __init__(self):
        super().__init__()

class Analog(IntegratedCircuit):
    __slots__ = ('channels',)
    def __init__(self):
        super().__init__()

class Comparator(Analog):
    __slots__ = ('output',)
    def __init__(self):
        super().__init__()

class OpAmp(Analog):
    __slots__ = ('voltage', 'rail-to-rail')
    def __init__(self):
        super().__init__()

class Digital(IntegratedCircuit):
    __slots__ = ('family',)
    def __init__(self):
        super().__init__()

class Logic(Digital):
    __slots__ = ('function',)
    def __init__(self):
        super().__init__()

class Regulator(IntegratedCircuit):
    __slots__ = ('voltage', 'current')
    def __init__(self):
        super().__init__()

class Transistor(Component):
    __slots__ = ('part_number', 'type', 'voltage', 'current') #'voltage' and 'current' are left as generic fields
    def __init__(self):
        super().__init__()

class BJT(Transistor):
    __slots__ = ('v_ceo', 'v_cbo', 'v_ebo', 'i_c', 'h_fe_min', 'h_fe_max')
    def __init__(self):
        super().__init__()

class MOSFET(Transistor):
    __slots__ = ('v_dss', 'v_dgr', 'v_gss', 'i_d', 'v_gs(th)', 'r_ds(on)')
    def __init__(self):
        super().__init__()

class JFET(Transistor):
    __slots__ = ('v_ds', 'v_gs', 'i_g', 'i_dss' 'v_gs(off)_min', 'v_gs(off_max)')
    def __init__(self):
        super().__init__()

#todo:add igbt


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
