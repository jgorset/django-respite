.. _routes:

Routes
======

Respite connects views to URLs through ``resource`` declarations, each of which define routes
for a particular collection of views.

.. autofunction:: respite.urls.resource

There are two ways to go about providing a ``resource`` declaration with its ``routes`` argument: You can
either declare them using the ``route`` function, or attach them to their respective view using the ``route``
decorator.

.. autofunction:: respite.urls.routes.route

.. autofunction:: respite.decorators.route

.. note::

    If you prefer to attach routes to their respective views using the ``route`` decorator, the
    ``routes`` argument to the ``resource`` declaration must reference the ``route`` property of the view
    functions routed in this way.
