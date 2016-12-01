************
Introduction
************

ezvalue (pronounced 'easy value') provides an elegant yet powerful
implementation of value objects.

=============
Value Objects
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
float, tuple and string.

========================
Example of using ezvalue
========================

TODO

.. rubric:: Footnotes

.. [#wiki_value_object]  Paraphrased from `wikipedia <https://en.wikipedia.org/wiki/Value_object>`_.
