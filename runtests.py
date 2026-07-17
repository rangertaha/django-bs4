#!/usr/bin/env python
"""Standalone test runner for django-bs4.

Run with ``python runtests.py`` (optionally passing test labels).
"""

import os
import sys

import django
from django.conf import settings

# Run against the in-tree package (src/ layout) and make ``tests`` importable
# without requiring an editable install first.
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, ROOT)


def main():
    settings.configure(
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.sites",
            "django.contrib.messages",
            "django.contrib.staticfiles",
            "django.contrib.admin",
            "bs4",
        ],
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": [
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                    ],
                },
            }
        ],
        MIDDLEWARE=[
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
        ],
        STATIC_URL="/static/",
        USE_TZ=True,
        SITE_ID=1,
        SECRET_KEY="django-bs4-test-secret-key",
        # Values the test suite asserts against.
        BOOTSTRAP4={
            "required_css_class": "bootstrap3-req",
            "error_css_class": "bootstrap3-err",
            "success_css_class": "bootstrap3-bound",
            "javascript_in_head": True,
        },
    )
    django.setup()

    from django.test.utils import get_runner

    test_runner = get_runner(settings)()
    labels = sys.argv[1:] or ["tests"]
    failures = test_runner.run_tests(labels)
    sys.exit(bool(failures))


if __name__ == "__main__":
    main()
