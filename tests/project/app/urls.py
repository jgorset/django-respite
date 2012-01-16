from respite.urls import resource

from .views import ArticleViews

urlpatterns = resource(
    prefix = 'articles/',
    views = ArticleViews,
    routes = ArticleViews.routes + [
        ArticleViews.preview.route
    ]
)
