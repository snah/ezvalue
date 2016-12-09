********
Tutorial
********

This document is intended as a quick introduction to creating and
using ezvalue value objects. After going through this tutorial you
will be able to effectively use ezvalue value objects and understand
code that uses them.

.. TODO: Add links to API doc and mention them here.
.. TODO: Add estimated time to go through tutorial.

Creating value objects
======================

New value objects are created by subclassing :class:`ezvalue.Value`::

    import ezvalue
    class Point(ezvalue.Value):
        """Defines a cartesian point in 2D space."""
        
        x = """The x-coordinate in meters."""
        y = """The y-coordinate in meters."""

The class docstring should be used to document the value object and strings
should be assigned to the class attributes to document them. After defining
the value object it can be instantiated and used as follows::

    >>> my_point = Point(x=1, y=13)
    >>> my_point.x
    1
    >>> my_point.y
    13

Note that value objects are immutable::

    >>> my_point.x = 2
    Traceback (most recent call last):
      File "<input>", line 1, in <module>
      File "ezvalue/__init__.py", line 270, in __setattr__
        raise AttributeError()
    AttributeError

It is however very simple to create a modified copy of the value
object::

    >>> different_point = Point(my_point, x=2)
    >>> different_point.x
    2
    >>> different_point.y
    13

As you can see a value object can take another object as it's first parameter
to be used as a source object, any keyword arguments provided will overwrite
the values of the source object.

Equality of value objects
=========================

:meth:`Equality <ezvalue.Value.__eq__>` of value objects is based on their
value::

    >>> my_point == Point(x=1, y=13)
    True
    >>> my_point == Point(x=2, y=13)
    False

Value objects are never equal to objects of a different type with exception of
their mutable companion classes which will be introduced below::

    >>> from collections import namedtuple
    >>> NamedTuple = namedtuple(my_point == NamedTuple(x=1, y=13)
    False

If you must compare to another object with the same attributes you can convert
it to a value object first::

    >>> my_point == Point(NamedTuple(x=1, y=13))
    True

Mutable value objects
=====================

Value objects should normally be immutable for various good reasons
[#fowler_value_object]_ however there are times that mutable value objects are
useful. One such situation can occur when working with code that is outside
your control. Suppose you need to use a function that takes a point and inverts
it's x-coordinate::

    def invert_x(point):
        point.x = -point.x

If you would supply this function with an instance of the Point class we
defined above it would raise an AttributeError::

    >>> invert_x(my_point)
    Traceback (most recent call last):
      File "<input>", line 1, in <module>
      File "<input>", line 2, in move_left
      File "ezvalue/__init__.py", line 270, in __setattr__
        raise AttributeError()
    AttributeError

However you can create a :meth:`mutable <ezvalue.Value.mutable>` copy of the
object and pass that to the function::

    >>> my_mutable_point = my_point.mutable()
    >>> invert_x(my_mutable_point)
    >>> my_mutable_point
    MutablePoint(x=-1,y=13)

The mutable point can easily be converted back to an
:meth:`immutable <ezvalue._MutableValueBase.immutable>` object::

    >>> my_mutable_point.immutable()
    Point(x=0,y=13)

If you are able to modify the function it would however be better to modify it
to return a new point::

    def inverted_x(point):
        return Point(point, x=-point.x)

Note that the function was also renamed to describe the new functionality. It
can then be used as follows::

    >>> my_inverted_point = inverted_x(my_point)
    >>> my_inverted_point
    Point(x=-1,y=13)


.. rubric:: Footnotes

.. [#fowler_value_object] See `this post by Martin fowler
    <http://martinfowler.com/bliki/ValueObject.html>`_ for a very good
    discussion of value objects and why they should be immutable.
