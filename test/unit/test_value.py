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

    def test_init_immutable_with_mutable(self):
        mutable_foo = Foo.Mutable()
        mutable_foo.bar = 1
        mutable_foo.baz = 'hi'
        foo = Foo(mutable_foo)
        self.assertEqual(foo.bar, 1)
        self.assertEqual(foo.baz, 'hi')

    def test_kwargs_overwrite_source_object_values(self):
        mutable_foo = Foo.Mutable()
        mutable_foo.bar = 1
        mutable_foo.baz = 'hi'
        foo = Foo(mutable_foo, baz='bye')
        self.assertEqual(foo.bar, 1)
        self.assertEqual(foo.baz, 'bye')

    def test_supplement_attributes_with_kwargs(self):
        mutable_foo = Foo.Mutable()
        mutable_foo.bar = 1
        foo = Foo(mutable_foo, baz='bye')
        self.assertEqual(foo.bar, 1)
        self.assertEqual(foo.baz, 'bye')

    def test_missing_attributes_in_constructor_raises_attribute_error(self):
        with self.assertRaisesRegex(AttributeError, 'baz'):
            foo = Foo(bar=2)

    def test_unkown_attributes_in_constructor_are_ignored(self):
        foo = Foo(bar=1, baz='hi', unknown='spam')

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

class TestMutableValueObject(unittest.TestCase):
    def test_initialize_with_keyword_argument(self):
        mutable_foo = Foo.Mutable(bar=1)
        self.assertEqual(mutable_foo.bar, 1)

    def test_initialize_with_value_object(self):
        foo = Foo(bar=1, baz='hi')
        mutable_foo = Foo.Mutable(foo)
        self.assertEqual(mutable_foo.bar, 1)
        self.assertEqual(mutable_foo.baz, 'hi')

    def test_set_attribute(self):
        mutable_foo = Foo.Mutable()
        mutable_foo.bar = 1
        self.assertEqual(mutable_foo.bar, 1)

    def test_create_immutable(self):
        mutable_foo = Foo.Mutable()
        mutable_foo.bar = 1
        mutable_foo.baz = 'hi'
        foo = mutable_foo.immutable()
        self.assertEqual(foo.bar, 1)
        self.assertEqual(foo.baz, 'hi')
