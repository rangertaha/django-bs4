#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
try:
    from setuptools import setup, Command
except ImportError:
    from distutils.core import setup, Command

import bs4

version = bs4.__version__

with open('README.rst') as readme_file:
    readme = readme_file.read()


class Publish(Command):
    description = 'Build documentation and upload to pypi.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('cd docs && make html')
        os.system('python setup.py sdist upload')


setup(
    name='django-bs4',
    version=bs4.__version__,
    description="""Bootstrap 4 for Django""",
    long_description=readme,
    author='Rangertaha',
    author_email='rangertaha@gmail.com',
    url='https://github.com/rangertaha/django-bs4',
    packages=[
        'bs4',
    ],
    include_package_data=True,
    install_requires=[],
    cmdclass={
        'publish': Publish,
    },
    license="The MIT License",
    zip_safe=False,
    keywords='django-bootstrap4',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)
