"""Representation of where clauses."""

from django.db.models.sql.where import (
    AND,
    NothingNode,
    WhereNode,
)
from django.db.models.expressions import Col


def where_repr(where):
    """Representation of a 'where' clause."""

    if isinstance(where, NothingNode):
        return 'none()'
    if not isinstance(where, WhereNode):
        raise NotImplementedError
    if not where.children:
        return 'all()'
    if where.connector != AND:
        raise NotImplementedError
    return 'filter({})'.format(', '.join(
        lookup_repr(lookup)
        for lookup in where.children
    ))


def lookup_repr(lookup):
    """Representation of a lookup."""

    lookup_name = '' if lookup.lookup_name == 'exact' else \
        '__' + lookup.lookup_name
    if not isinstance(lookup.lhs, Col):
        raise NotImplementedError
    lhs = lookup.lhs.target.name
    # FIXME: This should use qs_repr
    rhs = repr(lookup.rhs)

    return '{}{}={}'.format(lhs, lookup_name, rhs)
