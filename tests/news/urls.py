from respite.urls import resource, routes

from views import ArticleViews

urlpatterns = resource(
    prefix = 'articles/',
    views = ArticleViews,
    routes = [
        ArticleViews.index.route,
        ArticleViews.create.route,
        ArticleViews.show.route,
        ArticleViews.update.route,
        ArticleViews.replace.route,
        ArticleViews.destroy.route,
        ArticleViews.edit.route,
        ArticleViews.new.route,
        ArticleViews.preview.route
    ]
)
