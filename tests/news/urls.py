from respite.urls import resource, action

from views import ArticleViews

urlpatterns = resource(
    prefix = 'articles/',
    views = ArticleViews,
    custom_actions = [
        action(
            regex = r'(?P<id>[0-9]+)/preview(?:\.[a-zA-Z]+)?',
            function = 'preview',
            methods = ['GET'],
            name = 'preview_news_article'
        )
    ]
)
