"""Test qs_repr()."""

from django_queryset_repr import qs_repr
from django_queryset_repr.utils.deep_eq import assert_deep_eq

from .base import TestCase


class ReprTestCase(TestCase):
    """Test qs_repr()."""

    def assert_reproducible(self, queryset):
        """Assert a queryset is reproducible using its representation."""

        repr_ = qs_repr(queryset)
        new_queryset = eval(repr_, self.models.__dict__)
        assert_deep_eq(queryset, new_queryset)

    def test_all(self):
        """Test representation of .all()."""

        qs_all = self.models.Tree.objects.all()
        self.assertEqual(qs_repr(qs_all), 'Tree.objects.all()')
        self.assert_reproducible(qs_all)

    def test_filter(self):
        """Test representation of a filtered queryset."""

        filtered = self.models.Tree.objects.filter(color="red")
        self.assertEqual(qs_repr(filtered),
                         """Tree.objects.filter(color='red')""")
        self.assert_reproducible(filtered)
