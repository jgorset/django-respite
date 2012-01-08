.. _overview-and-tutorial:

Overview and Tutorial
=====================

Welcome to Respite! This document is a whirlwind tour of Respite's
features and a quick guide to its use. Additional documentation (which
is linked to throughout) can be found in the :ref:`usage-documentation`.

.. note::

    This tutorial assumes that you are least vaguely familiar with Django and
    Representational State Transfer.

Tutorial
--------

I'd like to walk you through the creation of a simple blog application
with Respite.

A Django application that leverages Respite is not so different from an
ordinary Django application; it, too, has models, views, templates
and routes. It's pretty tricky to create a RESTful web application with
Django by default, though, so Respite does some of these things a little
differently than you might expect from a vanilla Django application.

Setup
^^^^^

Please create a new Django project and install Respite according
to the :ref:`installation instructions <installation>`. When you're done,
create a new application and include its ``urls`` module in your project's
url configuration like you normally would::

    $ python manage.py startapp blog
    $ vim urls.py

Models
^^^^^^

Models are unchanged in Respite, but let's define one for good measure::

    # blog/models.py
    
    from django.db import models

    class Post(models.Model):
        title = models.CharField(max_length=255)
        content = models.TextField()
        is_published = models.BooleanField()
        created_at = models.DateTimeField(auto_now_add=True)

Views
^^^^^

Next, let's make some views for our ``Post`` model. Our application should
have an index of all posts and separate pages for each individual post.
In Respite, views are encapsulated in classes according to the model
they supervise::

    # blog/views.py
    
    from respite import Views
    
    from models import Post
    
    class PostViews(Views):
        supported_formats = ['html', 'json']
        
        def index(self, request):
            """Render a list of blog posts."""
            posts = Post.objects.all()
            
            return self._render(
                request = request,
                template = 'news/articles/index',
                context = {
                    'posts': posts
                },
                status = 200
            )

        def show(self, request, id):
            """Render a single blog post."""
            post = Post.objects.get(pk=id)
            
            return self._render(
                request = request,
                template = 'news/articles/show',
                context = {
                    'post': post
                },
                status = 200
            )

You can name and route views however you like, but the canonical way to go about
it is as follows:

=================== =================== =================== ========================================
HTTP path           HTTP method         View                Purpose
=================== =================== =================== ========================================
articles/           GET                 index               Render a list of articles
articles/           POST                create              Create a new article
articles/new        GET                 new                 Render a form to create a new article
articles/1          GET                 show                Render a specific article
articles/1/edit     GET                 edit                Render a form to edit a specific article
articles/1          PUT                 replace             Replace a specific article
articles/1          PATCH               update              Update a specific article
articles/1          DELETE              destroy             Delete a specific article
=================== =================== =================== ========================================

You can construct your views' HTTP responses however you like, too, but in the end you'll
probably want to use ``self._render`` because it allows your views to be format-agnostic.

.. admonition:: See also

    :ref:`Usage documentation for views <views>`

Routes
^^^^^^

Respite routes views through ``resource`` declarations, each of which define routes for a
particular collection of views. For example, one might route the ``PostViews`` class that
we defined earlier like so::

    # blog/urls.py

    from respite.urls import resource, routes

    from views import PostViews

    urlpatterns = resource(
        prefix = 'posts/',
        views = PostViews,
        routes = [
            # Route 'posts/' to the 'index' view.
            routes.route(
                regex = r'^(?:$|index(?:\.[a-zA-Z]+)?$)',
                view = 'index',
                method = 'GET',
                name = 'blog_posts'
            ),
            # Route 'posts/1' to the 'show' view.
            routes.route(
                regex = r'^(?P<id>[0-9]+)(?:\.[a-zA-Z]+)?$',
                view = 'show',
                method = 'GET',
                name = 'blog_post'
            )
        ]
    )

.. admonition:: See also

    :ref:`Usage documentation for routing <routing>`
    
Templates
^^^^^^^^^

Templates, too, are unchanged in Respite::

    # templates/news/articles/index.html

    <!DOCTYPE html>
    
    <html>

        <head>
            <title>My awesome blog</title>
        </head>
    
        <body>
        
            {% for post in posts %}
                <h1>{{ post.title }}</h1>
                <time datetime="{{ post.created_at.isoformat }}">{{ post.created_at }}</time>
                {{ post.content|linebreaks }}
            {% endfor %}
    
        </body>
    
    </html>
    
    # templates/news/articles/show.html

    <!DOCTYPE html>
    
    <html>

        <head>
            <title>My awesome blog</title>
        </head>
    
        <body>
        
            <h1>{{ post.title }}</h1>
            <time datetime="{{ post.created_at.isoformat }}">{{ post.created_at }}</time>
            {{ post.content|linebreaks }}
    
        </body>
    
    </html>

Conclusion
^^^^^^^^^^

That's it, you're done! Let's check out your new blog. ::

    $ python manage.py runserver
    
Create some dummy blog posts and point your browser to ``http://localhost:8000/blog/posts/index.html``.
As you might expect, Respite will populate one of your HTML templates with the
context you defined in the ``index`` view.

That's cool and all, but the real power of Respite (besides conforming Django to the way HTTP is
supposed to work) is data representation. In the end, someone always wants to create an iPhone
app to do something really silly (like reading your blog) and so HTML just doesn't cut it anymore.

In an ordinary Django application, you would need to write another set of views or use a library
like `Piston`_ to represent your blog posts in different formats. In an application that leverages
Respite, though, your views are inherently format-agnostic. Your blog is already available
in JSON, and Respite will serialize its articles automatically.
`Check it out <http://localhost:8000/blog/posts/index.json>`_!

.. note::

    You can specify the request format by extension or the the `accept header`_.
    
.. _accept header: http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.1
.. _Piston: https://bitbucket.org/jespern/django-piston

This application makes use of a large portion of Respite's feature set, but there's still a lot of things we haven't
covered here. Please make sure you follow the various "see also" links, and check out the documentation table of contents
on :ref:`the main index page <index>`.
