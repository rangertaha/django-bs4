.. :changelog:

History
-------


0.1.0 (unreleased)
++++++++++++++++++

* Revive the package: complete the unfinished migration so it imports and
  runs again (wire up the ``{% load bs4 %}`` template tag library, fix the
  ``bootstrap3`` package/template references, and the broken renderer
  imports).
* Target Python 3.10+ and Django 5.2 LTS (drop end-of-life Django 4.2/5.0/5.1).
* Replace removed/deprecated Django APIs (``force_text`` → ``force_str``,
  ``django.forms.extras``, ``ugettext`` → ``gettext``, ``MIDDLEWARE_CLASSES``
  → ``MIDDLEWARE``, ``conf.urls`` → ``django.urls``).
* Honor ``set_required=False`` against Django's automatic HTML5 ``required``
  attribute.
* Modernize the codebase (drop ``__future__`` imports and Python 2 fallbacks,
  f-strings, ``super()``).
* Switch to PEP 621 packaging (``pyproject.toml`` + Hatchling) and add
  GitHub Actions CI plus PyPI Trusted Publishing.
* Add a standalone test runner (``runtests.py``); all 43 tests pass.


0.0.1 (2016-03-18)
+++++++++++++++++++

* Add Bootstrap 4 forms support
