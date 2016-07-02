"""Main module for django_queryset_repr."""

from .where import where_repr


def qs_repr(queryset):
    """Representation of a queryset."""

    # FIXME: 'objects' might not be the name of the default manager
    return queryset.model.__name__ + \
        '.objects.' + \
        where_repr(queryset.query.where)
