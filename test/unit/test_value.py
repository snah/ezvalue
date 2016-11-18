import unittest

import ezvalue


class Foo(ezvalue.Value):
    """Value object docstring."""

    bar = """Docstring 1."""
    baz = """Docstring 2."""


class TestValueObject(unittest.TestCase):
    def test_direct_instantiation(self):
        empty_value = ezvalue.Value()
        self.assertCountEqual(empty_value._attributes, [])

    def test_list_attributes(self):
        self.assertCountEqual(Foo._attributes, ('bar', 'baz'))

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

    def test_init_immutable_with_mutable(self):
        mutable_foo = Foo.Mutable()
        mutable_foo.bar = 1
        mutable_foo.baz = 'hi'
        foo = Foo(mutable_foo)
        self.assertEqual(foo.bar, 1)
        self.assertEqual(foo.baz, 'hi')

    def test_overwrite_attributes_with_kwargs(self):
        mutable_foo = Foo.Mutable()
        mutable_foo.bar = 1
        mutable_foo.baz = 'hi'
        foo = Foo(mutable_foo, baz='bye')
        self.assertEqual(foo.bar, 1)
        self.assertEqual(foo.baz, 'bye')


    #TODO: test missing attributes.
    #TODO: test supplement attributes.
