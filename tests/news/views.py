from django.shortcuts import render

from respite import Views, Resource
from respite.decorators import route

from models import Article

class ArticleViews(Views, Resource):
    model = Article
    template_path = 'articles/'
    supported_formats = ['html', 'json']

    @route(
        regex = r'^(?P<id>[0-9]+)/preview(?:\.[a-zA-Z]+)?$',
        method = 'GET',
        name = 'preview_news_article'
    )
    def preview(self, request, id):
        try:
            article = Article.objects.get(id=id)
        except Article.DoesNotExist:
            return render(
                request = request,
                template_name = '404.html',
                status = 404
            )

        return self._render(
            request = request,
            template = 'preview',
            context = {
                'article': article
            },
            status = 200
        )
