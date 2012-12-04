from django.shortcuts import render

from respite import Views, Resource
from respite.decorators import route, before

from models import Article

class ArticleViews(Views, Resource):
    model = Article
    template_path = 'articles/'
    supported_formats = ['html', 'json', 'yaml']

    @route(
        regex = Resource.index.route.regex,
        method = Resource.index.route.method,
        name = Resource.index.route.name
    )
    def index(self, request):
        """Render a list of objects."""
        articles = Article.objects.all()

        return self._render(
            request = request,
            template = 'index',
            context = {
                'articles': articles,
            },
            status = 200
        )

    @route(
        regex = r'^(?P<id>[0-9]+)/preview(?:\.[a-zA-Z]+)?$',
        method = 'GET',
        name = 'preview_article'
    )
    @before('_load')
    def preview(self, request, article):
        return self._render(
            request = request,
            template = 'preview',
            context = {
                'article': article
            },
            status = 200
        )

    def _load(self, request, id):
        """Load the article with the given id."""
        try:
            return request, Article.objects.get(id=id)
        except Article.DoesNotExist:
            return self._error(request, 404, message='The article could not be found.')
