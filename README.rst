
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


Quick start
-----------

Installation
^^^^^^^^^^^^

.. code-block:: bash

   # install
   pip install pybugsnag

Basic Usage
^^^^^^^^^^^

.. code-block:: python

    from pybugsnag import BugsnagDataClient
    from pybugsnag.models import Error

    client = BugsnagDataClient("$AUTH_TOKEN")
    organization = client.organizations[0]  # first organization for the auth token
    project = organization.projects[0]  # first project in the organization
    project.get_errors(
        sort=Error.Sort.LAST_SEEN,
        direction=Error.Sort.Direction.DESCENDING,
        per_page=30,
    )  # gets errors for this project, 
    project.get_trend_buckets()  # data for a trend histogram
