"""Test qs_repr()."""

from django_queryset_repr import qs_repr

from .base import TestCase


class ReprTestCase(TestCase):
    """Test qs_repr()."""

    def test_all(self):
        """Test representation of .all()."""

        qs_all = self.models.Tree.objects.all()
        self.assertEqual(qs_repr(qs_all), 'Tree.objects.all()')
