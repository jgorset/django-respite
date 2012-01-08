.. _routing:

Routing
======

Respite connects views to URLs through ``resource`` declarations, each of which define routes
for a particular collection of views.

.. autofunction:: respite.urls.resource

Routes
------

There are two ways to go about providing a ``resource`` declaration with its ``routes`` argument: You can
either declare them using the ``route`` function, or attach them to their respective view using the ``route``
decorator:

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

.. autofunction:: respite.decorators.route

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
