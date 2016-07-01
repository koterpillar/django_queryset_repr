"""Base test classes."""

import sys
import os
import unittest

import django


class TestCase(unittest.TestCase):
    """Test class setting up Django environment."""

    def setUp(self):
        """Set up Django with the test application."""

        sys.path.insert(
            0, os.path.join(os.path.dirname(__file__), 'test_django_project'))
        os.environ['DJANGO_SETTINGS_MODULE'] = 'test_django_project.settings'
        django.setup()

        # Import models from the test application
        import garden.models
        self.models = garden.models
