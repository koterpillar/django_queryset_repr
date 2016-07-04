"""Test deep equality comparison."""

import unittest

from django_queryset_repr.utils.deep_eq import assert_deep_eq, deep_eq


class DeepEqTest(unittest.TestCase):
    """Test deep equality function."""

    class X(object):
        """Test class for comparisons."""
        pass

    class Y(object):
        """Test class for comparisons, not related to X."""
        pass

    @staticmethod
    def create_object(type_, **attrs):
        """Create an object and set attributes on it."""

        obj = type_()
        for key, value in attrs.items():
            setattr(obj, key, value)
        return obj

    def assert_deep_equal(self, a, b):
        """Assert that the two objects are tested as structurally the same."""

        self.assertTrue(deep_eq(a, b))
        assert_deep_eq(a, b)

    def assert_not_deep_equal(self, a, b, expected_path):
        """
        Assert that the two objects are tested as not structurally the same,
        and the first difference is found at expected_path.
        """

        self.assertFalse(deep_eq(a, b))
        with self.assertRaises(AssertionError) as raised:
            assert_deep_eq(a, b)
        self.assertIn("(at path {})".format(expected_path),
                      str(raised.exception))

    def test_deep_eq(self):
        """Test deep equality function."""

        x1 = self.create_object(self.X, foo=1, bar=2)

        # This is the same as x1
        x1_same = self.create_object(self.X, foo=1, bar=2)

        # Not the same as x1
        x2 = self.create_object(self.X, foo=1, bar=3)

        # Missing an attribute
        x3 = self.create_object(self.X, foo=1)

        # Extra attribute
        x4 = self.create_object(self.X, foo=1, bar=2, baz=3)

        # Same attributes, different class
        y1 = self.create_object(self.Y, foo=1, bar=2)

        self.assert_deep_equal(x1, x1)
        self.assert_deep_equal(x1, x1_same)

        self.assert_not_deep_equal(x1, x2, '.bar')
        self.assert_not_deep_equal(x1, x3, '.__dict__')
        self.assert_not_deep_equal(x1, x4, '.__dict__')
        self.assert_not_deep_equal(x1, y1, '.__class__')

    class SlotX(object):
        """Test class for comparisons, with __slots__."""
        __slots__ = ['foo', 'bar']

    def test_slots(self):
        """Test deep equality with __slots__."""

        x1 = self.create_object(self.SlotX, foo=1, bar=2)

        # This is the same as x1
        x1_same = self.create_object(self.SlotX, foo=1, bar=2)

        # Not the same as x1
        x2 = self.create_object(self.SlotX, foo=1, bar=3)

        # Missing an attribute
        x3 = self.create_object(self.SlotX, foo=1)

        self.assert_deep_equal(x1, x1)
        self.assert_deep_equal(x1, x1_same)

        self.assert_not_deep_equal(x1, x2, '.bar')
        self.assert_not_deep_equal(x1, x3, '.__hasattr__(\'bar\')')

    def test_recursion(self):
        """Test deep equality for recursive structures."""

        x1 = self.create_object(self.X, foo=1)
        x1.bar = x1

        x1_same = self.create_object(self.X, foo=1)
        x1_same.bar = x1_same

        x2 = self.create_object(self.X, foo=2)
        x2.bar = x2

        self.assert_deep_equal(x1, x1_same)
        self.assert_not_deep_equal(x1, x2, '.foo')

    def test_dict(self):
        """Test deep equality for dictionaries."""

        d1 = {'foo': 1, 'bar': 2}
        d1_same = {'foo': 1, 'bar': 2}

        d2 = {'foo': 1, 'bar': 3}
        d3 = {'foo': 1}
        d4 = {'foo': 1, 'bar': 2, 'baz': 3}

        self.assert_deep_equal(d1, d1_same)
        self.assert_not_deep_equal(d1, d2, '[\'bar\']')
        self.assert_not_deep_equal(d1, d3, '.keys()')
        self.assert_not_deep_equal(d1, d4, '.keys()')

    def test_recursive_dict(self):
        """Test recursive dictionaries."""

        d1 = {'foo': 1}
        d1['bar'] = d1

        d1_same = {'foo': 1}
        d1_same['bar'] = d1_same

        d2 = {'foo': 2}
        d2['bar'] = d2

        self.assert_deep_equal(d1, d1_same)
        self.assert_not_deep_equal(d1, d2, '[\'foo\']')
