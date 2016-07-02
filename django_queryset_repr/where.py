"""Representation of where clauses."""

from django.db.models.sql.where import NothingNode


def where_repr(where):
    """Representation of a 'where' clause."""

    if isinstance(where, NothingNode):
        return 'none()'
    if not where.children:
        return 'all()'
    raise NotImplementedError
