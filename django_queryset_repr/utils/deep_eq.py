"""Deep (structural) equality function."""


SENTINEL = object()  # Object distinct from anything defined elsewhere


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
        in zip(gen_attrs(a, set()), gen_attrs(b, set()))
    )


def gen_attrs(obj, seen):
    """
    An iterable of attributes to compare for structural equality.

    The iterables are element-by-element equal for arguments that are
    structurally the same.

    If an object is in 'seen', it's assumed to have been yielded already.
    """

    if obj in seen:
        return
    seen.add(obj)

    yield type(obj)

    has_dict = hasattr(obj, '__dict__')
    yield has_dict
    if has_dict:
        keys = sorted(obj.__dict__.keys())
        yield keys
        for key in keys:
            yield from gen_attrs(getattr(obj, key), seen)
    else:
        has_slots = hasattr(type(obj), '__slots__')
        yield has_slots
        if has_slots:
            slots = getattr(obj, '__slots__')
            yield slots
            for slot in slots:
                yield from gen_attrs(getattr(obj, slot, SENTINEL), seen)
        else:
            yield obj
