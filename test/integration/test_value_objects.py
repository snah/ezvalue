import unittest

from test import util

import components.ezvalue


class Foo(components.ezvalue.Value):
    """Value object docstring."""
    bar = """Docstring 1."""
    baz = """Docstring 2."""


class TestValueObject(util.TestCase):
    def test_create_immutable(self):
        foo = Foo(bar=1, baz='hi')
        self.assertEqual(foo.bar, 1)
        self.assertEqual(foo.baz, 'hi')
        with self.assertRaises(AttributeError):
            foo.bar = 3

    def test_construct_mutable_to_send_immutable(self):
        mutable_foo = Foo.Mutable()
        mutable_foo.bar = 1
        mutable_foo.baz = 'hi'
        mutable_foo.bar = 2
        foo = mutable_foo.immutable()
        self.assertEqual(foo.bar, 2)
        self.assertEqual(foo.baz, 'hi')
        with self.assertRaises(AttributeError):
            foo.bar = 3
