"""Representation of querysets."""

from . import where


def qs_repr(queryset):
    """Representation of a queryset."""

    # FIXME: 'objects' might not be the name of the default manager
    return queryset.model.__name__ + \
        '.objects.' + \
        where.where_repr(queryset.query.where)
