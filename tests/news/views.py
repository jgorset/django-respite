from django.shortcuts import render

from respite.views import Views

from models import Article

class ArticleViews(Views):
    model = Article
    template_path = 'articles/'
    supported_formats = ['html', 'json']

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
