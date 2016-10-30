
class ValueMeta(type):
    def __init__(cls, name, bases, namespace):
        attributes = tuple(name for name in cls.__dict__
                if not name.startswith('_'))
        cls._fields = attributes


class Value(metaclass=ValueMeta):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __setattr__(self, name, value):
        if name in self.__dict__ or name not in self._fields:
            raise AttributeError()
        else:
            super().__setattr__(name, value)

    @classmethod
    def Mutable(cls):
        class cls:
            pass
        return cls
