
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
    TODO: document _attributes.
    TODO: methods allowed?
    TODO: append attribute docstrings to class docstring?
    '''

    def __init__(self, source=None, **kwargs):
        """Create from a source object and/or keyword arguments.
        
        If the source argument is given the fields will be
        initialized from equally named fields in the source object.
        This for example allows the value object to be created
        from a named tuple. If the source object has fields that
        are not defined in the value object they will be ignored.
        
        Alternatively the objects can be initialized by supplying the
        names and values as keyword arguments.
        
        If both a source object and keyword arguments are given the
        keyword arguments supplement or overwrite the values from the
        source object. This allows the user to create a modified
        version of a value object by supplying the original as the
        source object and overwriting values as needed with
        keyword arguments.

        If the value object defines an attribute that is not present
        in either the source object or the keyword arguments then
        an AttributeError is raised. Extra keyword arguments that
        are not known to the value object are silently ignored.
        
        TODO: examples.
        """
        for name in self._attributes:
            if name in kwargs:
                value = kwargs[name]
            elif source:
                value = getattr(source, name)
            else:
                raise AttributeError("Attribute '{}' not specified."
                        .format(name))
            setattr(self, name, value)

    @classmethod
    def Mutable(cls, source=None, **kwargs):
        """Return an instance of a mutable version of the value object.
        
        TODO: detailed description.
        """
        class MutableValue:
            def __init__(self, source=None, **kwargs):
                if source:
                    for name in source._attributes:
                        setattr(self, name, getattr(source, name))
                for name, value in kwargs.items():
                    setattr(self, name, value)

            def immutable(self):
                return cls(self)
        return MutableValue(source, **kwargs)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        for name in self._attributes:
            if getattr(self, name) != getattr(other, name):
                return False
        return True

    def __setattr__(self, name, value):
        if name in self.__dict__ or name not in self._attributes:
            raise AttributeError()
        else:
            super().__setattr__(name, value)

    def __str__(self):
        attributes = ','.join('{}={}'.format(name, getattr(self, name))
                for name in self._attributes)
        return '{}({})'.format(type(self).__name__, attributes)

    def __repr__(self):
        attributes = ','.join('{}={}'.format(name, repr(getattr(self, name)))
                for name in self._attributes)
        return '{}({})'.format(type(self).__name__, attributes)
