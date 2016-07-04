"""Deep (structural) equality function."""

import types


def deep_eq(a, b):
    """
    Compare two objects structurally.

    The objects are structurally the same if and only if:
    - They are of the same type.
    - Either both of them have the same set of instance attributes, or neither
      has any instance attributes at all, and normal equality holds.
    - All of their corresponding instance attributes are structurally the same.
    """

    return all(
        a_attr == b_attr
        for a_attr, b_attr
        in zip(gen_attrs(a, '', set()), gen_attrs(b, '', set()))
    )


def assert_deep_eq(a, b):
    """
    Assert the two objects are structurally equal.

    On failure, a message explaining where is the difference found is produced.
    """

    for (path, a_attr), (_, b_attr) in zip(
            gen_attrs(a, '', set()), gen_attrs(b, '', set())):
        if a_attr != b_attr:
            raise AssertionError("{} is not {} (at path {})".format(
                a_attr, b_attr, path))


def gen_attrs(obj, prefix, seen):
    """
    An iterable of attributes to compare for structural equality.

    The iterables are element-by-element equal for arguments that are
    structurally the same.

    If an object is in 'seen', it's assumed to have been compared already.
    """

    if id(obj) in seen:
        return
    seen.add(id(obj))

    yield prefix + '.__class__', type(obj)

    # Since the types of the objects were compared, the results of all these
    # checks can be assumed to be the same for both objects
    if isinstance(obj, types.ModuleType):
        yield prefix + '.__name__', obj.__name__

    elif isinstance(obj, dict):
        keys = sorted(obj.keys())
        yield prefix + '.keys()', keys
        for key in keys:
            yield from gen_attrs(obj[key], prefix + '[{!r}]'.format(key), seen)

    elif isinstance(obj, (list, tuple)):
        yield prefix + '.__len__()', len(obj)
        for idx, item in enumerate(obj):
            yield from gen_attrs(item, prefix + '[{!r}]'.format(idx), seen)

    elif hasattr(obj, '__dict__'):
        keys = sorted(obj.__dict__.keys())
        yield prefix + '.__dict__', keys
        for key in keys:
            yield from gen_attrs(getattr(obj, key), prefix + '.' + key, seen)

    elif hasattr(type(obj), '__slots__'):
        slots = getattr(obj, '__slots__')
        yield slots
        for slot in slots:
            yield prefix + '.__hasattr__({!r})'.format(slot), hasattr(obj, slot)
            yield from gen_attrs(getattr(obj, slot), prefix + '.' + slot, seen)

    else:
        yield prefix, obj
