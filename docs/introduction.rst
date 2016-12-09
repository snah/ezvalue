************
Introduction
************

ezvalue (pronounced 'easy value') provides an elegant yet powerful
implementation of value objects.

Value objects
=============

A value object is a *simple* *immutable* object whose equality is based on
*value* rather than identity\ [#wiki_value_object]_.

This definition can be broken down into three basic components:

Simple:
    The object should represent a concept that is easy to understand and
    explain. Also it should ideally contain no business logic at all.

Value base equality:
    Two objects of the same type should compare equal if and only if the value
    of the objects are the same. The fact that they may be stored in different
    locations should be irrelevant.

Immutable:
    It should be impossible to change the value of the object after it is
    created. This makes it easy and less error prone to work with value
    objects.

The Python Standard Library defines various value objects out of box like int,
float, tuple and string. However there is no elegant way of defining your own
value objects in python. There is collections.NamedTuple, but the syntax can
hardly be called elegant, especially with more than two or three attributes.

Value objects with ezvalue
==========================

The ezvalue library lets the user define new value objects by creating a
subclass and defining class attributes. The resulting value object can be used
similarly to a named tuple, but has additional features. For example ezvalue
value object have more flexible constructors an it is possible to create a
mutable copy of the value object.

The :doc:`tutorial` provides an introduction on how to use ezvalue objects.


.. rubric:: Footnotes

.. [#wiki_value_object]  Paraphrased from `wikipedia
    <https://en.wikipedia.org/wiki/Value_object>`_.
