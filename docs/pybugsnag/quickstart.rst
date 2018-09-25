.. _quickstart:

Quickstart
==========

This document presents a brief, high-level overview of pybugsnag's primary features.

pybugsnag is a python wrapper for the Bugsnag Data Access API

.. note::
    Be aware that this uses the `Bugsnag Data Access API <https://bugsnagapiv2.docs.apiary.io>`_ directly. The Bugsnag Data Access API we use here is `Version 2 <https://bugsnagapiv2.docs.apiary.io/#introduction/versioning>`_.


Installation
------------

.. code-block:: bash

    # install pybugsnag
    pip install pybugsnag


Basic Usage
-----------

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


Rate Limiting
-------------

The following is pulled directly from the `Bugsnag Data Client API specifications <https://bugsnagapiv2.docs.apiary.io/#introduction/rate-limiting>`_.

The time window for rate limits is 1 minute.

Requests that have not been denied due to rate limiting will have the following response headers:

- X-RateLimit-Limit: number of requests allowed per time window
- X-RateLimit-Remaining: number of requests remaining in the current time window


.. note::
  Requests that have been rate limited will return a 429 response code and have a Retry-After response header to indicate how long you should wait (in seconds) before trying again.

