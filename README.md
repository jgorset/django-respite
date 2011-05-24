# Respite

## About

Respite conforms Django to [Representational State Transfer (REST)](http://en.wikipedia.org/wiki/Representational_State_Transfer).

## Requirements

* Django v1.3 or later

## Usage

### Primer

Respite is influenced by Ruby on Rails, though in the spirit of Python it is not nearly as "magic". It will, however, save you a lot of code:

    # news/models.py
    
    from django.db import models
    
    class Article(models.Model):
        title = models.CharField(max_length=255)
        content = models.TextField()
        published = True
        created_at = models.DateTimeField(auto_now_add=True)

    # news/urls.py
    
    from django.conf.urls.defaults import *
    from respite.urls import resource
    from views import ArticleView
    
    urlpatterns = resource(
        prefix = 'news/articles',
        view = ArticleView
    )

    # news/views.py
    
    from respite import View
    from models import Article
    
    class ArticleView(View):
        model = Article
        template_path = 'news/articles'
        supported_formats = ['html', 'json']
    
    # templates/news/articles/index.html
    
    <!DOCTYPE html>
    <html>
        <head>
            <title>{{ article.title }}</title>
        </head>
        <body>
            {% for article in articles %}
            <article>
                <h1><a href="{% url news_article id=article.id %}">{{ article.title }}</a></h1>
                <time datetime="{{ article.created_at.isoformat }}">{{ article.created_at }}</time>
                <p>
                    {{ article.content }}
                </p>
            </article>
            {% endfor %}
        </body>
    </html>
    
    # templates/news/articles/index.json
    # ...

### Default actions

Respite's `View` class defines actions for viewing and manipulating model instances;
`index`, `show`, `new`, `create`, `edit`‚ `update` and `destroy`.

    HTTP method         HTTP path           Function            Purpose
    
    GET                 articles/           index               Render a list of articles
    GET                 articles/new        new                 Render a form to create a new article
    POST                articles/           create              Create a new article
    GET                 articles/1          show                Render a specific article
    GET                 articles/1/edit     edit                Render a form to edit a specific article
    PUT                 articles/1          update              Edit a specific article
    DELETE              articles/1          destroy             Delete a specific article
    
In a nutshell, Respite provides you with a collection of features you probably need for most of your models and routes them
RESTfully. You may override any or all of these functions and customize them as you'd like. For example, you could only list
articles that have been published:

    # news/views.py

    class ArticleView(View):
        model = Article
        template_path = 'news/articles'
        supported_formats = ['html', 'json']
        
        def index(self, request):
            articles = self.model.objects.filter(published=True)
            
            return self._render(
                request = request,
                template = 'index',
                context = {
                    'articles': articles,
                },
                status = 200
            )
            
You may also omit one or several of the default actions altogether. For example, you could only implement the `index` and `show` actions:

    # news/urls.py
    
    from django.conf.urls.defaults import *
    from respite.urls import resource
    from views import ArticleView
    
    urlpatterns = resource(
        prefix = 'news/articles',
        view = ArticleView,
        actions = ['index', 'show']
    )
            
### Custom actions
            
You are not limited to Respite's seven predefined actions; you may add any number of custom actions and
route them however you like:

    # news/urls.py
    
    from django.conf.urls.defaults import *
    from respite.urls import resource, action
    from views import ArticleView
    
    urlpatterns = resource(
        prefix = 'news/articles',
        view = ArticleView,
        custom_actions = [
            action(
                regex = r'(?P<id>[0-9]+)/preview\.?[a-zA-Z]*$',
                function = 'preview',
                methods = ['GET'],
                name = 'preview_news_article'
            )
        ]
    )

    # news/views.py

    from respite import View
    from models import Article

    class ArticleView(View):
        model = Article
        template_path = 'news/articles'
        supported_formats = ['html', 'json']
        
        def preview(self, request, id):
            article = Article.objects.get(id=id)
            
            return self._render(
                request = request,
                template = 'preview',
                context = {
                    'article': article
                },
                status = 200
            )


## Installation

* `pip install git+http://github.com/jgorset/respite.git`
* Add `respite` to `INSTALLED_APPS` in your settings file
* Add `respite.middleware.HTTPPUTMiddleware` to `MIDDLEWARE_CLASSES` in your settings file

If you're not just building an API, you might also want to add `respite.middleware.HTTPMethodOverrideMiddleware`
to your middleware classes; it facilitates for overriding the HTTP method with the `X-HTTP-Method-Override` header or a
`_method` HTTP POST parameter, which is the only way to update (HTTP PUT) and delete (HTTP DELETE) resources from
a web browser.
