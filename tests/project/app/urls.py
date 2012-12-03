from django.utils.translation import ugettext_lazy as _

from respite.urls import resource

from .views import ArticleViews

urlpatterns = resource(
    prefix = _('articles/'),
    views = ArticleViews,
    routes = ArticleViews.routes + [
        ArticleViews.preview.route
    ]
)
