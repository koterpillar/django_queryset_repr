"""Django settings for the test project."""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'n+jzjqlko6$za^uy+&$m33)$zjye!txayqz0bru7o1j+rwz-40'

INSTALLED_APPS = [
    'garden',
]

ROOT_URLCONF = 'test_django_project.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
