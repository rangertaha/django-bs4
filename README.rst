==========
django-bs4
==========

Bootstrap 4 forms and components for Django templates.

.. image:: https://github.com/rangertaha/django-bs4/actions/workflows/ci.yml/badge.svg?branch=master
    :target: https://github.com/rangertaha/django-bs4/actions/workflows/ci.yml
    :alt: CI status

.. image:: https://img.shields.io/pypi/v/django-bs4.svg
    :target: https://pypi.org/project/django-bs4/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue.svg
    :target: https://pypi.org/project/django-bs4/
    :alt: Supported Python versions

.. image:: https://img.shields.io/badge/license-MIT-green.svg
    :target: https://github.com/rangertaha/django-bs4/blob/master/LICENSE
    :alt: MIT License

What
----

``django-bs4`` is a reusable Django app that renders plain Django forms,
formsets, fields, buttons, alerts, messages, and pagination as
`Bootstrap 4 <https://getbootstrap.com/docs/4.6/>`_ markup. Write your forms
as usual and let the ``bs4`` template tag library take care of the HTML.

Requires Python 3.12+ and Django 5.2 LTS.

Install
-------

Install from PyPI:

.. code:: bash

    pip install django-bs4

Or install the development version from a checkout:

.. code:: bash

    pip install -e .

Then add ``bs4`` to ``INSTALLED_APPS`` in your ``settings.py``:

.. code:: python

    INSTALLED_APPS = [
        # ...
        "bs4",
    ]

Usage
-----

Load the ``bs4`` library in your templates and use its tags:

.. code:: django

    {% load bs4 %}

    <form action="/" method="post" class="form">
        {% csrf_token %}

        {% bootstrap_form form %}

        {% buttons %}
            <button type="submit" class="btn btn-primary">Submit</button>
        {% endbuttons %}
    </form>

Commonly used tags include:

- ``{% bootstrap_form form %}`` / ``{% bootstrap_formset formset %}`` --
  render a whole form or formset
- ``{% bootstrap_field form.field %}`` -- render a single field
- ``{% bootstrap_css %}`` / ``{% bootstrap_javascript %}`` -- include the
  Bootstrap 4 static assets from a CDN
- ``{% bootstrap_button "Save" button_type="submit" %}`` and
  ``{% bootstrap_alert "Done!" alert_type="success" %}``
- ``{% bootstrap_messages %}`` -- render ``django.contrib.messages``
- ``{% bootstrap_pagination page %}`` -- render a paginator

Configuration
-------------

All settings are optional and live in a single ``BOOTSTRAP4`` dict in your
``settings.py``. The defaults are defined in ``bs4/bootstrap.py``; the most
common overrides:

.. code:: python

    BOOTSTRAP4 = {
        # CDN locations of the static assets.
        "base_url": "//cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/",
        "jquery_url": "//code.jquery.com/jquery.min.js",
        # Layout classes for horizontal forms.
        "horizontal_label_class": "col-md-3",
        "horizontal_field_class": "col-md-9",
        # Field rendering behavior.
        "set_required": True,
        "set_placeholder": True,
        "required_css_class": "",
        "error_css_class": "has-error",
        "success_css_class": "has-success",
    }

Development
-----------

.. code:: bash

    # Run the test suite (uses the standalone Django test runner).
    python runtests.py

    # Lint, format, and type-check.
    ruff check .
    ruff format --check .
    mypy

    # Try the demo project.
    cd demo && python manage.py runserver

Bugs and suggestions
--------------------

Please use the issue tracker on GitHub:
https://github.com/rangertaha/django-bs4/issues

License
-------

MIT. See the `LICENSE <LICENSE>`_ file for details.

Author
------

Developed and maintained by `Rangertaha <https://github.com/rangertaha>`_.
See `AUTHORS.rst <AUTHORS.rst>`_ for a list of contributors.
