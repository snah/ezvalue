import copy

class ValueMeta(type):
    """Meta class for creating value objects.
    
    The ValueMeta class is responsible for setting several special
    class attributes on a value class. It is the metaclass of the
    Value class, so normally the user should not have to specify
    a metaclass when creating their own value objects. However if the
    user wishes to use their own meta class for a value object they
    must make sure their meta class inherits from this class.
    """
    def __init__(cls, name, bases, namespace):
        attributes = {name for name in cls.__dict__
                if not name.startswith('_')}
        attributes -= {'Mutable', 'mutable'}
        cls._attributes = attributes

        class SubclassedMutable(_MutableValueBase):
            pass

        cls.Mutable = SubclassedMutable
        cls.Mutable.Immutable = cls
        cls.Mutable._attributes = attributes


class _MutableValueBase:
    """Base class for the mutable version of a value.
    
    This is the base class for mutable versions of value objects and
    is not meant to instatiated directly. When defining a new value
    object the Mutable attribute is autmatically set to a newly
    created subclass of this base class.

    A mutable value object has the same attributes as the immutable
    value object it is derived from, however the attributes are
    writable.
    
    Unlike an immutable value object where all the attributes must be
    supplied to the constructor, with a mutable value object it is
    possible to assign only a subset of attributes and assign the rest
    of the attributes later.
    
    Also unlike an immutable value object it is possible to define
    extra attributes like in normal python classes, for example to be
    used as temporary variables. These extra attributes will be
    ignored when creating an immutable value object from the mutable
    value object.
    """
    def __init__(self, source=None, **kwargs):
        """Create from a source object and/or keyword arguments.

        If source is given the attributes are initialized from
        equally named attributes of the source object. This means the
        class be initialized with for example an instance of the
        complementary Value class or with a named tuple. If the
        source object has attributes that are not defined in the
        Value class they are silently ignored.

        If additonal keyword argument are given they will be assigned
        to the corresponding attributes. Unlike in the Value class
        keywords that do not correspond to defined attributes will be
        added to the class as new attributes. Any attributes that
        were also present in the source object will be overwritten
        by keyword arguments.

        Contrary to the immutable value object it is not an error if
        not all of the attributes are given, indeed one of the
        porposes of the mutable version of the value object is to
        allow object creation to happen in stages.
        """
        if source:
            for name in self._attributes:
                try:
                    setattr(self, name, getattr(source, name))
                except AttributeError:
                    pass
        for name, value in kwargs.items():
            setattr(self, name, value)

    """Create an immutable value object from this mutable instance.
    
    Create an new instance of the complementary (immutable) Value
    class and pass 'self' as the source object. This has the effect
    of returning an immutable version of the object. Keep in mind
    that any assigned attributes that are not part of the Value's
    definition will not be part of the returned object.
    """
    def immutable(self):
        return self.Immutable(self)

    def __eq__(self, other):
        if type(other) not in (type(self), self.Immutable):
            return False
        for name in self._attributes:
            if getattr(self, name) != getattr(other, name):
                return False
        return True


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
    any valid python variable name not starting with an underscore
    except 'Mutable', 'mutable', 'Immutable' and 'immutable'.

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
        
        If the source argument is given the attributes will be
        initialized from equally named attributes in the source
        object. This for example allows the value object to be
        created from a named tuple. If the source object has fields
        that are not defined in the value object they will be ignored.
        
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
        are not defined in the value object are silently ignored.
        
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

    def mutable(self):
        """Return a mutable copy of the value object.
        
        Create a new instance of the complementary mutable value
        object and pass 'self' as the source object.
        """
        return self.Mutable(source=self)

    def __eq__(self, other):
        if type(other) not in (type(self), self.Mutable):
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
