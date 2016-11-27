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

    def test_init_with_named_tuple(self):
        Foo_tuple = collections.namedtuple('Foo_tuple', ('bar', 'baz'))
        foo_tuple = Foo_tuple(bar=1, baz='hi')
        foo = Foo(foo_tuple)
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
        self.assertIsNotNone(foo)

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

    def test_create_mutable_from_instance(self):
        foo = Foo(bar=1, baz='hi')
        mutable_foo = foo.mutable()
        self.assertEqual(mutable_foo.bar, 1)
        self.assertEqual(mutable_foo.baz, 'hi')

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

    def test_compares_equal_to_mutable_value_with_same_values(self):
        foo = Foo(bar=1, baz='hi')
        mutable_foo = foo.mutable()
        self.assertTrue(foo == mutable_foo)
        self.assertFalse(foo != mutable_foo)

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

    def test_initialize_with_named_tuple(self):
        Foo_tuple = collections.namedtuple('Foo_tuple', ('bar', 'baz'))
        foo_tuple = Foo_tuple(bar=1, baz='hi')
        mutable_foo = Foo.Mutable(foo_tuple)
        self.assertEqual(mutable_foo.bar, 1)
        self.assertEqual(mutable_foo.baz, 'hi')

    def test_init_ignores_extra_attributes_in_source_object(self):
        Foo_tuple = collections.namedtuple('Foo_tuple', ('bar', 'baz', 'spam'))
        foo_tuple = Foo_tuple(bar=1, baz='hi', spam='spam')
        mutable_foo = Foo.Mutable(foo_tuple)
        self.assertEqual(mutable_foo.bar, 1)
        self.assertEqual(mutable_foo.baz, 'hi')
        self.assertFalse(hasattr(mutable_foo, 'spam'))

    def test_initialize_with_source_with_missing_attributes(self):
        Foo_tuple = collections.namedtuple('Foo_tuple', ('bar', ))
        foo_tuple = Foo_tuple(bar=1)
        mutable_foo = Foo.Mutable(foo_tuple)
        self.assertEqual(mutable_foo.bar, 1)

    def test_create_two_different_mutable_classes(self):
        class Foo2(ezvalue.Value):
            a = """Docstring 1"""
            b = """Docstring 2"""

        self.assertCountEqual(Foo.Mutable()._attributes, ('bar', 'baz'))
        self.assertCountEqual(Foo2.Mutable()._attributes, ('a', 'b'))

    def test_list_attributes(self):
        foo = Foo(bar=1, baz='hi')
        mutable_foo = Foo.Mutable()
        self.assertCountEqual(mutable_foo._attributes, ('bar', 'baz'))

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

    def test_compares_equal_values_to_mutable_with_equal_values(self):
        mutable_foo1 = Foo.Mutable(bar=1, baz='hi')
        mutable_foo2 = Foo.Mutable(bar=1, baz='hi')
        self.assertTrue(mutable_foo1 == mutable_foo2)
        self.assertFalse(mutable_foo1 != mutable_foo2)

    def test_compares_inequal_values_to_mutable_with_inequal_values(self):
        mutable_foo1 = Foo.Mutable(bar=1, baz='hi')
        mutable_foo2 = Foo.Mutable(bar=2, baz='hi')
        self.assertFalse(mutable_foo1 == mutable_foo2)
        self.assertTrue(mutable_foo1 != mutable_foo2)

    def test_compares_equal_to_immutable_value_with_same_values(self):
        mutable_foo = Foo.Mutable(bar=1, baz='hi')
        foo = mutable_foo.immutable()
        self.assertTrue(mutable_foo == foo)
        self.assertFalse(mutable_foo != foo)

    def test_compares_inequal_to_immutable_value_with_different_values(self):
        mutable_foo = Foo.Mutable(bar=1, baz='hi')
        foo = mutable_foo.immutable()
        mutable_foo.bar = 2
        self.assertFalse(mutable_foo == foo)
        self.assertTrue(mutable_foo != foo)

    def test_compares_inequal_to_named_tuple(self):
        mutable_foo = Foo.Mutable(bar=1, baz='hi')
        Foo_tuple = collections.namedtuple('Foo_tuple', ('bar', 'baz'))
        foo_tuple = Foo_tuple(bar=1, baz='hi')
        self.assertFalse(mutable_foo == foo_tuple)
        self.assertFalse(foo_tuple == mutable_foo)
        self.assertTrue(mutable_foo != foo_tuple)
        self.assertTrue(foo_tuple != mutable_foo)
