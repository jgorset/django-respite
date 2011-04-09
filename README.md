# Respite

## About

Respite conforms Django to [Representational State Transfer (REST)](http://en.wikipedia.org/wiki/Representational_State_Transfer).

## Requirements

* Django v1.3 or later

## Example

    # models.py
    
    from django import models
    
    class Article(models.Model):
        title = models.CharField(max_length=255)
        content = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)


    # urls.py
    
    from django.conf.urls.defaults import *
    from respite.urls import resource
    from views import ArticleViews
    
    urlpatterns = resource(
        prefix = 'articles',
        views = ArticleView
    )


    # views.py
    
    from respite import View
    from models import Article
    
    class ArticleView(View):
        model = Post
        template_path = 'articles'
        supported_formats = ['html', 'json']
    
    # templates/articles/index.html
    
    <!DOCTYPE html>
    <html>
        <head>
            <title>{{ article.title }}</title>
        </head>
        <body>
            {% for article in articles %}
            <article>
                <h1><a href="{% url article id=article.id %}">{{ article.title }}</a></h1>
                <time datetime="{{ article.created_at.isoformat }}">{{ article.created_at }}</time>
                <p>
                    {{ article.content }}
                </p>
            </article>
            {% endfor %}
        </body>
    </html>
    
    # templates/articles/index.json
    
    [
        {% for article in articles %}
        {
            "id": article.id,
            "title": "{{ article.title }}",
            "content": "{{ article.content }}",
            "created_at": "{{ article.created_at.isoformat }}",
            "url": "{% url article id=article.id %}"
        }{% if not forloop.last %},{% endif %}
        {% endfor %}
    ]
    
    ...

## Installation

* `pip install git+http://github.com/jgorset/respite.git`
* Add `respite.middleware.HTTPPUTMiddleware` your middleware classes.

If you're not just building an API, you might also want to add `respite.middleware.HTTPMethodOverrideMiddleware`
to your middleware classes; it facilitates for overriding the HTTP method with the `X-HTTP-Method-Override` header or a
`_method` HTTP POST parameter, which is the only way to update (HTTP PUT) and delete (HTTP DELETE) resources from
a web browser.

