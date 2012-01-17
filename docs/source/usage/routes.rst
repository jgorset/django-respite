.. _routing:

Routing
=======

Respite connects views to URLs through ``resource`` declarations, each of which define routes
for a particular collection of views.

.. autofunction:: respite.urls.resource

    ::

        # urls.py

        urlpatterns = resource(
            prefix = 'posts/',
            views = PostViews,
            routes = [
                ...
            ]
        )

Routes
------

There are two ways in which you might populate the resource's routes: you can declare
them inline using the ``route`` function, or reference views that have been decorated with
the ``route`` decorator.

Inline routes
^^^^^^^^^^^^^

.. autofunction:: respite.urls.routes.route

::

    # urls.py

    urlpatterns = resource(
        prefix = 'posts/',
        views = PostViews,
        routes = [
            # Route GET requests to 'posts/' to the 'index' view.
            routes.route(
                regex = r'^(?:$|index(?:\.[a-zA-Z]+)?$)',
                view = 'index',
                method = 'GET',
                name = 'blog_posts'
            ),
            # Route GET requests 'posts/1' to the 'show' view.
            routes.route(
                regex = r'^(?P<id>[0-9]+)(?:\.[a-zA-Z]+)?$',
                view = 'show',
                method = 'GET',
                name = 'blog_post'
            )
        ]
    )

Referenced routes
^^^^^^^^^^^^^^^^^

.. autofunction:: respite.decorators.route

::

    # views.py
    
    class PostViews:
    
        @route(
            regex = r'^(?:$|index(?:\.[a-zA-Z]+)?$)',
            method = 'GET',
            name = 'blog_posts'
        )
        def index(request):
            ...
        
        @route(
            regex = r'^(?P<id>[0-9]+)(?:\.[a-zA-Z]+)?$',
            method = 'GET',
            name = 'blog_post'
        )
        def show(request, id):
            ...

::

    # urls.py

    urlpatterns = resource(
        prefix = 'posts/',
        views = PostViews,
        routes = [
            PostViews.index.route,
            PostViews.show.route
        ]
    )
