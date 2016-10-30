import unittest

from test import util

import components.ezvalue


class Foo(components.ezvalue.Value):
    """Class docstring."""
    bar = """Docstring 1."""
    baz = """Docstring 2."""


class TestValueObject(util.TestCase):
    def test_list_fields(self):
        self.assertCountEqual(Foo._fields, ('bar', 'baz'))

    def test_init_immutable_with_kwargs(self):
        foo = Foo(bar=1, baz='hi')
        self.assertEqual(foo.bar, 1)
        self.assertEqual(foo.baz, 'hi')

    def test_setting_immutables_attribute_raises_exception(self):
        foo = Foo(bar=1, baz='hi')
        with self.assertRaises(AttributeError):
            foo.bar = 3

    def test_non_extisting_attribute_raises_exception(self):
        foo = Foo(bar=1, baz='hi')
        with self.assertRaises(AttributeError):
            foo.non_existing = 'hi'

    def test_instantiate_mutable_class(self):
        mutable_foo = Foo.Mutable()
        mutable_foo.bar = 1
