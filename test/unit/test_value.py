# pylint: disable=blacklisted-name,protected-access,no-self-use
# pylint: disable=unused-variable,attribute-defined-outside-init

import collections
import unittest

import ezvalue


class Foo(ezvalue.Value):
    """Value object docstring."""

    bar = """Docstring 1."""
    baz = """Docstring 2."""


class _TestValueObjetBase:
    # pylint: disable = no-member
    def test_init_with_kwargs(self):
        # pylint: disable=blacklisted-name
        foo = self.CUT(bar=1, baz='hi')
        self.assert_attribute_values_equal(foo, 1, 'hi')

    def test_init_with_named_tuple(self):
        FooTuple = collections.namedtuple('FooTuple', ('bar', 'baz'))
        foo_tuple = FooTuple(bar=1, baz='hi')
        foo = self.CUT(foo_tuple)
        self.assert_attribute_values_equal(foo, 1, 'hi')

    def test_init_from_mutable(self):
        mutable_foo = Foo.Mutable()
        mutable_foo.bar = 1
        mutable_foo.baz = 'hi'
        foo = self.CUT(mutable_foo)
        self.assert_attribute_values_equal(foo, 1, 'hi')

    def test_init_from_immutable(self):
        immutable_foo = Foo(bar=1, baz='hi')
        foo = self.CUT(immutable_foo)
        self.assert_attribute_values_equal(foo, 1, 'hi')

    def test_kwargs_overwrite_source_object_values(self):
        source_foo = Foo(bar=1, baz='hi')
        foo = self.CUT(source_foo, baz='bye')
        self.assert_attribute_values_equal(foo, 1, 'bye')

    def test_supplement_attributes_with_kwargs(self):
        mutable_foo = Foo.Mutable()
        mutable_foo.bar = 1
        foo = self.CUT(mutable_foo, baz='bye')
        self.assert_attribute_values_equal(foo, 1, 'bye')

    def test_unkown_attributes_in_constructor_are_ignored(self):
        foo = self.CUT(bar=1, baz='hi', unknown='spam')

    def test_iterate_over_attributes(self):
        foo = self.CUT(bar=1, baz='hi')
        self.assertCountEqual(iter(foo), ('bar', 'baz'))

    def test_contains_attributes(self):
        foo = self.CUT(bar=1, baz='hi')
        self.assertTrue('bar' in foo)
        self.assertFalse('spam' in foo)

    def test_compares_equal_to_mutable_with_equal_values(self):
        foo = self.CUT(bar=1, baz='hi')
        mutable_foo = Foo.Mutable(bar=1, baz='hi')
        self.assertTrue(foo == mutable_foo)
        self.assertFalse(foo != mutable_foo)

    def test_compares_equal_to_immutable_value_with_equal_values(self):
        foo = self.CUT(bar=1, baz='hi')
        immutable_foo = Foo(bar=1, baz='hi')
        self.assertTrue(foo == immutable_foo)
        self.assertFalse(foo != immutable_foo)

    def test_compares_inequal_when_inequal_values(self):
        foo1 = self.CUT(bar=1, baz='hi')
        foo2 = self.CUT(bar=2, baz='hi')
        self.assertFalse(foo1 == foo2)
        self.assertTrue(foo1 != foo2)

    def test_compares_inequal_to_named_tuple(self):
        foo = self.CUT(bar=1, baz='hi')
        FooTuple = collections.namedtuple('FooTuple', ('bar', 'baz'))
        foo_tuple = FooTuple(bar=1, baz='hi')
        self.assertFalse(foo == foo_tuple)
        self.assertFalse(foo_tuple == foo)
        self.assertTrue(foo != foo_tuple)
        self.assertTrue(foo_tuple != foo)

    def test_compares_inequal_to_different_value_object(self):
        class NotFoo(ezvalue.Value):
            bar = 'docstring'
            baz = 'docstring'
            spam = 'docstring'

        foo = self.CUT(bar=1, baz='hi')
        not_foo = NotFoo(bar=1, baz='hi', spam='spam')
        self.assertFalse(foo == not_foo)
        self.assertFalse(not_foo == foo)
        self.assertTrue(foo != not_foo)
        self.assertTrue(not_foo != foo)

    def test_string_representation(self):
        foo = self.CUT(bar=1, baz='hi')
        string = str(foo)
        self.assertIn(self.class_name, string)
        self.assertIn('bar=1', string)
        self.assertIn('baz=hi', string)

    def test_repr(self):
        foo = self.CUT(bar=1, baz='hi')
        string = repr(foo)
        self.assertIn(self.class_name, string)
        self.assertIn('bar=1', string)
        self.assertIn("baz='hi'", string)

    def test_repr_works_in_exec(self):
        # pylint: disable = eval-used
        foo = self.CUT(bar=1, baz='hi')
        string = repr(foo)
        foo2 = eval(string, {self.class_name: self.CUT})
        self.assertEqual(foo2.bar, 1)
        self.assertEqual(foo2.baz, 'hi')

    def test_hash_differs_when_different_values(self):
        foo1 = self.CUT(bar=1, baz='hi')
        foo2 = self.CUT(bar=2, baz='hi')
        self.assertNotEqual(hash(foo1), hash(foo2))

    def test_hash_equal_for_same_values(self):
        foo1 = self.CUT(bar=1, baz='hi')
        foo2 = self.CUT(bar=1, baz='hi')
        self.assertEqual(hash(foo1), hash(foo2))

    def test_hash_when_mutable_values(self):
        foo = Foo(bar=1, baz=[1, 2])
        self.assertIsNotNone(foo)

    def assert_attribute_values_equal(self, foo, bar, baz):
        """Assert that the attribute values are equal to those given."""
        self.assertEqual(foo.bar, bar)
        self.assertEqual(foo.baz, baz)


class TestValueObject(unittest.TestCase, _TestValueObjetBase):
    CUT = Foo   # Class Under Test
    class_name = 'Foo'

    def test_direct_instantiation(self):
        empty_value = ezvalue.Value()
        self.assertCountEqual(empty_value._attributes, [])

    def test_missing_attributes_in_constructor_raises_attribute_error(self):
        with self.assertRaisesRegex(AttributeError, 'baz'):
            foo = Foo(bar=2)

    def test_create_mutable_from_instance(self):
        foo = Foo(bar=1, baz='hi')
        mutable_foo = foo.to_mutable()
        self.assert_attribute_values_equal(mutable_foo, 1, 'hi')

    def test_setting_attribute_raises_exception(self):
        foo = Foo(bar=1, baz='hi')
        with self.assertRaises(AttributeError):
            foo.bar = 3

    def test_non_extisting_attribute_raises_exception(self):
        foo = Foo(bar=1, baz='hi')
        with self.assertRaises(AttributeError):
            foo.non_existing = 'hi'

    def test_delete_attribute_raises_exception(self):
        foo = Foo(bar=1, baz='hi')
        with self.assertRaises(AttributeError):
            del foo.non_existing

    def test_additional_methods(self):
        class ValueWithMethod(ezvalue.Value):
            bar = """test"""

            def method(self):
                return 'hi'

        value = ValueWithMethod(bar=1)
        self.assertEqual(value.method(), 'hi')


class TestMutableValueObject(unittest.TestCase, _TestValueObjetBase):
    CUT = Foo.Mutable   # Class Under Test
    class_name = 'MutableFoo'

    def test_missing_kwargs_does_not_raise_exception(self):
        foo = self.CUT(bar=1)
        self.assertEqual(foo.bar, 1)

    def test_init_ignores_extra_attributes_in_source_object(self):
        FooTuple = collections.namedtuple('FooTuple', ('bar', 'baz', 'spam'))
        foo_tuple = FooTuple(bar=1, baz='hi', spam='spam')
        foo = Foo.Mutable(foo_tuple)
        self.assertEqual(foo.bar, 1)
        self.assertEqual(foo.baz, 'hi')
        self.assertFalse(hasattr(foo, 'spam'))

    def test_initialize_with_source_with_missing_attributes(self):
        FooTuple = collections.namedtuple('FooTuple', ('bar', ))
        foo_tuple = FooTuple(bar=1)
        foo = Foo.Mutable(foo_tuple)
        self.assertEqual(foo.bar, 1)

    def test_create_two_different_mutable_classes(self):
        # Testing because the mutable class is created dynamically.
        class Foo2(ezvalue.Value):
            attr1 = """Docstring 1"""
            attr2 = """Docstring 2"""

        self.assertCountEqual(Foo.Mutable()._attributes, ('bar', 'baz'))
        self.assertCountEqual(Foo2.Mutable()._attributes, ('attr1', 'attr2'))

    def test_set_attribute(self):
        foo = Foo.Mutable()
        foo.bar = 1
        self.assertEqual(foo.bar, 1)

    def test_set_non_existing_attribute(self):
        foo = Foo.Mutable()
        foo.spam = 3
        self.assertEqual(foo.spam, 3)

    def test_create_immutable_from_instance(self):
        foo = Foo.Mutable()
        foo.bar = 1
        foo.baz = 'hi'
        immutable_foo = foo.to_immutable()
        self.assertEqual(immutable_foo.bar, 1)
        self.assertEqual(immutable_foo.baz, 'hi')
