
pybugsnag
=========


.. image:: https://badge.fury.io/py/pybugsnag.svg
    :target: https://badge.fury.io/py/pybugsnag
    :alt: PyPI version


.. image:: https://travis-ci.org/jpetrucciani/pybugsnag.svg?branch=master
    :target: https://travis-ci.org/jpetrucciani/pybugsnag
    :alt: Build Status


.. image:: https://coveralls.io/repos/github/jpetrucciani/pybugsnag/badge.svg?branch=master
    :target: https://coveralls.io/github/jpetrucciani/pybugsnag?branch=master
    :alt: Coverage Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black
    :alt: Code style: black


.. image:: https://readthedocs.org/projects/pybugsnag/badge/?version=latest
    :target: https://pybugsnag.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


A python wrapper for the Bugsnag Data Access API

COMING SOON!

Quick start
-----------

Installation
^^^^^^^^^^^^

.. code-block:: bash

   # install pybugsnag
   pip install pybugsnag

Basic Usage
^^^^^^^^^^^

.. code-block:: python

   from pybugsnag import BugsnagDataAccessClient

   bugsnag_client = BugsnagDataAccessClient("$ACCESS_TOKEN")
