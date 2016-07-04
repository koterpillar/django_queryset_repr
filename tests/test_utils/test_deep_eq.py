"""Test deep equality comparison."""

import unittest

from django_queryset_repr.utils.deep_eq import deep_eq


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

        self.assertTrue(deep_eq(x1, x1))
        self.assertTrue(deep_eq(x1, x1_same))

        self.assertFalse(deep_eq(x1, x2))
        self.assertFalse(deep_eq(x1, x3))
        self.assertFalse(deep_eq(x1, x4))
        self.assertFalse(deep_eq(x1, y1))

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

        self.assertTrue(deep_eq(x1, x1))
        self.assertTrue(deep_eq(x1, x1_same))

        self.assertFalse(deep_eq(x1, x2))
        self.assertFalse(deep_eq(x1, x3))

    def test_recursion(self):
        """Test deep equality for recursive structures."""

        x1 = self.create_object(self.X, foo=1)
        x1.bar = x1

        x1_same = self.create_object(self.X, foo=1)
        x1_same.bar = x1_same

        x2 = self.create_object(self.X, foo=2)
        x2.bar = x2

        self.assertTrue(deep_eq(x1, x1_same))
        self.assertFalse(deep_eq(x1, x2))
