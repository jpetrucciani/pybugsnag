.. _quickstart:

Quickstart
==========

This document presents a brief, high-level overview of pybugsnag's primary features.

pybugsnag is a python wrapper for the Bugsnag Data Access API

.. note::
    Be aware that this uses the `Bugsnag Data Access API <https://clickup.com/api>`_ directly. The Bugsnag Data Access API is currently in beta, and is subject to change.

At the time of writing, ClickUp has the following limits in place for API requests:

- 100 requests per minute per token

Installation
------------

.. code-block:: bash

    # install pybugsnag
    pip install pybugsnag


Basic Usage
-----------

.. code-block:: python

   from pybugsnag import BugsnagDataClient
