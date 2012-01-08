.. _installation:

Installation and configuration
==============================

Respite is best installed with `pip`_::

    $ pip install django-respite
    
.. _configuration:

Configuration
-------------

In your ``settings`` module...

* Add ``respite`` to ``INSTALLED_APPS``
* Add ``respite.middleware.HttpPutMiddleware`` to ``MIDDLEWARE_CLASSES``
* Add ``respite.middleware.HttpPatchMiddleware`` to ``MIDDLEWARE_CLASSES``
* Add ``respite.middleware.JsonMiddleware`` to ``MIDDLEWARE_CLASSES``

If you're not just building an API, you might also want to add ``respite.middleware.HttpMethodOverrideMiddleware``
to your middleware classes; it facilitates for overriding the HTTP method with the ``X-HTTP-Method-Override`` header or a
``_method`` HTTP POST parameter, which is the only way to replace, update and delete resources from a web browser.

.. note::

    ``HttpMethodOverrideMiddleware`` must be processed before ``HttpPutMiddleware`` and ``HttpPatchMiddleware``.

.. _dependencies:

Dependencies
------------

In order to install and use Respite, you will need four primary pieces of software:

* the Python programming language.
* the ``setuptools`` packaging/installation library.
* Django version 1.3 or later.

.. _development dependencies:

Development dependencies
------------------------

If you are interested in contributing to Respite, you will also need to install
some or all of the following packages:

* `pytest`_
* `sphinx`_

For an up-to-date list of exact testing/development requirements, including version numbers, please
see the ``DEPENDENCIES`` file included with the source distribution. This file is intended to be used
with ``pip``, e.g. ``pip install -r DEPENDENCIES``.

.. _source-code-checkouts:

Source code checkouts
---------------------

To follow Respite's development via Git instead of downloading official releases, please see our `Github mirror`_.

.. _pip: http://www.pip-installer.org/en/latest/
.. _pytest: http://pytest.org/
.. _sphinx: http://www.pip-installer.org/en/latest/
.. _Github mirror: http://github.com/jgorset/django-respite/
