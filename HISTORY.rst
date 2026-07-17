.. :changelog:

History
-------

This project keeps its changelog in the spirit of
`Keep a Changelog <https://keepachangelog.com/>`_ and follows
`Semantic Versioning <https://semver.org/>`_.


0.1.0 (unreleased)
++++++++++++++++++

Added
~~~~~

* Python 3.14 support; classifiers, CI matrix, and Ruff ``target-version``
  updated accordingly.
* GitHub Actions CI (tests across Python 3.12/3.13/3.14, Ruff lint/format,
  mypy) and a PyPI Trusted Publishing release workflow.
* Standalone test runner (``runtests.py``); all tests pass.
* Ruff (lint + format) and mypy configuration in ``pyproject.toml``.

Changed
~~~~~~~

* Require Python 3.12+ (SPEC 0).
* Pin Django to the 5.2 LTS line (``Django>=5.2,<6.0``); tested against
  Django 5.2.16 on Python 3.14. End-of-life Django releases (1.x-5.1) are
  no longer supported.
* Switch packaging to PEP 621 (``pyproject.toml`` + Hatchling), replacing
  ``setup.py``/``MANIFEST.in``.
* Adopt the ``src/`` layout (``src/bs4/``); the installed import path is
  unchanged (``import bs4``, ``{% load bs4 %}``). Tests moved from
  ``bs4/tests.py`` to ``tests/`` so they are no longer shipped in the wheel.
* Modernize the codebase for Python 3.12+ (drop ``__future__`` imports and
  Python 2 fallbacks, f-strings, plain ``super()``) and ``docs/conf.py``
  (drop ``u''`` prefixes and the ``coding: utf-8`` header).
* Replace removed/deprecated Django APIs (``force_text`` → ``force_str``,
  ``django.forms.extras``, ``ugettext`` → ``gettext``, ``MIDDLEWARE_CLASSES``
  → ``MIDDLEWARE``, ``conf.urls`` → ``django.urls``).

Fixed
~~~~~

* Revive the package: complete the unfinished ``bootstrap3`` → ``bs4``
  migration so it imports and runs again (wire up the ``{% load bs4 %}``
  template tag library, fix the ``bootstrap3`` package/template references
  and the broken renderer imports).
* Honor ``set_required=False`` against Django's automatic HTML5 ``required``
  attribute.

Removed
~~~~~~~

* Travis CI configuration (replaced by GitHub Actions).
* The unused ``bs4/legacy.py`` Python 2 compatibility shim.


0.0.2 - 0.0.4 (2020-01-26 - 2021-01-25)
+++++++++++++++++++++++++++++++++++++++

* Published to PyPI (0.0.2 on 2020-01-26, 0.0.3 on 2020-06-17, 0.0.4 on
  2021-01-25). No changelog was recorded in the repository for these
  releases; the release dates are reconstructed from PyPI.


0.0.1 (2016-03-18)
++++++++++++++++++

Added
~~~~~

* Initial release: Bootstrap 4 rendering for Django forms, formsets, and
  fields, plus template tags for buttons, alerts, icons, messages, and
  pagination, with a configurable ``BOOTSTRAP4`` settings dict and a demo
  project.
