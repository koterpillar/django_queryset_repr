"""Test qs_repr()."""

from django_queryset_repr import qs_repr

from .base import TestCase


class ReprTestCase(TestCase):
    """Test qs_repr()."""

    def test_all(self):
        """Test representation of .all()."""

        qs_all = self.models.Tree.objects.all()
        self.assertEqual(qs_repr(qs_all), 'Tree.objects.all()')

    def test_filter(self):
        """Test representation of a filtered queryset."""

        filtered = self.models.Tree.objects.filter(color="red")
        self.assertEqual(qs_repr(filtered),
                         """Tree.objects.filter(color='red')""")
