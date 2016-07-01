Django queryset repr
====================

Make [Django][django] querysets representation show the querysets themselves,
not the results of running them.

```python
>>> repr(Tree.objects.filter(color__in=["green", "red"]))
"[<Tree: spruce>, <Tree: maple>]"

>>> from django_queryset_repr import qs_repr
>>> qs_repr(Tree.objects.filter(color__in=["green", "red"]))
"Tree.objects.filter(color__in=['green', 'red'])"
```

Status
------

Under development.

[django]: https://www.djangoproject.com/
