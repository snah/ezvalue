import collections
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

    def test_comparing_values_with_equal_values_returns_true(self):
        foo1 = Foo(bar=1, baz='hi')
        foo2 = Foo(bar=1, baz='hi')
        self.assertTrue(foo1 == foo2)
        self.assertFalse(foo1 != foo2)

    def test_comparing_values_with_inequal_values_returns_false(self):
        foo1 = Foo(bar=1, baz='hi')
        foo2 = Foo(bar=2, baz='hi')
        self.assertFalse(foo1 == foo2)
        self.assertTrue(foo1 != foo2)

    def test_compares_inequal_to_named_tuple(self):
        foo = Foo(bar=1, baz='hi')
        Foo_tuple = collections.namedtuple('Foo_tuple', ('bar', 'baz'))
        foo_tuple = Foo_tuple(bar=1, baz='hi')
        self.assertFalse(foo == foo_tuple)
        self.assertFalse(foo_tuple == foo)
        self.assertTrue(foo != foo_tuple)
        self.assertTrue(foo_tuple != foo)

    def test_compares_inequal_to_different_value_object(self):
        class NotFoo(ezvalue.Value):
            bar = 'docstring'
            baz = 'docstring'
            spam = 'docstring'

        foo = Foo(bar=1, baz='hi')
        not_foo = NotFoo(bar=1, baz='hi', spam='spam')
        self.assertFalse(foo == not_foo)
        self.assertFalse(not_foo == foo)
        self.assertTrue(foo != not_foo)
        self.assertTrue(not_foo != foo)

    # TODO: compare to mutable

    def test_string_representation(self):
        foo = Foo(bar=1, baz='hi')
        string = str(foo)
        self.assertIn('Foo', string)
        self.assertIn('bar=1', string)
        self.assertIn('baz=hi', string)

    def test_repr(self):
        foo = Foo(bar=1, baz='hi')
        string = repr(foo)
        self.assertIn('Foo', string)
        self.assertIn('bar=1', string)
        self.assertIn("baz='hi'", string)

    def test_repr_works_in_exec(self):
        foo = Foo(bar=1, baz='hi')
        string = repr(foo)
        foo2 = eval(string)
        self.assertEqual(foo2.bar, 1)
        self.assertEqual(foo2.baz, 'hi')


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
