"""Models for test application."""

from django.db import models


class Tree(models.Model):
    """A tree."""

    color = models.CharField(max_length=100)
    height = models.IntegerField()


class Leaf(models.Model):
    """A tree's leaf."""

    tree = models.ForeignKey(Tree, related_name='leaves')
    size = models.IntegerField()
