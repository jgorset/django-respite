.. _views:

Views
=====

In Respite, views are encapsulated in classes according to the model they supervise. You are
not required to subclass Respite's ``Views`` class, but doing so will yield some things you might
find useful:

.. autoclass:: respite.Views
    :members: _render

Default views
-------------

Respite defines a collection of views that facilitate for common features like viewing a list
of items, viewing a specific item by its id, rendering a form to create a new item and so on. You
can leverage these views by adding Respite's ``Resource`` class to the base classes of your views class.

.. autoclass:: respite.Resource
    
    .. automethod:: respite.Resource.index(request)
    .. automethod:: respite.Resource.show(request, id)
    .. automethod:: respite.Resource.new(request)
    .. automethod:: respite.Resource.create(request)
    .. automethod:: respite.Resource.update(request, id)
    .. automethod:: respite.Resource.replace(request, id)
    .. automethod:: respite.Resource.destroy(request, id)
