
class ValueMeta(type):
    def __init__(cls, name, bases, namespace):
        attributes = {name for name in cls.__dict__
                if not name.startswith('_')}
        attributes -= {'Mutable'}
        cls._attributes = attributes


class Value(metaclass=ValueMeta):
    '''Subclass this to define a new value object.
    
    The Value class is intended to be subclassed by the user to
    define a new value object. Alternatively the class can be
    instantiated directly to create an empty value object.

    To define a new value object the user should define a new class
    that inherits from this class. The attributes of the value object
    are defined by defining class attributes with the desired names
    in the subclass body. The value of the attributes should be a
    docstring describing the attribute. Valid attribute names are
    any valid python variable name not starting with an underscore.

    Example:
    TODO
    
    Note: If the inherited class specifies a metaclass than the
    metaclass must inherit from ValueMeta.

    The resulting value object is in immutable object with the
    specified attributes. Attempting to assign a value to an
    attribute or creating a new attribute will raise an
    AttributeError.

    TODO: summerize functionality.
    TODO: methods allowed?
    TODO: append attribute docstrings to class docstring?
    '''

    def __init__(self, source=None, **kwargs):
        """Create from a source object and/or keyword arguments.
        
        If the source argument is given the fields will be
        initialized from equally named fields in the source object.
        This for example allows the value object to be created
        from a named tuple.
        
        Alternatively the objects can be initialized by supplying the
        names and values as keyword arguments.
        
        If both a source object and keyword arguments are given the
        keyword arguments supplement or overwrite the values from the
        source object. This allows the user to create a modified
        version of a value object by supplying the original as the
        source object and overwriting values as needed with
        keyword arguments.

        TODO: specify exceptions (missing/unknown attributes).
        TODO: examples.
        TODO: supplement with keyword arguments.
        """
        for name in self._attributes:
            if source:
                try:
                    value = getattr(source, name)
                except AttributeError:
                    pass
            if name in kwargs:
                value = kwargs[name]
            setattr(self, name, value)

    def __setattr__(self, name, value):
        if name in self.__dict__ or name not in self._attributes:
            raise AttributeError()
        else:
            super().__setattr__(name, value)

    @classmethod
    def Mutable(cls):
        """Return an instance of mutable version of the value object.
        
        TODO: detailed description.
        """
        class cls:
            pass
        return cls
