======================
Bootstrap 4 for Django
======================

Bootstrap 4 for  Django projects



Write Django as usual, and let ``django-bs4`` make template output into Bootstrap 4 code.


.. image:: https://travis-ci.org/rangertaha/django-bs4.svg?branch=master
    :target: https://travis-ci.org/rangertaha/django-bs4

.. image:: https://img.shields.io/pypi/v/django-bs4.svg
    :target: https://pypi.python.org/pypi/django-bs4
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/django-bs4.svg
    :target: https://pypi.python.org/pypi/django-bs4
    :alt: Number of PyPI downloads per month


Requirements
------------

- Python 2.7, 3.2, 3.3, 3.4, or 3.5
- Django >= 1.8



Installation
------------

1. Install using pip:

   ``pip install django-bs4``

   Alternatively, you can install download or clone this repo and call ``pip install -e .``.


2. Add to INSTALLED_APPS in your ``settings.py``:

   ``'bs4',``

3. In your templates, load the ``bs4`` library and use the tags:



Example template
----------------

   .. code:: Django

    {% load bs4 %}

    <form action="/" method="post" class="form">
        {% csrf_token %}

        {% bs4_form form %}

        <button type="submit" class="btn btn-primary">Submit</button>
    </form>


Documentation
-------------

The full documentation is at http://django-bs4.readthedocs.org/.


Bugs and suggestions
--------------------

If you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.

https://github.com/rangertaha/django-bs4/issues


License
-------

You can use this under Apache 2.0. See `LICENSE
<LICENSE>`_ file for details.


Author
------

Developed and maintained by `Rangertaha <https://github.com/rangertaha>`_.

Please see AUTHORS.rst for a list of contributors.
