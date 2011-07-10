from respite.urls import resource, routes

from views import ArticleViews

urlpatterns = resource(
    prefix = 'articles/',
    views = ArticleViews,
    routes = [
        routes.index,
        routes.create,
        routes.show,
        routes.update,
        routes.delete,
        routes.edit,
        routes.new,
        routes.route(
            regex = lambda prefix: r'^%s(?P<id>[0-9]+)/preview(?:\.[a-zA-Z]+)?$' % prefix,
            view = 'preview',
            method = 'GET',
            name = lambda views: 'preview_%s_%s' % (views.model._meta.app_label, views.model.__name__.lower())
        )
    ]
)
